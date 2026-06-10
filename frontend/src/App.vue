<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { 
  LayoutDashboard, 
  ShoppingBasket, 
  ChefHat, 
  ClipboardList,
  Languages
} from 'lucide-vue-next';

const { locale, t } = useI18n();

const toggleLanguage = () => {
  locale.value = locale.value === 'en' ? 'it' : 'en';
};
</script>

<template>
  <div class="flex h-screen bg-gray-100">
    <!-- Sidebar -->
    <aside class="w-64 bg-white shadow-md border-r flex flex-col">
      <div class="p-6">
        <h1 class="text-2xl font-bold text-primary-600">Bakery Flow</h1>
        <p class="text-xs text-gray-500 uppercase tracking-wider mt-1">Production Manager</p>
      </div>
      
      <nav class="mt-6 px-4 space-y-1 flex-1">
        <RouterLink 
          to="/" 
          class="flex items-center px-4 py-3 text-gray-700 rounded-lg hover:bg-primary-50 hover:text-primary-600 transition-colors"
          active-class="bg-primary-50 text-primary-600 font-medium"
        >
          <LayoutDashboard class="w-5 h-5 mr-3" />
          {{ t('nav.dashboard') }}
        </RouterLink>

        <RouterLink 
          to="/ingredients" 
          class="flex items-center px-4 py-3 text-gray-700 rounded-lg hover:bg-primary-50 hover:text-primary-600 transition-colors"
          active-class="bg-primary-50 text-primary-600 font-medium"
        >
          <ShoppingBasket class="w-5 h-5 mr-3" />
          {{ t('nav.ingredients') }}
        </RouterLink>

        <RouterLink 
          to="/recipes" 
          class="flex items-center px-4 py-3 text-gray-700 rounded-lg hover:bg-primary-50 hover:text-primary-600 transition-colors"
          active-class="bg-primary-50 text-primary-600 font-medium"
        >
          <ChefHat class="w-5 h-5 mr-3" />
          {{ t('nav.recipes') }}
        </RouterLink>

        <RouterLink 
          to="/production" 
          class="flex items-center px-4 py-3 text-gray-700 rounded-lg hover:bg-primary-50 hover:text-primary-600 transition-colors"
          active-class="bg-primary-50 text-primary-600 font-medium"
        >
          <ClipboardList class="w-5 h-5 mr-3" />
          {{ t('nav.production') }}
        </RouterLink>
      </nav>

      <!-- Language Toggle -->
      <div class="p-4 border-t">
        <button 
          @click="toggleLanguage"
          class="flex items-center w-full px-4 py-2 text-sm text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <Languages class="w-4 h-4 mr-3" />
          <span class="flex-1 text-left uppercase font-bold">{{ locale }}</span>
          <span class="text-xs text-gray-400">Switch</span>
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 overflow-y-auto p-8 text-gray-900">
      <RouterView />
    </main>
  </div>
</template>

<style>
/* Ensure dark mode colors are handled or forced light */
:root {
  background-color: #f3f4f6;
  color: #111827;
}
</style>
