<script setup lang="ts">
import { ref, onMounted } from 'vue';
import api from '../api';

const recipes = ref<any[]>([]);

onMounted(async () => {
  try {
    const response = await api.get('recipes/');
    recipes.value = response.data;
  } catch (error) {
    console.error('Error fetching recipes:', error);
  }
});
</script>

<template>
  <div>
    <div class="flex justify-between items-center">
      <div>
        <h2 class="text-3xl font-bold text-gray-800">Recipes</h2>
        <p class="mt-2 text-gray-600">Define base recipes and mix percentages.</p>
      </div>
      <button class="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors">
        Create Recipe
      </button>
    </div>

    <div class="mt-8 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="recipe in recipes" :key="recipe.id" class="bg-white p-6 rounded-xl shadow-sm border hover:border-primary-300 transition-all cursor-pointer">
        <h3 class="text-xl font-bold text-gray-900">{{ recipe.name }}</h3>
        <div class="mt-2 flex items-center space-x-2">
          <span class="text-xs px-2 py-1 rounded bg-gray-100 text-gray-600 uppercase font-medium">
            {{ recipe.calc_method }}
          </span>
          <span class="text-xs px-2 py-1 rounded bg-blue-50 text-blue-600 font-medium">
            {{ recipe.base_yield_qty }} {{ recipe.base_yield_unit }}
          </span>
        </div>
        <p class="mt-4 text-sm text-gray-500 line-clamp-2">
          {{ recipe.instructions || 'No instructions provided.' }}
        </p>
        <div class="mt-6 flex justify-end space-x-3">
          <button class="text-sm font-medium text-primary-600 hover:text-primary-800">Calculate</button>
          <button class="text-sm font-medium text-gray-600 hover:text-gray-800">Edit</button>
        </div>
      </div>
      
      <div v-if="recipes.length === 0" class="col-span-full py-12 text-center text-gray-500 bg-white border-2 border-dashed rounded-xl">
        No recipes found. Create your first recipe to get started.
      </div>
    </div>
  </div>
</template>
