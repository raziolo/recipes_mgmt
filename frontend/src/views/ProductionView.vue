<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useI18n } from 'vue-i18n';
import api from '../api';

const { t } = useI18n();
const sessions = ref<any[]>([]);

onMounted(async () => {
  try {
    const response = await api.get('production-sessions/');
    sessions.value = response.data;
  } catch (error) {
    console.error('Error fetching production sessions:', error);
  }
});
</script>

<template>
  <div>
    <div class="flex justify-between items-center">
      <div>
        <h2 class="text-3xl font-bold text-gray-800">{{ t('production.title') }}</h2>
        <p class="mt-2 text-gray-600">{{ t('production.subtitle') }}</p>
      </div>
      <button class="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors">
        {{ t('production.newSession') }}
      </button>
    </div>

    <div class="mt-8 space-y-6">
      <div v-for="session in sessions" :key="session.id" class="bg-white rounded-xl shadow-sm border overflow-hidden">
        <div class="bg-gray-50 px-6 py-4 border-b flex justify-between items-center">
          <h3 class="font-bold text-lg text-gray-900">{{ t('production.session') }}: {{ session.date }}</h3>
          <span :class="{
            'px-2 py-1 rounded text-xs font-bold uppercase': true,
            'bg-blue-100 text-blue-700': session.status === 'PLANNED',
            'bg-amber-100 text-amber-700': session.status === 'ACTIVE',
            'bg-emerald-100 text-emerald-700': session.status === 'COMPLETED'
          }">
            {{ session.status }}
          </span>
        </div>
        
        <div class="p-6">
          <div v-if="session.tasks && session.tasks.length > 0" class="space-y-4">
            <div v-for="task in session.tasks" :key="task.id" class="flex justify-between items-center p-4 bg-gray-50 rounded-lg border border-gray-100">
              <div>
                <p class="font-bold text-gray-900">{{ task.recipe_name }}</p>
                <p class="text-sm text-gray-500">{{ task.target_qty }} {{ task.target_unit }}</p>
              </div>
              <div class="flex items-center space-x-4">
                <span class="text-xs text-gray-400 italic">{{ task.status }}</span>
                <button class="bg-white border text-gray-700 px-3 py-1 rounded shadow-sm hover:bg-gray-50 transition-colors text-sm">
                  {{ t('production.actions.print') }}
                </button>
              </div>
            </div>
          </div>
          <div v-else class="text-center py-6 text-gray-400 italic">
            {{ t('production.emptyTasks') }}
          </div>
        </div>
      </div>
      
      <div v-if="sessions.length === 0" class="py-12 text-center text-gray-500 bg-white border-2 border-dashed rounded-xl">
        {{ t('production.emptySessions') }}
      </div>
    </div>
  </div>
</template>
