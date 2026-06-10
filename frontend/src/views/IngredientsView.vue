<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue';
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

const openModal = async (ingredient: Ingredient | null = null) => {
  if (ingredient) {
    editingIngredient.value = { ...ingredient };
    form.value = { ...ingredient };
  } else {
    editingIngredient.value = null;
    form.value = { name: '', unit: 'kg', category: '', notes: '' };
  }
  await nextTick();
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
    alert(t('common.save') + ' failed.');
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
  <div class="animate-in fade-in duration-500">
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
      <div>
        <h2 class="text-3xl font-black text-gray-900 dark:text-white">{{ t('ingredients.title') }}</h2>
        <p class="mt-1 text-gray-500 dark:text-gray-400 font-medium">{{ t('ingredients.subtitle') }}</p>
      </div>
      <button @click="openModal()" class="w-full sm:w-auto bg-primary-600 text-white px-6 py-3 rounded-2xl font-bold hover:bg-primary-700 transition-all shadow-lg shadow-primary-500/20 active:scale-95">
        {{ t('ingredients.addBtn') }}
      </button>
    </div>

    <div class="mt-8 bg-white dark:bg-gray-800 shadow-xl shadow-gray-200/50 dark:shadow-none border border-gray-100 dark:border-gray-700 rounded-3xl overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-100 dark:divide-gray-700">
          <thead class="bg-gray-50 dark:bg-gray-900/50">
            <tr>
              <th class="px-6 py-4 text-left text-[10px] font-black text-gray-400 uppercase tracking-widest">{{ t('ingredients.table.name') }}</th>
              <th class="px-6 py-4 text-left text-[10px] font-black text-gray-400 uppercase tracking-widest">{{ t('ingredients.table.unit') }}</th>
              <th class="px-6 py-4 text-left text-[10px] font-black text-gray-400 uppercase tracking-widest">{{ t('ingredients.table.category') }}</th>
              <th class="px-6 py-4 text-right text-[10px] font-black text-gray-400 uppercase tracking-widest">{{ t('ingredients.table.actions') }}</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100 dark:divide-gray-700">
            <tr v-for="ing in ingredients" :key="ing.id" class="hover:bg-gray-50 dark:hover:bg-gray-700/30 transition-colors">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-bold text-gray-900 dark:text-gray-100">{{ ing.name }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400 font-medium uppercase">{{ ing.unit }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                <span v-if="ing.category" class="bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded text-xs font-bold">{{ ing.category }}</span>
                <span v-else>-</span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-bold">
                <button @click="openModal(ing)" class="text-primary-600 dark:text-primary-400 hover:text-primary-800 mr-4">{{ t('common.edit') }}</button>
                <button @click="deleteIngredient(ing.id!)" class="text-red-600 dark:text-red-400 hover:text-red-800">{{ t('common.delete') }}</button>
              </td>
            </tr>
            <tr v-if="ingredients.length === 0">
              <td colspan="4" class="px-6 py-20 text-center text-gray-400 italic">
                {{ t('ingredients.empty') }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Ingredient Modal -->
    <AppModal 
      :show="isModalOpen" 
      :title="editingIngredient ? t('common.edit') : t('ingredients.addBtn')" 
      @close="closeModal"
    >
      <form @submit.prevent="saveIngredient" class="space-y-6">
        <div>
          <label class="block text-xs font-black text-gray-400 uppercase tracking-widest mb-2">{{ t('ingredients.form.name') }}</label>
          <input v-model="form.name" type="text" required class="block w-full rounded-xl border-gray-200 dark:border-gray-700 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm bg-gray-50 dark:bg-gray-900 p-3" />
        </div>
        
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div>
            <label class="block text-xs font-black text-gray-400 uppercase tracking-widest mb-2">{{ t('ingredients.form.unit') }}</label>
            <select v-model="form.unit" class="block w-full rounded-xl border-gray-200 dark:border-gray-700 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm bg-gray-50 dark:bg-gray-900 p-3 font-bold">
              <option value="kg">kg</option>
              <option value="g">g</option>
              <option value="L">L</option>
              <option value="ml">ml</option>
              <option value="pcs">pcs</option>
            </select>
          </div>
          <div>
            <label class="block text-xs font-black text-gray-400 uppercase tracking-widest mb-2">{{ t('ingredients.form.category') }}</label>
            <input v-model="form.category" type="text" class="block w-full rounded-xl border-gray-200 dark:border-gray-700 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm bg-gray-50 dark:bg-gray-900 p-3" />
          </div>
        </div>

        <div>
          <label class="block text-xs font-black text-gray-400 uppercase tracking-widest mb-2">{{ t('ingredients.form.notes') }}</label>
          <textarea v-model="form.notes" rows="3" class="block w-full rounded-xl border-gray-200 dark:border-gray-700 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm bg-gray-50 dark:bg-gray-900 p-3"></textarea>
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
  </div>
</template>
