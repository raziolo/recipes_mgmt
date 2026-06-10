<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router';
import { 
  LayoutDashboard, 
  ShoppingBasket, 
  ChefHat, 
  ClipboardList 
} from 'lucide-vue-next';
</script>

<template>
  <div class="flex h-screen bg-gray-100">
    <!-- Sidebar -->
    <aside class="w-64 bg-white shadow-md border-r">
      <div class="p-6">
        <h1 class="text-2xl font-bold text-primary-600">Bakery Flow</h1>
        <p class="text-xs text-gray-500 uppercase tracking-wider mt-1">Production Manager</p>
      </div>
      
      <nav class="mt-6 px-4 space-y-1">
        <RouterLink 
          to="/" 
          class="flex items-center px-4 py-3 text-gray-700 rounded-lg hover:bg-primary-50 hover:text-primary-600 transition-colors"
          active-class="bg-primary-50 text-primary-600 font-medium"
        >
          <LayoutDashboard class="w-5 h-5 mr-3" />
          Dashboard
        </RouterLink>

        <RouterLink 
          to="/ingredients" 
          class="flex items-center px-4 py-3 text-gray-700 rounded-lg hover:bg-primary-50 hover:text-primary-600 transition-colors"
          active-class="bg-primary-50 text-primary-600 font-medium"
        >
          <ShoppingBasket class="w-5 h-5 mr-3" />
          Ingredients
        </RouterLink>

        <RouterLink 
          to="/recipes" 
          class="flex items-center px-4 py-3 text-gray-700 rounded-lg hover:bg-primary-50 hover:text-primary-600 transition-colors"
          active-class="bg-primary-50 text-primary-600 font-medium"
        >
          <ChefHat class="w-5 h-5 mr-3" />
          Recipes
        </RouterLink>

        <RouterLink 
          to="/production" 
          class="flex items-center px-4 py-3 text-gray-700 rounded-lg hover:bg-primary-50 hover:text-primary-600 transition-colors"
          active-class="bg-primary-50 text-primary-600 font-medium"
        >
          <ClipboardList class="w-5 h-5 mr-3" />
          Production
        </RouterLink>
      </nav>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 overflow-y-auto p-8">
      <RouterView />
    </main>
  </div>
</template>

<style>
/* Custom primary color overrides if needed */
</style>
