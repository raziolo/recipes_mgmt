<script setup lang="ts">
import { ref, computed, onMounted, nextTick } from 'vue';
import { useI18n } from 'vue-i18n';
import api from '../api';
import AppModal from '../components/AppModal.vue';
import type { ProductionSession, Recipe } from '../types';
import { PrinterIcon, TrashIcon, CalendarDaysIcon, PlusCircleIcon } from '@heroicons/vue/24/outline';

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
  status: 'PENDING',
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

const openSessionModal = async () => {
  sessionForm.value = {
    date: new Date().toISOString().split('T')[0],
    status: 'PLANNED',
    notes: ''
  };
  await nextTick();
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

const openTaskModal = async (session: ProductionSession) => {
  activeSession.value = session;
  taskForm.value = {
    recipe: undefined,
    target_qty: 1,
    target_unit: 'kg',
    status: 'PENDING',
    notes: ''
  };
  await nextTick();
  isTaskModalOpen.value = true;
};

const addTask = async () => {
  if (!activeSession.value || !taskForm.value.recipe) return;
  isLoading.value = true;
  try {
    const taskData = {
      ...taskForm.value,
      session: activeSession.value.id,
      target_unit: 'kg'
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

const isPrintPreviewOpen = ref(false);
const printPreviewData = ref<any>(null);
const printInstructions = ref<{ text: string; checked: boolean }[]>([]);

const checkedPrintItems = computed(() =>
  printInstructions.value.filter(item => item.checked)
);

const printSheet = async (taskId: number) => {
  try {
    const res = await api.post(`production-tasks/${taskId}/print_sheet/`);
    printPreviewData.value = res.data;
    printInstructions.value = (res.data.instructions || '')
      .split('\n')
      .map((l: string) => l.trim())
      .filter(Boolean)
      .map((text: string) => ({ text, checked: true }));
    isPrintPreviewOpen.value = true;
  } catch (error) {
    console.error('Printing error:', error);
    alert('Failed to load print preview.');
  }
};

const doPrint = () => {
  isPrintPreviewOpen.value = false;
  setTimeout(() => window.print(), 200);
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

const getStatusClass = (status: string) => {
  switch (status) {
    case 'PLANNED': return 'bg-blue-100 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400';
    case 'ACTIVE': return 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400';
    case 'COMPLETED': return 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400';
    default: return 'bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-400';
  }
};
</script>

<template>
  <div class="animate-in fade-in duration-500">
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
      <div>
        <h2 class="text-3xl font-black text-gray-900 dark:text-white">{{ t('production.title') }}</h2>
        <p class="mt-1 text-gray-500 dark:text-gray-400 font-medium">{{ t('production.subtitle') }}</p>
      </div>
      <button @click="openSessionModal" class="w-full sm:w-auto bg-primary-600 text-white px-6 py-3 rounded-2xl font-bold hover:bg-primary-700 transition-all shadow-lg shadow-primary-500/20 active:scale-95">
        {{ t('production.newSession') }}
      </button>
    </div>

    <div class="mt-8 space-y-8">
      <div v-for="session in sessions" :key="session.id" class="bg-white dark:bg-gray-800 rounded-3xl shadow-xl shadow-gray-200/50 dark:shadow-none border border-gray-100 dark:border-gray-700 overflow-hidden">
        <div class="bg-gray-50 dark:bg-gray-900/50 px-6 py-5 border-b border-gray-100 dark:border-gray-700 flex flex-col sm:flex-row gap-4 justify-between items-start sm:items-center">
          <div class="flex items-center space-x-4">
            <div class="bg-white dark:bg-gray-800 p-3 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700">
              <CalendarDaysIcon class="w-6 h-6 text-primary-600" />
            </div>
            <div>
              <h3 class="font-black text-lg text-gray-900 dark:text-white">{{ session.date }}</h3>
              <div class="flex items-center space-x-2">
                <span class="text-[10px] px-2 py-0.5 rounded-full font-black uppercase tracking-widest" :class="getStatusClass(session.status)">
                  {{ t(`common.status.${session.status.toLowerCase()}`) }}
                </span>
              </div>
            </div>
          </div>
          <div class="flex items-center space-x-3 w-full sm:w-auto">
            <button @click="openTaskModal(session)" class="flex-1 sm:flex-none flex items-center justify-center text-sm bg-primary-600 text-white px-4 py-2 rounded-xl font-bold hover:bg-primary-700 transition-all shadow-md active:scale-95">
              <PlusCircleIcon class="w-5 h-5 mr-2" /> {{ t('production.form.addTask') }}
            </button>
            <button @click="deleteSession(session.id!)" class="text-gray-400 hover:text-red-600 p-2 hover:bg-red-50 dark:hover:bg-red-900/30 rounded-xl transition-colors">
              <TrashIcon class="w-5 h-5" />
            </button>
          </div>
        </div>
        
        <div class="p-6">
          <div v-if="session.tasks && session.tasks.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div v-for="task in session.tasks" :key="task.id" class="group relative flex flex-col justify-between p-5 bg-white dark:bg-gray-800 rounded-2xl border border-gray-100 dark:border-gray-700 shadow-sm hover:border-primary-200 dark:hover:border-primary-500/50 transition-all">
              <div>
                <h4 class="font-black text-gray-900 dark:text-white text-lg truncate mb-1">{{ task.recipe_name }}</h4>
                <div class="flex items-center gap-3">
                  <span class="text-sm text-gray-600 dark:text-gray-400 font-bold uppercase tracking-tight">{{ task.target_qty }} {{ task.target_unit }}</span>
                  <span class="text-[9px] px-2 py-0.5 rounded bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-300 font-black uppercase tracking-widest">{{ t(`common.status.${task.status.toLowerCase()}`) }}</span>
                </div>
              </div>
              <div class="flex items-center justify-end space-x-2 mt-6">
                <button @click="printSheet(task.id!)" class="p-3 text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-primary-50 dark:hover:bg-primary-900/30 rounded-xl transition-all">
                  <PrinterIcon class="w-5 h-5" />
                </button>
                <button @click="deleteTask(task.id!)" class="p-3 text-gray-400 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/30 rounded-xl transition-all">
                  <TrashIcon class="w-5 h-5" />
                </button>
              </div>
            </div>
          </div>
          <div v-else class="text-center py-16 text-gray-400 italic bg-gray-50 dark:bg-gray-900/30 rounded-3xl border-2 border-dashed border-gray-100 dark:border-gray-700">
            {{ t('production.emptyTasks') }}
          </div>
        </div>
      </div>
      
      <div v-if="sessions.length === 0" class="py-32 text-center text-gray-500 bg-white dark:bg-gray-800 border-2 border-dashed border-gray-200 dark:border-gray-700 rounded-3xl">
        <CalendarDaysIcon class="w-16 h-16 mx-auto text-gray-200 dark:text-gray-700 mb-6" />
        <p class="text-lg font-bold">{{ t('production.emptySessions') }}</p>
      </div>
    </div>

    <!-- Session Modal -->
    <AppModal 
      :show="isSessionModalOpen" 
      :title="t('production.newSession')" 
      @close="isSessionModalOpen = false"
    >
      <form @submit.prevent="createSession" class="space-y-6">
        <div>
          <label class="block text-xs font-black text-gray-400 uppercase tracking-widest mb-2">{{ t('production.form.date') }}</label>
          <input v-model="sessionForm.date" type="date" required class="block w-full p-3 border border-gray-200 dark:border-gray-700 rounded-xl bg-gray-50 dark:bg-gray-900 font-bold" />
        </div>
        <div>
          <label class="block text-xs font-black text-gray-400 uppercase tracking-widest mb-2">{{ t('production.form.status') }}</label>
          <select v-model="sessionForm.status" class="block w-full p-3 border border-gray-200 dark:border-gray-700 rounded-xl bg-gray-50 dark:bg-gray-900 font-bold">
            <option value="PLANNED">{{ t('common.status.planned') }}</option>
            <option value="ACTIVE">{{ t('common.status.active') }}</option>
            <option value="COMPLETED">{{ t('common.status.completed') }}</option>
          </select>
        </div>
        <div class="mt-8 flex flex-col sm:flex-row justify-end gap-3">
          <button type="button" @click="isSessionModalOpen = false" class="px-6 py-3 border border-gray-200 dark:border-gray-700 rounded-xl text-sm font-bold text-gray-700 dark:text-gray-300">
            {{ t('common.cancel') }}
          </button>
          <button type="submit" :disabled="isLoading" class="px-6 py-3 bg-primary-600 text-white rounded-xl text-sm font-bold hover:bg-primary-700 shadow-lg shadow-primary-500/20">
            {{ isLoading ? '...' : t('common.save') }}
          </button>
        </div>
      </form>
    </AppModal>

    <!-- Task Modal -->
    <AppModal 
      :show="isTaskModalOpen" 
      :title="t('production.form.addTask')" 
      @close="isTaskModalOpen = false"
    >
      <form @submit.prevent="addTask" class="space-y-6">
        <div>
          <label class="block text-xs font-black text-gray-400 uppercase tracking-widest mb-2">{{ t('production.form.recipe') }}</label>
          <select v-model="taskForm.recipe" required class="block w-full p-3 border border-gray-200 dark:border-gray-700 rounded-xl bg-gray-50 dark:bg-gray-900 font-bold">
            <option :value="undefined">{{ t('production.form.recipe') }}</option>
            <option v-for="r in recipes" :key="r.id" :value="r.id">{{ r.name }}</option>
          </select>
        </div>
        
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div>
            <label class="block text-xs font-black text-gray-400 uppercase tracking-widest mb-2">{{ t('production.form.targetQty') }}</label>
            <input v-model="taskForm.target_qty" type="number" step="0.001" required class="block w-full p-3 border border-gray-200 dark:border-gray-700 rounded-xl bg-gray-50 dark:bg-gray-900 font-bold" />
          </div>
          <div>
            <label class="block text-xs font-black text-gray-400 uppercase tracking-widest mb-2">{{ t('production.form.taskStatus') }}</label>
            <select v-model="taskForm.status" class="block w-full p-3 border border-gray-200 dark:border-gray-700 rounded-xl bg-gray-50 dark:bg-gray-900 font-bold">
              <option value="PENDING">{{ t('common.status.pending') }}</option>
              <option value="IN_PROGRESS">{{ t('common.status.in_progress') }}</option>
              <option value="DONE">{{ t('common.status.done') }}</option>
            </select>
          </div>
        </div>

        <div class="mt-8 flex flex-col sm:flex-row justify-end gap-3">
          <button type="button" @click="isTaskModalOpen = false" class="px-6 py-3 border border-gray-200 dark:border-gray-700 rounded-xl text-sm font-bold text-gray-700 dark:text-gray-300">
            {{ t('common.cancel') }}
          </button>
          <button type="submit" :disabled="isLoading" class="px-6 py-3 bg-primary-600 text-white rounded-xl text-sm font-bold hover:bg-primary-700 shadow-lg shadow-primary-500/20">
            {{ isLoading ? '...' : t('common.save') }}
          </button>
        </div>
      </form>
    </AppModal>

    <!-- Print Preview Modal -->
    <AppModal
      :show="isPrintPreviewOpen"
      :title="t('production.actions.print')"
      @close="isPrintPreviewOpen = false"
    >
      <div v-if="printPreviewData" class="space-y-6">
        <div>
          <h4 class="text-2xl font-black text-gray-900 dark:text-white">{{ printPreviewData.recipe_name }}</h4>
          <p class="mt-1 text-sm font-bold text-gray-500">{{ printPreviewData.target_qty }} {{ printPreviewData.target_unit }}</p>
        </div>

        <div>
          <h5 class="text-xs font-black text-gray-400 uppercase tracking-widest mb-3">{{ t('recipes.form.printPreview.components') }}</h5>
          <div class="space-y-2">
            <div v-for="(ing, i) in printPreviewData.ingredients" :key="i" class="flex justify-between items-center py-2 px-3 bg-gray-50 dark:bg-gray-900 rounded-xl">
              <span class="font-bold text-gray-700 dark:text-gray-300 text-sm">{{ ing.name }}</span>
              <span class="text-xs font-bold text-primary-600 dark:text-primary-400 whitespace-nowrap">{{ ing.qty }} {{ ing.unit }}</span>
            </div>
            <div v-if="printPreviewData.sub_recipes && printPreviewData.sub_recipes.length > 0" class="mt-4">
              <div v-for="(sub, i) in printPreviewData.sub_recipes" :key="'sub'+i" class="py-2 px-3 bg-gray-50 dark:bg-gray-900 rounded-xl mb-2">
                <p class="font-bold text-gray-700 dark:text-gray-300 text-sm mb-1">{{ sub.recipe_name }} — {{ sub.target_qty }} {{ sub.target_unit }}</p>
                <div v-for="(ing, j) in sub.ingredients" :key="'s'+i+'i'+j" class="flex justify-between items-center pl-4 py-0.5">
                  <span class="text-xs text-gray-500">{{ ing.name }}</span>
                  <span class="text-xs font-bold text-primary-600 dark:text-primary-400">{{ ing.qty }} {{ ing.unit }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div>
          <h5 class="text-xs font-black text-gray-400 uppercase tracking-widest mb-3">{{ t('recipes.form.printPreview.instructions') }}</h5>
          <div v-if="printInstructions.length === 0" class="text-sm text-gray-400 italic">---</div>
          <div v-else class="space-y-1.5 max-h-48 overflow-y-auto custom-scrollbar">
            <label v-for="(item, i) in printInstructions" :key="i" class="flex items-start gap-3 p-2 -mx-2 rounded-xl hover:bg-gray-50 dark:hover:bg-gray-900 cursor-pointer">
              <input type="checkbox" v-model="item.checked" class="mt-0.5 rounded border-gray-300 dark:border-gray-600 text-primary-600 focus:ring-primary-500" />
              <span class="text-sm text-gray-700 dark:text-gray-300 select-none">{{ item.text }}</span>
            </label>
          </div>
        </div>

        <div class="flex flex-col sm:flex-row justify-end gap-3 pt-2">
          <button type="button" @click="isPrintPreviewOpen = false" class="px-6 py-3 border border-gray-200 dark:border-gray-700 rounded-xl text-sm font-bold text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
            {{ t('common.cancel') }}
          </button>
          <button type="button" @click="doPrint" class="px-6 py-3 bg-primary-600 text-white rounded-xl text-sm font-bold hover:bg-primary-700 shadow-lg shadow-primary-500/20 flex items-center">
            <PrinterIcon class="w-5 h-5 mr-2" /> {{ t('production.actions.print') }}
          </button>
        </div>
      </div>
    </AppModal>

    <!-- Printable Block -->
    <div id="print-area-production" class="print-only">
      <div v-if="printPreviewData" class="print-header">
        <h1>{{ printPreviewData.recipe_name }}</h1>
        <p class="print-total">{{ printPreviewData.target_qty }} {{ printPreviewData.target_unit }}</p>
      </div>
      <div v-if="printPreviewData" class="print-section">
        <h2>{{ t('recipes.form.printPreview.components') }}</h2>
        <ul>
          <li v-for="(ing, i) in printPreviewData.ingredients" :key="i">
            {{ ing.name }} — {{ ing.qty }} {{ ing.unit }}
          </li>
        </ul>
        <div v-if="printPreviewData.sub_recipes && printPreviewData.sub_recipes.length > 0">
          <div v-for="(sub, i) in printPreviewData.sub_recipes" :key="'sub'+i" style="margin-top:8pt">
            <p style="font-weight:700">{{ sub.recipe_name }} — {{ sub.target_qty }} {{ sub.target_unit }}</p>
            <ul>
              <li v-for="(ing, j) in sub.ingredients" :key="'s'+i+'i'+j">
                {{ ing.name }} — {{ ing.qty }} {{ ing.unit }}
              </li>
            </ul>
          </div>
        </div>
      </div>
      <div v-if="checkedPrintItems.length > 0" class="print-section">
        <h2>{{ t('recipes.form.printPreview.instructions') }}</h2>
        <ul>
          <li v-for="(item, i) in checkedPrintItems" :key="i">{{ item.text }}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #e5e7eb;
  border-radius: 9999px;
}
:root.dark .custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #374151;
}

@media screen {
  .print-only {
    display: none !important;
  }
}

@media print {
  body * {
    visibility: hidden;
  }
  #print-area-production, #print-area-production * {
    visibility: visible;
  }
  #print-area-production {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    padding: 2cm;
    font-family: 'Segoe UI', system-ui, sans-serif;
    color: #000;
  }
  #print-area-production h1 {
    font-size: 24pt;
    font-weight: 900;
    margin-bottom: 8pt;
  }
  #print-area-production .print-total {
    font-size: 12pt;
    font-weight: 700;
    color: #555;
    margin-bottom: 20pt;
  }
  #print-area-production .print-section {
    margin-bottom: 16pt;
  }
  #print-area-production .print-section h2 {
    font-size: 14pt;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #333;
    border-bottom: 2pt solid #333;
    padding-bottom: 4pt;
    margin-bottom: 8pt;
  }
  #print-area-production ul {
    list-style: disc;
    padding-left: 20pt;
    margin: 0;
  }
  #print-area-production li {
    font-size: 11pt;
    padding: 2pt 0;
    line-height: 1.5;
  }
}
</style>
