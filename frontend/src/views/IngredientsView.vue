<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useI18n } from 'vue-i18n';
import api from '../api';
import AppModal from '../components/AppModal.vue';
import type { Ingredient } from '../types';

const { t } = useI18n();
const ingredients = ref<Ingredient[]>([]);
const isModalOpen = ref(false);
const editingIngredient = ref<Ingredient | null>(null);
const isLoading = ref(false);

const form = ref<Ingredient>({
  name: '',
  unit: 'kg',
  category: '',
  notes: '',
});

const fetchIngredients = async () => {
  try {
    const response = await api.get('ingredients/');
    ingredients.value = response.data;
  } catch (error) {
    console.error('Error fetching ingredients:', error);
  }
};

onMounted(fetchIngredients);

const openModal = (ingredient: Ingredient | null = null) => {
  if (ingredient) {
    editingIngredient.value = ingredient;
    form.value = { ...ingredient };
  } else {
    editingIngredient.value = null;
    form.value = { name: '', unit: 'kg', category: '', notes: '' };
  }
  isModalOpen.value = true;
};

const closeModal = () => {
  isModalOpen.value = false;
  editingIngredient.value = null;
};

const saveIngredient = async () => {
  isLoading.value = true;
  try {
    if (editingIngredient.value?.id) {
      await api.put(`ingredients/${editingIngredient.value.id}/`, form.value);
    } else {
      await api.post('ingredients/', form.value);
    }
    await fetchIngredients();
    closeModal();
  } catch (error) {
    console.error('Error saving ingredient:', error);
    alert('Failed to save ingredient. Please check the data.');
  } finally {
    isLoading.value = false;
  }
};

const deleteIngredient = async (id: number) => {
  if (!confirm(t('common.delete') + '?')) return;
  try {
    await api.delete(`ingredients/${id}/`);
    await fetchIngredients();
  } catch (error) {
    console.error('Error deleting ingredient:', error);
  }
};
</script>

<template>
  <div>
    <div class="flex justify-between items-center">
      <div>
        <h2 class="text-3xl font-bold text-gray-800">{{ t('ingredients.title') }}</h2>
        <p class="mt-2 text-gray-600">{{ t('ingredients.subtitle') }}</p>
      </div>
      <button @click="openModal()" class="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors shadow-sm">
        {{ t('ingredients.addBtn') }}
      </button>
    </div>

    <div class="mt-8 bg-white shadow-sm border rounded-xl overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ t('ingredients.table.name') }}</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ t('ingredients.table.unit') }}</th>
            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ t('ingredients.table.category') }}</th>
            <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">{{ t('ingredients.table.actions') }}</th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr v-for="ing in ingredients" :key="ing.id">
            <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ ing.name }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 uppercase">{{ ing.unit }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ ing.category || '-' }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
              <button @click="openModal(ing)" class="text-primary-600 hover:text-primary-900 mr-4 font-semibold">{{ t('common.edit') }}</button>
              <button @click="deleteIngredient(ing.id!)" class="text-red-600 hover:text-red-900 font-semibold">{{ t('common.delete') }}</button>
            </td>
          </tr>
          <tr v-if="ingredients.length === 0">
            <td colspan="4" class="px-6 py-12 text-center text-gray-500 italic">
              {{ t('ingredients.empty') }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Ingredient Modal -->
    <AppModal 
      :show="isModalOpen" 
      :title="editingIngredient ? t('common.edit') : t('ingredients.addBtn')" 
      @close="closeModal"
    >
      <form @submit.prevent="saveIngredient" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700">{{ t('ingredients.table.name') }}</label>
          <input v-model="form.name" type="text" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm bg-gray-50 p-2 border" />
        </div>
        
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">{{ t('ingredients.table.unit') }}</label>
            <select v-model="form.unit" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm bg-gray-50 p-2 border">
              <option value="kg">kg</option>
              <option value="g">g</option>
              <option value="L">L</option>
              <option value="ml">ml</option>
              <option value="pcs">pcs</option>
            </select>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">{{ t('ingredients.table.category') }}</label>
            <input v-model="form.category" type="text" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm bg-gray-50 p-2 border" />
          </div>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700">Notes</label>
          <textarea v-model="form.notes" rows="3" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm bg-gray-50 p-2 border"></textarea>
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
  </div>
</template>
