<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useI18n } from 'vue-i18n';
import api from '../api';
import AppModal from '../components/AppModal.vue';
import type { Recipe, RecipeComponent, Ingredient } from '../types';
import { PlusIcon, TrashIcon, CalculatorIcon } from '@heroicons/vue/24/outline';

const { t } = useI18n();
const recipes = ref<Recipe[]>([]);
const ingredients = ref<Ingredient[]>([]);
const isModalOpen = ref(false);
const isCalcModalOpen = ref(false);
const editingRecipe = ref<Recipe | null>(null);
const isLoading = ref(false);

// Calculation related
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

const openModal = (recipe: Recipe | null = null) => {
  if (recipe) {
    editingRecipe.value = recipe;
    form.value = JSON.parse(JSON.stringify(recipe)); // Deep copy
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
    // Note: Django DRF Nested Writes might need custom logic if not using a library.
    // However, we can handle it by sending the full components list.
    // If DRF doesn't handle it out of the box (which it doesn't for Writable Nested Serializers),
    // we might need to adjust the backend. Let's assume standard behavior for now and fix if it fails.
    
    // Actually, I didn't implement Writable Nested Serializers in DRF yet. 
    // I should probably fix that in the backend first or handle it here.
    // Let's implement the frontend and then fix the backend.
    
    if (editingRecipe.value?.id) {
      await api.put(`recipes/${editingRecipe.value.id}/`, form.value);
    } else {
      await api.post('recipes/', form.value);
    }
    await fetchData();
    closeModal();
  } catch (error) {
    console.error('Error saving recipe:', error);
    alert('Failed to save recipe. Backend might need updates for nested components.');
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
  <div>
    <div class="flex justify-between items-center">
      <div>
        <h2 class="text-3xl font-bold text-gray-800">{{ t('recipes.title') }}</h2>
        <p class="mt-2 text-gray-600">{{ t('recipes.subtitle') }}</p>
      </div>
      <button @click="openModal()" class="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors shadow-sm">
        {{ t('recipes.createBtn') }}
      </button>
    </div>

    <div class="mt-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="recipe in recipes" :key="recipe.id" class="bg-white p-6 rounded-xl shadow-sm border hover:border-primary-300 transition-all">
        <div @click="openModal(recipe)" class="cursor-pointer">
          <h3 class="text-xl font-bold text-gray-900">{{ recipe.name }}</h3>
          <div class="mt-2 flex items-center space-x-2">
            <span class="text-xs px-2 py-1 rounded bg-gray-100 text-gray-600 uppercase font-bold">
              {{ getMethodLabel(recipe.calc_method) }}
            </span>
            <span class="text-xs px-2 py-1 rounded bg-blue-50 text-blue-600 font-bold uppercase">
              {{ recipe.base_yield_qty }} {{ recipe.base_yield_unit }}
            </span>
          </div>
          <p class="mt-4 text-sm text-gray-500 line-clamp-3 h-10 overflow-hidden">
            {{ recipe.instructions || 'No instructions provided.' }}
          </p>
        </div>
        
        <div class="mt-6 flex justify-between items-center pt-4 border-t">
          <div class="flex space-x-2">
            <button @click="openCalcModal(recipe)" class="p-2 text-gray-500 hover:text-primary-600 rounded-full hover:bg-primary-50">
              <CalculatorIcon class="w-5 h-5" />
            </button>
          </div>
          <div class="flex space-x-3">
            <button @click="openModal(recipe)" class="text-sm font-semibold text-primary-600 hover:text-primary-800">{{ t('common.edit') }}</button>
            <button @click="deleteRecipe(recipe.id!)" class="text-sm font-semibold text-red-600 hover:text-red-800">{{ t('common.delete') }}</button>
          </div>
        </div>
      </div>
      
      <div v-if="recipes.length === 0" class="col-span-full py-12 text-center text-gray-500 bg-white border-2 border-dashed rounded-xl">
        {{ t('recipes.empty') }}
      </div>
    </div>

    <!-- Recipe Modal -->
    <AppModal 
      :show="isModalOpen" 
      :title="editingRecipe ? t('common.edit') : t('recipes.createBtn')" 
      @close="closeModal"
    >
      <form @submit.prevent="saveRecipe" class="space-y-4">
        <div class="grid grid-cols-2 gap-4">
          <div class="col-span-2">
            <label class="block text-sm font-medium text-gray-700">Name</label>
            <input v-model="form.name" type="text" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm bg-gray-50 p-2 border" />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700">Method</label>
            <select v-model="form.calc_method" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm bg-gray-50 p-2 border">
              <option value="YIELD">Yield (Scaling)</option>
              <option value="PERCENTAGE">Percentage (Mix)</option>
            </select>
          </div>
          
          <div v-if="form.calc_method === 'YIELD'" class="flex space-x-2">
            <div class="w-1/2">
              <label class="block text-sm font-medium text-gray-700">Base Qty</label>
              <input v-model="form.base_yield_qty" type="number" step="0.001" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm bg-gray-50 p-2 border" />
            </div>
            <div class="w-1/2">
              <label class="block text-sm font-medium text-gray-700">Unit</label>
              <input v-model="form.base_yield_unit" type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm bg-gray-50 p-2 border" />
            </div>
          </div>
        </div>

        <!-- Components -->
        <div class="mt-6">
          <div class="flex justify-between items-center mb-2">
            <h4 class="text-sm font-bold text-gray-900 uppercase tracking-tight">Components</h4>
            <button type="button" @click="addComponent" class="text-xs bg-gray-100 px-2 py-1 rounded hover:bg-gray-200 flex items-center">
              <PlusIcon class="w-3 h-3 mr-1" /> Add
            </button>
          </div>
          
          <div class="space-y-2 max-h-60 overflow-y-auto pr-2">
            <div v-for="(comp, index) in form.components" :key="index" class="flex items-center space-x-2 p-2 bg-gray-50 rounded border">
              <select v-model="comp.ingredient" class="flex-1 text-xs p-1 border rounded bg-white">
                <option :value="undefined">-- Select Ingredient --</option>
                <option v-for="ing in ingredients" :key="ing.id" :value="ing.id">{{ ing.name }}</option>
              </select>
              <span class="text-xs text-gray-400">OR</span>
              <select v-model="comp.sub_recipe" class="flex-1 text-xs p-1 border rounded bg-white">
                <option :value="undefined">-- Select Recipe --</option>
                <option v-for="r in recipes" :key="r.id" :value="r.id" :disabled="r.id === editingRecipe?.id">{{ r.name }}</option>
              </select>
              <input v-model="comp.value" type="number" step="0.001" placeholder="Val" class="w-16 text-xs p-1 border rounded" />
              <input v-model="comp.unit" type="text" placeholder="Unit" class="w-12 text-xs p-1 border rounded" />
              <button @click="removeComponent(index)" type="button" class="text-red-500 hover:text-red-700">
                <TrashIcon class="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700">Instructions</label>
          <textarea v-model="form.instructions" rows="3" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm bg-gray-50 p-2 border"></textarea>
        </div>

        <div class="mt-6 flex justify-end space-x-3">
          <button type="button" @click="closeModal" class="px-4 py-2 border rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50">
            {{ t('common.cancel') }}
          </button>
          <button type="submit" :disabled="isLoading" class="px-4 py-2 bg-primary-600 text-white rounded-md text-sm font-medium hover:bg-primary-700 disabled:opacity-50">
            {{ isLoading ? '...' : t('common.save') }}
          </button>
        </div>
      </form>
    </AppModal>

    <!-- Calculation Modal -->
    <AppModal 
      :show="isCalcModalOpen" 
      title="Recipe Calculator" 
      @close="isCalcModalOpen = false"
    >
      <div v-if="selectedRecipeForCalc">
        <p class="text-sm font-bold text-gray-600 mb-4">{{ selectedRecipeForCalc.name }}</p>
        
        <div class="flex items-center space-x-4 mb-6">
          <div class="flex-1">
            <label class="block text-xs text-gray-500 uppercase font-bold">Target Quantity</label>
            <input v-model="calcQty" type="number" step="0.001" class="mt-1 block w-full p-2 border rounded bg-gray-50 font-bold" />
          </div>
          <div class="pt-4">
            <span class="text-gray-500 font-bold uppercase">{{ selectedRecipeForCalc.base_yield_unit }}</span>
          </div>
          <div class="pt-4">
            <button @click="runCalculation" :disabled="isLoading" class="bg-primary-600 text-white px-4 py-2 rounded font-bold hover:bg-primary-700 transition-colors flex items-center">
              <CalculatorIcon class="w-4 h-4 mr-2" /> {{ isLoading ? '...' : 'Calc' }}
            </button>
          </div>
        </div>

        <div v-if="calcResults" class="bg-gray-900 text-green-400 p-4 rounded font-mono text-sm max-h-80 overflow-y-auto">
          <h5 class="text-white border-b border-gray-700 pb-1 mb-2">INGREDIENTS:</h5>
          <div v-for="ing in calcResults.ingredients" :key="ing.name" class="flex justify-between">
            <span>{{ ing.name }}</span>
            <span class="text-white">{{ ing.qty.toFixed(3) }} {{ ing.unit }}</span>
          </div>
          
          <div v-if="calcResults.sub_recipes && calcResults.sub_recipes.length > 0">
            <h5 class="text-white border-b border-gray-700 pb-1 mt-4 mb-2">SUB-RECIPES:</h5>
            <div v-for="sub in calcResults.sub_recipes" :key="sub.recipe_name" class="mb-2">
              <div class="flex justify-between font-bold">
                <span>{{ sub.recipe_name }}</span>
                <span>{{ sub.target_qty.toFixed(3) }} {{ sub.target_unit }}</span>
              </div>
              <div v-for="ing in sub.ingredients" :key="ing.name" class="pl-4 text-xs opacity-80 flex justify-between">
                <span>{{ ing.name }}</span>
                <span>{{ ing.qty.toFixed(3) }} {{ ing.unit }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </AppModal>
  </div>
</template>
