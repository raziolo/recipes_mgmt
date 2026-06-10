<script setup lang="ts">
import { useI18n } from 'vue-i18n';
const { t } = useI18n();
</script>

<template>
  <div>
    <h2 class="text-3xl font-bold text-gray-800">{{ t('dashboard.title') }}</h2>
    <p class="mt-2 text-gray-600">{{ t('dashboard.subtitle') }}</p>
    
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
      <div class="bg-white p-6 rounded-xl shadow-sm border">
        <h3 class="text-sm font-medium text-gray-500 uppercase">{{ t('dashboard.activeSessions') }}</h3>
        <p class="text-3xl font-bold mt-2 text-primary-600">1</p>
      </div>
      <div class="bg-white p-6 rounded-xl shadow-sm border">
        <h3 class="text-sm font-medium text-gray-500 uppercase">{{ t('dashboard.tasksPending') }}</h3>
        <p class="text-3xl font-bold mt-2 text-amber-600">4</p>
      </div>
      <div class="bg-white p-6 rounded-xl shadow-sm border">
        <h3 class="text-sm font-medium text-gray-500 uppercase">{{ t('dashboard.completedToday') }}</h3>
        <p class="text-3xl font-bold mt-2 text-emerald-600">12</p>
      </div>
    </div>
  </div>
</template>
