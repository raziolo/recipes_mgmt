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
  if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
    isDark.value = true;
    document.documentElement.classList.add('dark');
  }
});
</script>

<template>
  <div class="flex h-screen bg-gray-100 dark:bg-slate-950 transition-colors duration-200 overflow-hidden font-sans">
    <!-- Sidebar -->
    <aside class="w-20 md:w-64 bg-white dark:bg-slate-900 shadow-2xl border-r border-gray-200 dark:border-slate-800 flex flex-col z-30 transition-all duration-300">
      <div class="p-6 overflow-hidden shrink-0">
        <h1 class="text-xl md:text-2xl font-black text-primary-600 dark:text-primary-500 truncate tracking-tight">Bakery Flow</h1>
        <p class="hidden md:block text-[10px] text-gray-400 dark:text-slate-500 uppercase font-black tracking-[0.2em] mt-1.5">Production Hub</p>
      </div>
      
      <nav class="mt-4 px-3 md:px-4 space-y-2 flex-1 overflow-y-auto">
        <RouterLink 
          to="/" 
          class="nav-link group"
          active-class="nav-link-active"
        >
          <LayoutDashboard class="w-6 h-6 md:mr-3 shrink-0 group-hover:scale-110 transition-transform" />
          <span class="hidden md:block">{{ t('nav.dashboard') }}</span>
        </RouterLink>

        <RouterLink 
          to="/ingredients" 
          class="nav-link group"
          active-class="nav-link-active"
        >
          <ShoppingBasket class="w-6 h-6 md:mr-3 shrink-0 group-hover:scale-110 transition-transform" />
          <span class="hidden md:block">{{ t('nav.ingredients') }}</span>
        </RouterLink>

        <RouterLink 
          to="/recipes" 
          class="nav-link group"
          active-class="nav-link-active"
        >
          <ChefHat class="w-6 h-6 md:mr-3 shrink-0 group-hover:scale-110 transition-transform" />
          <span class="hidden md:block">{{ t('nav.recipes') }}</span>
        </RouterLink>

        <RouterLink 
          to="/production" 
          class="nav-link group"
          active-class="nav-link-active"
        >
          <ClipboardList class="w-6 h-6 md:mr-3 shrink-0 group-hover:scale-110 transition-transform" />
          <span class="hidden md:block">{{ t('nav.production') }}</span>
        </RouterLink>
      </nav>

      <!-- Bottom Controls -->
      <div class="p-4 border-t border-gray-100 dark:border-slate-800 space-y-2">
        <button 
          @click="toggleDarkMode"
          class="flex items-center justify-center md:justify-start w-full p-3 text-sm font-bold text-gray-500 dark:text-slate-400 hover:bg-gray-100 dark:hover:bg-slate-800 rounded-2xl transition-all"
        >
          <component :is="isDark ? Sun : Moon" class="w-5 h-5 md:mr-3 shrink-0" />
          <span class="hidden md:block">{{ isDark ? 'Light' : 'Dark' }}</span>
        </button>

        <button 
          @click="toggleLanguage"
          class="flex items-center justify-center md:justify-start w-full p-3 text-sm font-black text-gray-500 dark:text-slate-400 hover:bg-gray-100 dark:hover:bg-slate-800 rounded-2xl transition-all uppercase"
        >
          <Languages class="w-5 h-5 md:mr-3 shrink-0" />
          <span class="hidden md:block">{{ locale }}</span>
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 overflow-y-auto p-4 md:p-10 relative">
      <div class="max-w-7xl mx-auto">
        <RouterView />
      </div>
    </main>
  </div>
</template>

<style>
@import "tailwindcss";

.nav-link {
  @apply flex items-center justify-center md:justify-start px-4 py-4 text-gray-600 dark:text-slate-400 rounded-2xl hover:bg-gray-50 dark:hover:bg-slate-800 hover:text-primary-600 dark:hover:text-primary-400 transition-all font-bold;
}

.nav-link-active {
  @apply bg-primary-600 dark:bg-primary-600 text-white dark:text-white shadow-lg shadow-primary-600/30 hover:bg-primary-700 hover:text-white;
}

body {
  @apply antialiased select-none;
}
</style>
