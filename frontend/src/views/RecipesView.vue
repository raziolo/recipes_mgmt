<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue';
import { useI18n } from 'vue-i18n';
import api from '../api';
import AppModal from '../components/AppModal.vue';
import type { Recipe, Ingredient } from '../types';
import { PlusIcon, TrashIcon, CalculatorIcon, PencilSquareIcon } from '@heroicons/vue/24/outline';

const { t } = useI18n();
const recipes = ref<Recipe[]>([]);
const ingredients = ref<Ingredient[]>([]);
const isModalOpen = ref(false);
const isCalcModalOpen = ref(false);
const editingRecipe = ref<Recipe | null>(null);
const isLoading = ref(false);

const selectedRecipeForCalc = ref<Recipe | null>(null);
const calcQty = ref(1);
const calcResults = ref<any>(null);

const form = ref<Recipe>({
  name: '',
  calc_method: 'YIELD',
  base_yield_qty: 1,
  base_yield_unit: 'kg',
  instructions: '',
  notes: '',
  components: []
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

const openModal = async (recipe: Recipe | null = null) => {
  if (recipe) {
    editingRecipe.value = { ...recipe };
    form.value = JSON.parse(JSON.stringify(recipe));
  } else {
    editingRecipe.value = null;
    form.value = {
      name: '',
      calc_method: 'YIELD',
      base_yield_qty: 1,
      base_yield_unit: 'kg',
      instructions: '',
      notes: '',
      components: []
    };
  }
  await nextTick();
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
  editingRecipe.value = null;
};

const addComponent = () => {
  form.value.components.push({
    value: 0,
    unit: ''
  });
};

const removeComponent = (index: number) => {
  form.value.components.splice(index, 1);
};

const saveRecipe = async () => {
  isLoading.value = true;
  try {
    if (editingRecipe.value?.id) {
      await api.put(`recipes/${editingRecipe.value.id}/`, form.value);
    } else {
      await api.post('recipes/', form.value);
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
  calcQty.value = Number(recipe.base_yield_qty);
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

const getMethodLabel = (method: string) => {
  return method === 'YIELD' ? t('recipes.methods.yield') : t('recipes.methods.percentage');
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
            <PencilSquareIcon class="w-5 h-5 text-gray-400 opacity-0 group-hover:opacity-100 transition-opacity" />
          </div>
          <div class="mt-2 flex flex-wrap gap-2">
            <span class="text-[10px] px-2 py-1 rounded-lg bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 uppercase font-black tracking-widest">
              {{ getMethodLabel(recipe.calc_method) }}
            </span>
            <span class="text-[10px] px-2 py-1 rounded-lg bg-blue-50 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 font-black tracking-widest uppercase">
              {{ recipe.base_yield_qty }} {{ recipe.base_yield_unit }}
            </span>
          </div>
          <p class="mt-4 text-sm text-gray-500 dark:text-gray-400 line-clamp-3 h-15 overflow-hidden font-medium">
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
      <form @submit.prevent="saveRecipe" class="space-y-6">
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div class="sm:col-span-2">
            <label class="block text-xs font-black text-gray-400 uppercase tracking-widest mb-2">{{ t('recipes.form.name') }}</label>
            <input v-model="form.name" type="text" required class="block w-full rounded-xl border-gray-200 dark:border-gray-700 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm bg-gray-50 dark:bg-gray-900 p-3" />
          </div>
          
          <div>
            <label class="block text-xs font-black text-gray-400 uppercase tracking-widest mb-2">{{ t('recipes.form.method') }}</label>
            <select v-model="form.calc_method" class="block w-full rounded-xl border-gray-200 dark:border-gray-700 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm bg-gray-50 dark:bg-gray-900 p-3 font-bold">
              <option value="YIELD">{{ t('recipes.methods.yield') }}</option>
              <option value="PERCENTAGE">{{ t('recipes.methods.percentage') }}</option>
            </select>
          </div>
          
          <div v-if="form.calc_method === 'YIELD'" class="flex space-x-2">
            <div class="w-1/2">
              <label class="block text-xs font-black text-gray-400 uppercase tracking-widest mb-2">{{ t('recipes.form.baseQty') }}</label>
              <input v-model="form.base_yield_qty" type="number" step="0.001" class="block w-full rounded-xl border-gray-200 dark:border-gray-700 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm bg-gray-50 dark:bg-gray-900 p-3" />
            </div>
            <div class="w-1/2">
              <label class="block text-xs font-black text-gray-400 uppercase tracking-widest mb-2">{{ t('recipes.form.baseUnit') }}</label>
              <input v-model="form.base_yield_unit" type="text" class="block w-full rounded-xl border-gray-200 dark:border-gray-700 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm bg-gray-50 dark:bg-gray-900 p-3" />
            </div>
          </div>
        </div>

        <!-- Components -->
        <div class="mt-8">
          <div class="flex justify-between items-center mb-4">
            <h4 class="text-xs font-black text-gray-400 uppercase tracking-widest">{{ t('recipes.form.components') }}</h4>
            <button type="button" @click="addComponent" class="text-xs bg-primary-50 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 px-3 py-1.5 rounded-lg font-black hover:bg-primary-100 transition-all flex items-center uppercase tracking-tighter">
              <PlusIcon class="w-4 h-4 mr-1" /> {{ t('recipes.form.addComponent') }}
            </button>
          </div>
          
          <div class="space-y-3 max-h-72 overflow-y-auto pr-2 custom-scrollbar">
            <div v-for="(comp, index) in form.components" :key="index" class="flex flex-col sm:flex-row items-start sm:items-center gap-3 p-4 bg-gray-50 dark:bg-gray-900/50 rounded-2xl border border-gray-100 dark:border-gray-700 relative">
              <div class="flex-1 w-full grid grid-cols-1 sm:grid-cols-2 gap-3">
                <select v-model="comp.ingredient" class="text-sm p-2.5 border border-gray-200 dark:border-gray-700 rounded-xl bg-white dark:bg-gray-800 font-bold">
                  <option :value="undefined">{{ t('recipes.form.selectIngredient') }}</option>
                  <option v-for="ing in ingredients" :key="ing.id" :value="ing.id">{{ ing.name }}</option>
                </select>
                <select v-model="comp.sub_recipe" class="text-sm p-2.5 border border-gray-200 dark:border-gray-700 rounded-xl bg-white dark:bg-gray-800 font-bold">
                  <option :value="undefined">{{ t('recipes.form.selectRecipe') }}</option>
                  <option v-for="r in recipes" :key="r.id" :value="r.id" :disabled="r.id === editingRecipe?.id">{{ r.name }}</option>
                </select>
              </div>
              <div class="flex items-center space-x-2 w-full sm:w-auto">
                <input v-model="comp.value" type="number" step="0.001" :placeholder="t('recipes.form.value')" class="w-full sm:w-20 text-sm p-2.5 border border-gray-200 dark:border-gray-700 rounded-xl bg-white dark:bg-gray-800 font-bold" />
                <input v-model="comp.unit" type="text" :placeholder="t('recipes.form.unit')" class="w-full sm:w-16 text-sm p-2.5 border border-gray-200 dark:border-gray-700 rounded-xl bg-white dark:bg-gray-800 font-bold" />
                <button @click="removeComponent(index)" type="button" class="text-red-500 hover:text-red-700 p-2 hover:bg-red-50 dark:hover:bg-red-900/30 rounded-xl transition-all">
                  <TrashIcon class="w-5 h-5" />
                </button>
              </div>
            </div>
          </div>
        </div>

        <div>
          <label class="block text-xs font-black text-gray-400 uppercase tracking-widest mb-2">{{ t('recipes.form.instructions') }}</label>
          <textarea v-model="form.instructions" rows="4" class="block w-full rounded-xl border-gray-200 dark:border-gray-700 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm bg-gray-50 dark:bg-gray-900 p-3"></textarea>
        </div>

        <div class="mt-8 flex flex-col sm:flex-row justify-end gap-3">
          <button type="button" @click="closeModal" class="px-6 py-3 border border-gray-200 dark:border-gray-700 rounded-xl text-sm font-bold text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
            {{ t('common.cancel') }}
          </button>
          <button type="submit" :disabled="isLoading" class="px-6 py-3 bg-primary-600 text-white rounded-xl text-sm font-bold hover:bg-primary-700 disabled:opacity-50 shadow-lg shadow-primary-500/20">
            {{ isLoading ? '...' : t('common.save') }}
          </button>
        </div>
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
            <label class="block text-xs font-black text-gray-400 uppercase tracking-widest mb-2">{{ t('recipes.form.baseQty') }}</label>
            <div class="relative">
              <input v-model="calcQty" type="number" step="0.001" class="block w-full p-4 border border-gray-200 dark:border-gray-700 rounded-2xl bg-gray-50 dark:bg-gray-900 font-black text-xl text-primary-600" />
              <div class="absolute right-4 top-1/2 -translate-y-1/2 font-black text-gray-400 uppercase">{{ selectedRecipeForCalc.base_yield_unit }}</div>
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
              <span class="text-green-400 font-bold whitespace-nowrap">{{ ing.qty.toFixed(3) }} <span class="text-[10px] text-gray-600 uppercase">{{ ing.unit }}</span></span>
            </div>
          </div>
          
          <div v-if="calcResults.sub_recipes && calcResults.sub_recipes.length > 0">
            <div class="flex items-center space-x-2 mt-8 mb-4">
               <div class="h-2 w-2 rounded-full bg-blue-500 animate-pulse"></div>
               <h5 class="text-xs font-black text-gray-500 uppercase tracking-widest">SUB-RECIPES</h5>
            </div>
            <div v-for="sub in calcResults.sub_recipes" :key="sub.recipe_name" class="mb-6 bg-gray-800/50 p-4 rounded-2xl border border-gray-700">
              <div class="flex justify-between font-black text-white mb-3">
                <span>{{ sub.recipe_name }}</span>
                <span class="text-blue-400">{{ sub.target_qty.toFixed(3) }} <span class="text-[10px] text-gray-500">{{ sub.target_unit }}</span></span>
              </div>
              <div class="space-y-1">
                <div v-for="ing in sub.ingredients" :key="ing.name" class="pl-4 text-xs flex justify-between">
                  <span class="text-gray-500">{{ ing.name }}</span>
                  <span class="text-gray-300">{{ ing.qty.toFixed(3) }} {{ ing.unit }}</span>
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
