<script setup lang="ts">
import { ref, computed, onMounted, nextTick, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import api from '../api';
import AppModal from '../components/AppModal.vue';
import ComboBox from '../components/ComboBox.vue';
import type { Recipe, Ingredient } from '../types';
import { PlusIcon, TrashIcon, CalculatorIcon, PencilIcon } from '@heroicons/vue/24/outline';

const { t } = useI18n();
const recipes = ref<Recipe[]>([]);
const ingredients = ref<Ingredient[]>([]);
const isModalOpen = ref(false);
const isCalcModalOpen = ref(false);
const editingRecipe = ref<Recipe | null>(null);
const isLoading = ref(false);

const isCreateIngredientOpen = ref(false);
const createTargetIndex = ref<number | null>(null);
const createForm = ref({ name: '', unit: 'kg', category: '', notes: '' });

const selectedRecipeForCalc = ref<Recipe | null>(null);
const calcQty = ref(1);
const calcResults = ref<any>(null);

const form = ref<Recipe>({
  name: '',
  instructions: '',
  notes: '',
  components: []
});

const initialFormSnapshot = ref('');
const formDirty = computed(() => {
  const c = JSON.parse(JSON.stringify(form.value));
  c.components?.forEach((x: any) => delete x._type);
  return JSON.stringify(c) !== initialFormSnapshot.value;
});

const fetchData = async () => {
  try {
    const [recipesRes, ingredientsRes] = await Promise.all([
      api.get('recipes/'),
      api.get('ingredients/')
    ]);
    recipes.value = recipesRes.data;
    ingredients.value = ingredientsRes.data;
  } catch (error) {
    console.error('Error fetching data:', error);
  }
};

onMounted(fetchData);

const openCreateIngredient = (index: number) => {
  createTargetIndex.value = index;
  createForm.value = { name: '', unit: 'kg', category: '', notes: '' };
  isCreateIngredientOpen.value = true;
};

const cancelCreateIngredient = () => {
  isCreateIngredientOpen.value = false;
  createTargetIndex.value = null;
};

const saveNewIngredient = async () => {
  try {
    const res = await api.post('ingredients/', createForm.value);
    const newIng = res.data;
    await fetchData();
    if (createTargetIndex.value !== null && form.value.components[createTargetIndex.value]) {
      form.value.components[createTargetIndex.value].ingredient = newIng.id;
    }
    isCreateIngredientOpen.value = false;
    createTargetIndex.value = null;
  } catch (error) {
    console.error('Error creating ingredient:', error);
  }
};

const fmtQty = (qty: number, unit: string): string => {
  const n = normalizeDisplay(qty, unit);
  return `${n.qty.toFixed(n.decimals)} ${n.unit}`;
};

const normalizeDisplay = (qty: number, unit: string): { qty: number; unit: string; decimals: number } => {
  const u = unit.toLowerCase();
  if (u === 'g' || u === 'gr') {
    return { qty: Math.round(qty * 1000 * 100) / 100, unit: 'g', decimals: 1 };
  }
  if (u === 'kg') {
    if (qty < 1) {
      return { qty: Math.round(qty * 1000 * 100) / 100, unit: 'g', decimals: 1 };
    }
    return { qty: Math.round(qty * 1000) / 1000, unit: 'kg', decimals: 3 };
  }
  if (u === 'l') {
    if (qty < 1) {
      return { qty: Math.round(qty * 1000 * 100) / 100, unit: 'ml', decimals: 1 };
    }
    return { qty: Math.round(qty * 1000) / 1000, unit: 'L', decimals: 3 };
  }
  if (u === 'ml') {
    return { qty: Math.round(qty * 1000 * 100) / 100, unit: 'ml', decimals: 1 };
  }
  return { qty: Math.round(qty * 1000) / 1000, unit, decimals: 0 };
};

const totalWeight = ref(1);
const isExpertMode = ref(false);
const componentRaw = ref<Record<number, { qty: number; unit: string }>>({});

const normalizeKg = (qty: number, unit: string): number => {
  const u = unit.toLowerCase();
  if (u === 'kg') return qty;
  if (u === 'g' || u === 'gr') return qty / 1000;
  if (u === 'l') return qty;
  if (u === 'ml') return qty / 1000;
  return qty;
};

const getComponentUnit = (comp: any): string => {
  if (comp.ingredient) {
    const ing = ingredients.value.find(i => i.id === comp.ingredient);
    return ing?.unit || 'kg';
  }
  return 'kg';
};

const getComponentAbs = (comp: any): string => {
  const pct = Number(comp.value) || 0;
  const absKg = (pct / 100) * totalWeight.value;
  return fmtQty(absKg, getComponentUnit(comp));
};

const pctSum = computed(() => {
  let sum = 0;
  for (const comp of form.value.components) {
    sum += Number(comp.value) || 0;
  }
  return Math.round(sum * 10) / 10;
});

const calcPctFromRaw = (index: number) => {
  const entry = componentRaw.value[index];
  const comp = form.value.components[index];
  if (!entry || !comp) return;
  const kg = entry.qty > 0 && totalWeight.value > 0 ? normalizeKg(entry.qty, entry.unit) : 0;
  comp.value = kg > 0 ? Math.round((kg / totalWeight.value) * 100 * 10) / 10 : 0;
};

const reverseCalcRaw = (comp: any): { qty: number; unit: string } => {
  const pct = Number(comp.value) || 0;
  const absKg = totalWeight.value > 0 ? (pct / 100) * totalWeight.value : 0;
  const unit = getComponentUnit(comp);
  const u = unit.toLowerCase();
  if (u === 'g' || u === 'gr') {
    return { qty: Math.round(absKg * 1000 * 100) / 100, unit: 'g' };
  }
  if (u === 'ml') {
    return { qty: Math.round(absKg * 1000 * 100) / 100, unit: 'ml' };
  }
  if (u === 'L') {
    return { qty: Math.round(absKg * 1000) / 1000, unit: 'L' };
  }
  return { qty: Math.round(absKg * 1000) / 1000, unit };
};

const rebuildRawFromPct = () => {
  const raw: Record<number, { qty: number; unit: string }> = {};
  form.value.components.forEach((comp: any, i: number) => {
    raw[i] = reverseCalcRaw(comp);
  });
  componentRaw.value = raw;
};

const toggleInputMode = () => {
  isExpertMode.value = !isExpertMode.value;
  if (!isExpertMode.value) {
    rebuildRawFromPct();
  }
};

watch(componentRaw, () => {
  if (isExpertMode.value) return;
  for (const key of Object.keys(componentRaw.value)) {
    calcPctFromRaw(parseInt(key));
  }
}, { deep: true });

watch(totalWeight, (newVal, oldVal) => {
  if (isExpertMode.value || form.value.components.length === 0 || !oldVal || oldVal <= 0) return;
  const scale = newVal / oldVal;
  if (scale === 1) return;
  const raw: Record<number, { qty: number; unit: string }> = {};
  form.value.components.forEach((_c: any, i: number) => {
    const entry = componentRaw.value[i];
    raw[i] = {
      qty: entry?.qty ? Math.round(entry.qty * scale * 1000) / 1000 : 0,
      unit: entry?.unit || 'kg',
    };
  });
  componentRaw.value = raw;
});

const openModal = async (recipe: Recipe | null = null) => {
  isCreateIngredientOpen.value = false;
  createTargetIndex.value = null;
  isExpertMode.value = false;
  if (recipe) {
    editingRecipe.value = { ...recipe };
    const cloned = JSON.parse(JSON.stringify(recipe));
    form.value = cloned;
  } else {
    editingRecipe.value = null;
    form.value = { name: '', instructions: '', notes: '', components: [] };
  }
  const snap = JSON.parse(JSON.stringify(form.value));
  snap.components?.forEach((x: any) => delete x._type);
  initialFormSnapshot.value = JSON.stringify(snap);
  totalWeight.value = 1;
  await nextTick();
  rebuildRawFromPct();
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
  editingRecipe.value = null;
  form.value = { name: '', instructions: '', notes: '', components: [] };
  isCreateIngredientOpen.value = false;
  createTargetIndex.value = null;
  isExpertMode.value = false;
  componentRaw.value = {};
  initialFormSnapshot.value = '';
};

const addComponent = () => {
  const idx = form.value.components.length;
  form.value.components.push({ value: 0, unit: 'kg' });
  componentRaw.value[idx] = { qty: 0, unit: 'kg' };
};

const removeComponent = (index: number) => {
  form.value.components.splice(index, 1);
  const newRaw: Record<number, { qty: number; unit: string }> = {};
  Object.keys(componentRaw.value).forEach((k) => {
    const ki = parseInt(k);
    if (ki < index) newRaw[ki] = componentRaw.value[ki];
    else if (ki > index) newRaw[ki - 1] = componentRaw.value[ki];
  });
  componentRaw.value = newRaw;
};

const saveRecipe = async () => {
  isLoading.value = true;
  try {
    const payload = JSON.parse(JSON.stringify(form.value));
    payload.components.forEach((c: any) => {
      delete c._type;
      c.unit = getComponentUnit(c);
    });
    if (editingRecipe.value?.id) {
      await api.put(`recipes/${editingRecipe.value.id}/`, payload);
    } else {
      await api.post('recipes/', payload);
    }
    await fetchData();
    closeModal();
  } catch (error) {
    console.error('Error saving recipe:', error);
    alert(t('common.save') + ' failed.');
  } finally {
    isLoading.value = false;
  }
};

const deleteRecipe = async (id: number) => {
  if (!confirm(t('common.delete') + '?')) return;
  try {
    await api.delete(`recipes/${id}/`);
    await fetchData();
  } catch (error) {
    console.error('Error deleting recipe:', error);
  }
};

const openCalcModal = (recipe: Recipe) => {
  selectedRecipeForCalc.value = recipe;
  calcQty.value = 1;
  calcResults.value = null;
  isCalcModalOpen.value = true;
};

const runCalculation = async () => {
  if (!selectedRecipeForCalc.value) return;
  isLoading.value = true;
  try {
    const response = await api.get(`recipes/${selectedRecipeForCalc.value.id}/calculate/`, {
      params: { qty: calcQty.value }
    });
    calcResults.value = response.data;
  } catch (error) {
    console.error('Calculation error:', error);
  } finally {
    isLoading.value = false;
  }
};

const getComponentType = (comp: any) => {
  return comp._type || (comp.sub_recipe ? 'sub_recipe' : 'ingredient');
};

const setComponentType = (comp: any, type: 'ingredient' | 'sub_recipe') => {
  comp._type = type;
  if (type === 'ingredient') {
    comp.sub_recipe = undefined;
  } else {
    comp.ingredient = undefined;
  }
};
</script>

<template>
  <div class="animate-in fade-in duration-500">
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
      <div>
        <h2 class="text-3xl font-black text-gray-900 dark:text-white">{{ t('recipes.title') }}</h2>
        <p class="mt-1 text-gray-500 dark:text-gray-400 font-medium">{{ t('recipes.subtitle') }}</p>
      </div>
      <button @click="openModal()" class="w-full sm:w-auto bg-primary-600 text-white px-6 py-3 rounded-2xl font-bold hover:bg-primary-700 transition-all shadow-lg shadow-primary-500/20 active:scale-95">
        {{ t('recipes.createBtn') }}
      </button>
    </div>

    <div class="mt-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="recipe in recipes" :key="recipe.id" class="group bg-white dark:bg-gray-800 p-6 rounded-3xl shadow-xl shadow-gray-200/50 dark:shadow-none border border-gray-100 dark:border-gray-700 hover:border-primary-300 dark:hover:border-primary-500 transition-all">
        <div @click="openModal(recipe)" class="cursor-pointer">
          <div class="flex justify-between items-start">
            <h3 class="text-xl font-black text-gray-900 dark:text-white">{{ recipe.name }}</h3>
            <PencilIcon class="w-5 h-5 text-gray-400 opacity-0 group-hover:opacity-100 transition-opacity" />
          </div>
          <p class="mt-3 text-sm text-gray-500 dark:text-gray-400 line-clamp-3 overflow-hidden font-medium">
            {{ recipe.instructions || '---' }}
          </p>
        </div>
        
        <div class="mt-6 flex justify-between items-center pt-4 border-t border-gray-100 dark:border-gray-700">
          <button @click="openCalcModal(recipe)" class="p-2 text-primary-600 dark:text-primary-400 hover:bg-primary-50 dark:hover:bg-primary-900/30 rounded-xl transition-colors">
            <CalculatorIcon class="w-6 h-6" />
          </button>
          <div class="flex space-x-4">
            <button @click="openModal(recipe)" class="text-sm font-black text-primary-600 dark:text-primary-400 hover:text-primary-800">{{ t('common.edit') }}</button>
            <button @click="deleteRecipe(recipe.id!)" class="text-sm font-black text-red-600 dark:text-red-400 hover:text-red-800">{{ t('common.delete') }}</button>
          </div>
        </div>
      </div>
      
      <div v-if="recipes.length === 0" class="col-span-full py-20 text-center text-gray-400 bg-white dark:bg-gray-800 border-2 border-dashed border-gray-200 dark:border-gray-700 rounded-3xl">
        {{ t('recipes.empty') }}
      </div>
    </div>

    <!-- Recipe Modal -->
    <AppModal 
      :show="isModalOpen" 
      :title="editingRecipe ? t('common.edit') : t('recipes.createBtn')" 
      @close="closeModal"
    >
      <form @submit.prevent="isCreateIngredientOpen ? saveNewIngredient() : saveRecipe()" class="space-y-6">
        <template v-if="!isCreateIngredientOpen">
          <div>
            <label class="block text-xs font-black text-gray-400 uppercase tracking-widest mb-2">{{ t('recipes.form.name') }}</label>
            <input v-model="form.name" type="text" required class="block w-full rounded-xl border-gray-200 dark:border-gray-700 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm bg-gray-50 dark:bg-gray-900 p-3" />
          </div>

          <!-- Components -->
          <div>
            <div class="flex justify-between items-center mb-4">
              <h4 class="text-xs font-black text-gray-400 uppercase tracking-widest">{{ t('recipes.form.components') }}</h4>
              <button type="button" @click="addComponent" class="text-xs bg-primary-50 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 px-3 py-1.5 rounded-lg font-black hover:bg-primary-100 transition-all flex items-center uppercase tracking-tighter">
                <PlusIcon class="w-4 h-4 mr-1" /> {{ t('recipes.form.addComponent') }}
              </button>
            </div>

            <div v-if="form.components.length > 0" class="mb-3">
              <div class="flex items-center gap-3 mb-2">
                <label class="text-xs font-black text-gray-400 uppercase tracking-widest shrink-0">{{ t('recipes.form.totalWeight') }}</label>
                <input v-model.number="totalWeight" type="number" step="0.01" min="0" class="w-24 text-sm p-2 border border-gray-200 dark:border-gray-700 rounded-xl bg-white dark:bg-gray-800 font-bold text-center" />
                <span class="text-xs font-black text-gray-400 uppercase">kg</span>
              </div>
              <div class="h-2 bg-gray-100 dark:bg-gray-800 rounded-full overflow-hidden">
                <div class="h-full rounded-full transition-all duration-300" :style="{ width: Math.min(pctSum, 100) + '%' }" :class="pctSum > 100.1 ? 'bg-red-500' : 'bg-primary-500'" />
              </div>
              <p class="mt-1 text-[10px] font-bold text-gray-400 uppercase tracking-wider flex justify-between">
                <span>{{ fmtQty(totalWeight, 'kg') }}</span>
                <span :class="pctSum > 100.1 ? 'text-red-500' : 'text-primary-500'">{{ pctSum.toFixed(1) }}%</span>
              </p>
            </div>
            
            <div v-if="!isExpertMode && form.components.length > 0" class="mb-3 p-3 bg-amber-50 dark:bg-amber-900/20 rounded-xl border border-amber-200 dark:border-amber-800">
              <p class="text-xs font-medium text-amber-700 dark:text-amber-300">
                Inserisci le quantità nel loro formato naturale (kg, g, L, ml). Le percentuali vengono calcolate automaticamente in base al peso totale.
              </p>
            </div>

            <div class="space-y-3 max-h-96 overflow-y-auto pr-2 custom-scrollbar">
              <div v-for="(comp, index) in form.components" :key="index" class="p-4 bg-gray-50 dark:bg-gray-900/50 rounded-2xl border border-gray-100 dark:border-gray-700 space-y-2">
                <div class="flex bg-gray-200/50 dark:bg-gray-800 rounded-lg p-0.5 w-fit border border-gray-200 dark:border-gray-700">
                  <button type="button" @click="setComponentType(comp, 'ingredient')" class="px-2.5 py-1 rounded-md text-[10px] font-black uppercase tracking-wider whitespace-nowrap transition-all" :class="getComponentType(comp) === 'ingredient' ? 'bg-white dark:bg-gray-700 text-primary-600 dark:text-primary-400 shadow-sm' : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200'">
                    {{ t('recipes.form.ingredient') }}
                  </button>
                  <button type="button" @click="setComponentType(comp, 'sub_recipe')" class="px-2.5 py-1 rounded-md text-[10px] font-black uppercase tracking-wider whitespace-nowrap transition-all" :class="getComponentType(comp) === 'sub_recipe' ? 'bg-white dark:bg-gray-700 text-primary-600 dark:text-primary-400 shadow-sm' : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200'">
                    {{ t('recipes.form.subRecipe') }}
                  </button>
                </div>
                <ComboBox
                  v-if="getComponentType(comp) === 'ingredient'"
                  v-model="comp.ingredient"
                  :options="ingredients"
                  :placeholder="t('recipes.form.selectIngredient')"
                  :allow-create="true"
                  no-results-label="Nessun risultato"
                  clear-label="Annulla selezione"
                  :create-label="t('ingredients.addBtn')"
                  @create="openCreateIngredient(index)"
                />
                <ComboBox
                  v-else
                  v-model="comp.sub_recipe"
                  :options="recipes.filter(r => r.id !== editingRecipe?.id)"
                  :placeholder="t('recipes.form.selectRecipe')"
                  no-results-label="Nessun risultato"
                />
                <template v-if="isExpertMode">
                  <div class="flex items-center gap-2">
                    <input v-model.number="comp.value" type="number" step="0.01" min="0" class="w-20 text-sm p-2 border border-gray-200 dark:border-gray-700 rounded-xl bg-white dark:bg-gray-800 font-bold text-right" />
                    <span class="text-xs font-black text-gray-400 mr-2">%</span>
                    <span class="text-xs font-bold text-primary-600 dark:text-primary-400 whitespace-nowrap">→ {{ getComponentAbs(comp) }}</span>
                    <button @click="removeComponent(index)" type="button" class="text-red-500 hover:text-red-700 p-1.5 hover:bg-red-50 dark:hover:bg-red-900/30 rounded-xl transition-all shrink-0 ml-auto">
                      <TrashIcon class="w-5 h-5" />
                    </button>
                  </div>
                </template>
                <template v-else>
                  <div class="flex items-center gap-2">
                    <input v-model.number="componentRaw[index].qty" type="number" step="0.01" min="0" class="flex-1 min-w-0 text-sm p-2 border border-gray-200 dark:border-gray-700 rounded-xl bg-white dark:bg-gray-800 font-bold" />
                    <select v-model="componentRaw[index].unit" class="w-16 shrink-0 text-sm p-2 border border-gray-200 dark:border-gray-700 rounded-xl bg-white dark:bg-gray-800 font-bold">
                      <option value="kg">kg</option>
                      <option value="g">g</option>
                      <option value="L">L</option>
                      <option value="ml">ml</option>
                      <option value="pcs">pcs</option>
                    </select>
                    <span class="text-xs font-bold text-primary-600 dark:text-primary-400 whitespace-nowrap w-14 text-right">{{ (comp.value || 0).toFixed(1) }}%</span>
                    <button @click="removeComponent(index)" type="button" class="text-red-500 hover:text-red-700 p-1.5 hover:bg-red-50 dark:hover:bg-red-900/30 rounded-xl transition-all shrink-0">
                      <TrashIcon class="w-5 h-5" />
                    </button>
                  </div>
                </template>
              </div>
              <div v-if="form.components.length === 0" class="text-center py-10 text-gray-400 italic bg-gray-50/50 dark:bg-gray-900/30 rounded-2xl border-2 border-dashed border-gray-200 dark:border-gray-700">
                {{ t('recipes.form.noComponents') }}
              </div>

              <div v-if="form.components.length > 0" class="flex justify-center pt-1">
                <button type="button" @click="toggleInputMode" class="text-xs font-bold text-primary-600 dark:text-primary-400 hover:text-primary-800 transition-colors flex items-center gap-1.5 bg-primary-50 dark:bg-primary-900/20 px-3 py-1.5 rounded-lg">
                  <span class="text-sm">&#x21BB;</span>
                  {{ isExpertMode ? 'Passa a input quantità' : 'Passa a input percentuale' }}
                </button>
              </div>
            </div>
          </div>

          <div>
            <label class="block text-xs font-black text-gray-400 uppercase tracking-widest mb-2">{{ t('recipes.form.instructions') }}</label>
            <textarea v-model="form.instructions" rows="4" class="block w-full rounded-xl border-gray-200 dark:border-gray-700 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm bg-gray-50 dark:bg-gray-900 p-3"></textarea>
          </div>
        </template>

        <template v-else>
          <div>
            <label class="block text-xs font-black text-gray-400 uppercase tracking-widest mb-2">{{ t('ingredients.form.name') }}</label>
            <input v-model="createForm.name" type="text" required class="block w-full rounded-xl border-gray-200 dark:border-gray-700 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm bg-gray-50 dark:bg-gray-900 p-3" />
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-black text-gray-400 uppercase tracking-widest mb-2">{{ t('ingredients.form.unit') }}</label>
              <select v-model="createForm.unit" class="block w-full rounded-xl border-gray-200 dark:border-gray-700 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm bg-gray-50 dark:bg-gray-900 p-3 font-bold">
                <option value="kg">kg</option>
                <option value="g">g</option>
                <option value="L">L</option>
                <option value="ml">ml</option>
                <option value="pcs">pcs</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-black text-gray-400 uppercase tracking-widest mb-2">{{ t('ingredients.form.category') }}</label>
              <input v-model="createForm.category" type="text" class="block w-full rounded-xl border-gray-200 dark:border-gray-700 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm bg-gray-50 dark:bg-gray-900 p-3" />
            </div>
          </div>
        </template>

        <template v-if="!isCreateIngredientOpen">
          <div class="flex flex-col sm:flex-row justify-end gap-3 pt-2">
            <button type="button" @click="closeModal" class="px-6 py-3 border border-gray-200 dark:border-gray-700 rounded-xl text-sm font-bold text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
              {{ t('common.cancel') }}
            </button>
            <button type="submit" :disabled="!formDirty || isLoading" class="px-6 py-3 bg-primary-600 text-white rounded-xl text-sm font-bold hover:bg-primary-700 disabled:opacity-50 shadow-lg shadow-primary-500/20">
              {{ isLoading ? '...' : t('common.save') }}
            </button>
          </div>
        </template>
        <template v-else>
          <div class="flex flex-col sm:flex-row justify-end gap-3 pt-2">
            <button type="button" @click="cancelCreateIngredient" class="px-6 py-3 border border-gray-200 dark:border-gray-700 rounded-xl text-sm font-bold text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
              {{ t('common.cancel') }}
            </button>
            <button type="submit" :disabled="isLoading" class="px-6 py-3 bg-primary-600 text-white rounded-xl text-sm font-bold hover:bg-primary-700 disabled:opacity-50 shadow-lg shadow-primary-500/20">
              {{ isLoading ? '...' : t('common.save') }}
            </button>
          </div>
        </template>
      </form>
    </AppModal>

    <!-- Calculation Modal -->
    <AppModal 
      :show="isCalcModalOpen" 
      :title="t('recipes.actions.calculate')" 
      @close="isCalcModalOpen = false"
    >
      <div v-if="selectedRecipeForCalc">
        <h4 class="text-2xl font-black text-gray-900 dark:text-white mb-6">{{ selectedRecipeForCalc.name }}</h4>
        
        <div class="flex flex-col sm:flex-row items-end gap-4 mb-8">
          <div class="flex-1 w-full">
            <label class="block text-xs font-black text-gray-400 uppercase tracking-widest mb-2">Target Quantity (kg)</label>
            <div class="relative">
              <input v-model="calcQty" type="number" step="0.01" class="block w-full p-4 border border-gray-200 dark:border-gray-700 rounded-2xl bg-gray-50 dark:bg-gray-900 font-black text-xl text-primary-600" />
              <div class="absolute right-4 top-1/2 -translate-y-1/2 font-black text-gray-400 uppercase">kg</div>
            </div>
          </div>
          <button @click="runCalculation" :disabled="isLoading" class="w-full sm:w-auto bg-gray-900 dark:bg-primary-600 text-white px-8 py-4 rounded-2xl font-black hover:bg-primary-700 transition-all flex items-center justify-center shadow-xl active:scale-95">
            <CalculatorIcon class="w-6 h-6 mr-2" /> {{ isLoading ? '...' : t('recipes.actions.calculate') }}
          </button>
        </div>

        <div v-if="calcResults" class="bg-gray-900 dark:bg-black/50 p-6 rounded-3xl font-mono text-sm max-h-96 overflow-y-auto custom-scrollbar border border-gray-800 shadow-inner">
          <div class="flex items-center space-x-2 mb-4">
             <div class="h-2 w-2 rounded-full bg-green-500 animate-pulse"></div>
             <h5 class="text-xs font-black text-gray-500 uppercase tracking-widest">INGREDIENTS</h5>
          </div>
          <div class="space-y-2">
            <div v-for="ing in calcResults.ingredients" :key="ing.name" class="flex justify-between items-center group">
              <span class="text-gray-400 group-hover:text-white transition-colors">{{ ing.name }}</span>
              <div class="flex-1 border-b border-gray-800 mx-4 border-dotted"></div>
              <span class="text-green-400 font-bold whitespace-nowrap">{{ fmtQty(ing.qty, ing.unit) }}</span>
            </div>
          </div>
          
          <div v-if="calcResults.sub_recipes && calcResults.sub_recipes.length > 0">
            <div class="flex items-center space-x-2 mt-8 mb-4">
               <div class="h-2 w-2 rounded-full bg-primary-500 animate-pulse"></div>
               <h5 class="text-xs font-black text-gray-500 uppercase tracking-widest">SUB-RECIPES</h5>
            </div>
            <div v-for="sub in calcResults.sub_recipes" :key="sub.recipe_name" class="mb-6 bg-gray-800/50 p-4 rounded-2xl border border-gray-700">
              <div class="flex justify-between font-black text-white mb-3">
                <span>{{ sub.recipe_name }}</span>
                <span class="text-primary-400">{{ fmtQty(sub.target_qty, sub.target_unit) }}</span>
              </div>
              <div class="space-y-1">
                <div v-for="ing in sub.ingredients" :key="ing.name" class="pl-4 text-xs flex justify-between">
                  <span class="text-gray-500">{{ ing.name }}</span>
                  <span class="text-gray-300">{{ fmtQty(ing.qty, ing.unit) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </AppModal>
  </div>
</template>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #e5e7eb;
  border-radius: 9999px;
}
:root.dark .custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #374151;
}
</style>
