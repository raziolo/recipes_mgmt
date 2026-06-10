<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useI18n } from 'vue-i18n';
import api from '../api';
import AppModal from '../components/AppModal.vue';
import type { ProductionSession, ProductionTask, Recipe } from '../types';
import { PlusIcon, PrinterIcon, TrashIcon, CalendarDaysIcon } from '@heroicons/vue/24/outline';

const { t } = useI18n();
const sessions = ref<ProductionSession[]>([]);
const recipes = ref<Recipe[]>([]);
const isSessionModalOpen = ref(false);
const isTaskModalOpen = ref(false);
const isLoading = ref(false);

const activeSession = ref<ProductionSession | null>(null);

const sessionForm = ref({
  date: new Date().toISOString().split('T')[0],
  status: 'PLANNED',
  notes: ''
});

const taskForm = ref({
  recipe: undefined as number | undefined,
  target_qty: 1,
  target_unit: 'kg',
  notes: ''
});

const fetchData = async () => {
  try {
    const [sessionsRes, recipesRes] = await Promise.all([
      api.get('production-sessions/'),
      api.get('recipes/')
    ]);
    sessions.value = sessionsRes.data;
    recipes.value = recipesRes.data;
  } catch (error) {
    console.error('Error fetching data:', error);
  }
};

onMounted(fetchData);

const openSessionModal = () => {
  sessionForm.value = {
    date: new Date().toISOString().split('T')[0],
    status: 'PLANNED',
    notes: ''
  };
  isSessionModalOpen.value = true;
};

const createSession = async () => {
  isLoading.value = true;
  try {
    await api.post('production-sessions/', sessionForm.value);
    await fetchData();
    isSessionModalOpen.value = false;
  } catch (error) {
    console.error('Error creating session:', error);
  } finally {
    isLoading.value = false;
  }
};

const openTaskModal = (session: ProductionSession) => {
  activeSession.value = session;
  taskForm.value = {
    recipe: undefined,
    target_qty: 1,
    target_unit: 'kg',
    notes: ''
  };
  isTaskModalOpen.value = true;
};

const addTask = async () => {
  if (!activeSession.value || !taskForm.value.recipe) return;
  isLoading.value = true;
  try {
    const recipe = recipes.value.find(r => r.id === taskForm.value.recipe);
    const taskData = {
      ...taskForm.value,
      session: activeSession.value.id,
      target_unit: recipe?.base_yield_unit || 'kg'
    };
    await api.post('production-tasks/', taskData);
    await fetchData();
    isTaskModalOpen.value = false;
  } catch (error) {
    console.error('Error adding task:', error);
  } finally {
    isLoading.value = false;
  }
};

const deleteTask = async (taskId: number) => {
  if (!confirm(t('common.delete') + '?')) return;
  try {
    await api.delete(`production-tasks/${taskId}/`);
    await fetchData();
  } catch (error) {
    console.error('Error deleting task:', error);
  }
};

const printSheet = async (taskId: number) => {
  try {
    const response = await api.post(`production-tasks/${taskId}/print_sheet/`);
    alert('Sent to printer! Check the output log if needed.');
    console.log('Printer output:', response.data.output);
  } catch (error) {
    console.error('Printing error:', error);
    alert('Failed to print. Check connection.');
  }
};

const deleteSession = async (id: number) => {
  if (!confirm(t('common.delete') + ' ' + t('production.session') + '?')) return;
  try {
    await api.delete(`production-sessions/${id}/`);
    await fetchData();
  } catch (error) {
    console.error('Error deleting session:', error);
  }
};
</script>

<template>
  <div>
    <div class="flex justify-between items-center">
      <div>
        <h2 class="text-3xl font-bold text-gray-800">{{ t('production.title') }}</h2>
        <p class="mt-2 text-gray-600">{{ t('production.subtitle') }}</p>
      </div>
      <button @click="openSessionModal" class="bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors shadow-sm">
        {{ t('production.newSession') }}
      </button>
    </div>

    <div class="mt-8 space-y-8">
      <div v-for="session in sessions" :key="session.id" class="bg-white rounded-xl shadow-sm border overflow-hidden">
        <div class="bg-gray-50 px-6 py-4 border-b flex justify-between items-center">
          <div class="flex items-center space-x-4">
            <CalendarDaysIcon class="w-6 h-6 text-gray-400" />
            <div>
              <h3 class="font-bold text-lg text-gray-900">{{ session.date }}</h3>
              <p class="text-xs text-gray-500 uppercase font-bold">{{ session.status }}</p>
            </div>
          </div>
          <div class="flex items-center space-x-3">
            <button @click="openTaskModal(session)" class="text-sm bg-primary-50 text-primary-600 px-3 py-1 rounded-md font-bold hover:bg-primary-100 transition-colors">
              + {{ t('nav.recipes') }}
            </button>
            <button @click="deleteSession(session.id!)" class="text-gray-400 hover:text-red-600 p-1">
              <TrashIcon class="w-5 h-5" />
            </button>
          </div>
        </div>
        
        <div class="p-6">
          <div v-if="session.tasks && session.tasks.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div v-for="task in session.tasks" :key="task.id" class="flex justify-between items-center p-4 bg-white rounded-lg border border-gray-100 shadow-sm hover:border-primary-200 transition-all">
              <div>
                <p class="font-bold text-gray-900">{{ task.recipe_name }}</p>
                <div class="flex items-center space-x-2 mt-1">
                  <span class="text-sm text-gray-600 font-medium">{{ task.target_qty }} {{ task.target_unit }}</span>
                  <span class="text-[10px] px-1.5 py-0.5 rounded bg-gray-100 text-gray-500 font-bold uppercase">{{ task.status }}</span>
                </div>
              </div>
              <div class="flex items-center space-x-2">
                <button @click="printSheet(task.id!)" class="p-2 text-gray-400 hover:text-primary-600 hover:bg-primary-50 rounded-full transition-colors">
                  <PrinterIcon class="w-5 h-5" />
                </button>
                <button @click="deleteTask(task.id!)" class="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-full transition-colors">
                  <TrashIcon class="w-5 h-5" />
                </button>
              </div>
            </div>
          </div>
          <div v-else class="text-center py-10 text-gray-400 italic bg-gray-50 rounded-lg border-2 border-dashed">
            {{ t('production.emptyTasks') }}
          </div>
        </div>
      </div>
      
      <div v-if="sessions.length === 0" class="py-20 text-center text-gray-500 bg-white border-2 border-dashed rounded-xl">
        <CalendarDaysIcon class="w-12 h-12 mx-auto text-gray-200 mb-4" />
        {{ t('production.emptySessions') }}
      </div>
    </div>

    <!-- Session Modal -->
    <AppModal 
      :show="isSessionModalOpen" 
      :title="t('production.newSession')" 
      @close="isSessionModalOpen = false"
    >
      <form @submit.prevent="createSession" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700">Date</label>
          <input v-model="sessionForm.date" type="date" required class="mt-1 block w-full p-2 border rounded bg-gray-50" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700">Status</label>
          <select v-model="sessionForm.status" class="mt-1 block w-full p-2 border rounded bg-gray-50">
            <option value="PLANNED">Planned</option>
            <option value="ACTIVE">Active</option>
            <option value="COMPLETED">Completed</option>
          </select>
        </div>
        <div class="mt-6 flex justify-end space-x-3">
          <button type="button" @click="isSessionModalOpen = false" class="px-4 py-2 border rounded-md text-sm font-medium text-gray-700">
            {{ t('common.cancel') }}
          </button>
          <button type="submit" :disabled="isLoading" class="px-4 py-2 bg-primary-600 text-white rounded-md text-sm font-medium hover:bg-primary-700">
            {{ isLoading ? '...' : t('common.save') }}
          </button>
        </div>
      </form>
    </AppModal>

    <!-- Task Modal -->
    <AppModal 
      :show="isTaskModalOpen" 
      title="Add Task to Session" 
      @close="isTaskModalOpen = false"
    >
      <form @submit.prevent="addTask" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700">Recipe</label>
          <select v-model="taskForm.recipe" required class="mt-1 block w-full p-2 border rounded bg-gray-50">
            <option :value="undefined">-- Select Recipe --</option>
            <option v-for="r in recipes" :key="r.id" :value="r.id">{{ r.name }}</option>
          </select>
        </div>
        
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Target Qty</label>
            <input v-model="taskForm.target_qty" type="number" step="0.001" required class="mt-1 block w-full p-2 border rounded bg-gray-50" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700">Status</label>
            <select v-model="taskForm.status" class="mt-1 block w-full p-2 border rounded bg-gray-50">
              <option value="PENDING">Pending</option>
              <option value="IN_PROGRESS">In Progress</option>
              <option value="DONE">Done</option>
            </select>
          </div>
        </div>

        <div class="mt-6 flex justify-end space-x-3">
          <button type="button" @click="isTaskModalOpen = false" class="px-4 py-2 border rounded-md text-sm font-medium text-gray-700">
            {{ t('common.cancel') }}
          </button>
          <button type="submit" :disabled="isLoading" class="px-4 py-2 bg-primary-600 text-white rounded-md text-sm font-medium hover:bg-primary-700">
            {{ isLoading ? '...' : t('common.save') }}
          </button>
        </div>
      </form>
    </AppModal>
  </div>
</template>
