<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { onMounted, ref } from 'vue';
import { 
  LayoutDashboard, 
  ShoppingBasket, 
  ChefHat, 
  ClipboardList,
  Languages,
  Moon,
  Sun
} from 'lucide-vue-next';

const { locale, t } = useI18n();
const isDark = ref(false);

const toggleLanguage = () => {
  locale.value = locale.value === 'en' ? 'it' : 'en';
};

const toggleDarkMode = () => {
  isDark.value = !isDark.value;
  if (isDark.value) {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
};

onMounted(() => {
  // Check system preference or default
  if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
    isDark.value = true;
    document.documentElement.classList.add('dark');
  }
});
</script>

<template>
  <div class="flex h-screen bg-gray-100 dark:bg-gray-900 transition-colors duration-200">
    <!-- Sidebar -->
    <aside class="w-20 md:w-64 bg-white dark:bg-gray-800 shadow-xl border-r border-gray-200 dark:border-gray-700 flex flex-col z-20 transition-all duration-300">
      <div class="p-4 md:p-6 overflow-hidden">
        <h1 class="text-xl md:text-2xl font-black text-primary-600 truncate">Bakery Flow</h1>
        <p class="hidden md:block text-[10px] text-gray-500 dark:text-gray-400 uppercase tracking-widest mt-1 font-bold">Production Manager</p>
      </div>
      
      <nav class="mt-6 px-2 md:px-4 space-y-2 flex-1">
        <RouterLink 
          to="/" 
          class="flex items-center justify-center md:justify-start px-3 py-3 text-gray-700 dark:text-gray-300 rounded-xl hover:bg-primary-50 dark:hover:bg-primary-900/30 hover:text-primary-600 dark:hover:text-primary-400 transition-all"
          active-class="bg-primary-50 dark:bg-primary-900/40 text-primary-600 dark:text-primary-400 font-bold shadow-sm"
        >
          <LayoutDashboard class="w-6 h-6 md:mr-3 shrink-0" />
          <span class="hidden md:block">{{ t('nav.dashboard') }}</span>
        </RouterLink>

        <RouterLink 
          to="/ingredients" 
          class="flex items-center justify-center md:justify-start px-3 py-3 text-gray-700 dark:text-gray-300 rounded-xl hover:bg-primary-50 dark:hover:bg-primary-900/30 hover:text-primary-600 dark:hover:text-primary-400 transition-all"
          active-class="bg-primary-50 dark:bg-primary-900/40 text-primary-600 dark:text-primary-400 font-bold shadow-sm"
        >
          <ShoppingBasket class="w-6 h-6 md:mr-3 shrink-0" />
          <span class="hidden md:block">{{ t('nav.ingredients') }}</span>
        </RouterLink>

        <RouterLink 
          to="/recipes" 
          class="flex items-center justify-center md:justify-start px-3 py-3 text-gray-700 dark:text-gray-300 rounded-xl hover:bg-primary-50 dark:hover:bg-primary-900/30 hover:text-primary-600 dark:hover:text-primary-400 transition-all"
          active-class="bg-primary-50 dark:bg-primary-900/40 text-primary-600 dark:text-primary-400 font-bold shadow-sm"
        >
          <ChefHat class="w-6 h-6 md:mr-3 shrink-0" />
          <span class="hidden md:block">{{ t('nav.recipes') }}</span>
        </RouterLink>

        <RouterLink 
          to="/production" 
          class="flex items-center justify-center md:justify-start px-3 py-3 text-gray-700 dark:text-gray-300 rounded-xl hover:bg-primary-50 dark:hover:bg-primary-900/30 hover:text-primary-600 dark:hover:text-primary-400 transition-all"
          active-class="bg-primary-50 dark:bg-primary-900/40 text-primary-600 dark:text-primary-400 font-bold shadow-sm"
        >
          <ClipboardList class="w-6 h-6 md:mr-3 shrink-0" />
          <span class="hidden md:block">{{ t('nav.production') }}</span>
        </RouterLink>
      </nav>

      <!-- Bottom Controls -->
      <div class="p-2 md:p-4 border-t border-gray-100 dark:border-gray-700 space-y-1">
        <button 
          @click="toggleDarkMode"
          class="flex items-center justify-center md:justify-start w-full px-3 py-2 text-sm text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
        >
          <component :is="isDark ? Sun : Moon" class="w-5 h-5 md:mr-3" />
          <span class="hidden md:block">{{ isDark ? 'Light' : 'Dark' }}</span>
        </button>

        <button 
          @click="toggleLanguage"
          class="flex items-center justify-center md:justify-start w-full px-3 py-2 text-sm text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
        >
          <Languages class="w-5 h-5 md:mr-3" />
          <span class="hidden md:block uppercase font-black">{{ locale }}</span>
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 overflow-y-auto p-4 md:p-8 text-gray-900 dark:text-gray-100">
      <div class="max-w-7xl mx-auto">
        <RouterView />
      </div>
    </main>
  </div>
</template>

<style>
/* Base overrides for better contrast and feel */
body {
  @apply antialiased text-gray-900 dark:text-gray-100 bg-gray-100 dark:bg-gray-900;
}
</style>
