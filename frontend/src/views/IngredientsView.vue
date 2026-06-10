<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useI18n } from 'vue-i18n';
import api from '../api';

const { t } = useI18n();
const ingredients = ref<any[]>([]);

onMounted(async () => {
  try {
    const response = await api.get('ingredients/');
    ingredients.value = response.data;
  } catch (error) {
    console.error('Error fetching ingredients:', error);
  }
});
</script>

<template>
  <div>
    <div class="flex justify-between items-center">
      <div>
        <h2 class="text-3xl font-bold text-gray-800">{{ t('ingredients.title') }}</h2>
        <p class="mt-2 text-gray-600">{{ t('ingredients.subtitle') }}</p>
      </div>
      <button class="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors">
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
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ ing.unit }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ ing.category || '-' }}</td>
            <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
              <button class="text-primary-600 hover:text-primary-900 mr-4">{{ t('common.edit') }}</button>
              <button class="text-red-600 hover:text-red-900">{{ t('common.delete') }}</button>
            </td>
          </tr>
          <tr v-if="ingredients.length === 0">
            <td colspan="4" class="px-6 py-12 text-center text-gray-500">
              {{ t('ingredients.empty') }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
