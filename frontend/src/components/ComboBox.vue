<script setup lang="ts">
import { ref, computed, watch, onMounted, onUnmounted } from 'vue';

const props = withDefaults(defineProps<{
  modelValue?: number | null;
  options: Record<string, any>[];
  placeholder?: string;
  labelKey?: string;
  valueKey?: string;
  allowCreate?: boolean;
  disabled?: boolean;
  searchPlaceholder?: string;
  noResultsLabel?: string;
  clearLabel?: string;
  createLabel?: string;
}>(), {
  modelValue: null,
  placeholder: 'Select...',
  labelKey: 'name',
  valueKey: 'id',
  allowCreate: false,
  disabled: false,
  searchPlaceholder: 'Search...',
  noResultsLabel: 'No results',
  clearLabel: 'Clear selection',
  createLabel: 'Create new',
});

const emit = defineEmits<{
  'update:modelValue': [value: number | null];
  create: [];
}>();

const isOpen = ref(false);
const search = ref('');
const buttonRef = ref<HTMLElement | null>(null);
const panelRef = ref<HTMLElement | null>(null);
const panelStyle = ref({ top: '0px', left: '0px', width: '0px' });

const selectedLabel = computed(() => {
  if (!props.modelValue) return '';
  const opt = props.options.find(o => o[props.valueKey] === props.modelValue);
  return opt ? opt[props.labelKey] : '';
});

const filteredOptions = computed(() => {
  const q = search.value.toLowerCase();
  if (!q) return props.options;
  return props.options.filter((o: Record<string, any>) =>
    (o[props.labelKey] || '').toLowerCase().includes(q)
  );
});

watch(isOpen, (val) => {
  if (val) search.value = '';
});

const toggle = () => {
  if (props.disabled) return;
  if (isOpen.value) {
    isOpen.value = false;
  } else {
    const rect = buttonRef.value?.getBoundingClientRect();
    if (rect) {
      panelStyle.value = {
        top: `${rect.bottom + 4}px`,
        left: `${rect.left}px`,
        width: `${rect.width}px`,
      };
    }
    isOpen.value = true;
  }
};

const select = (opt: Record<string, any>) => {
  emit('update:modelValue', opt[props.valueKey]);
  isOpen.value = false;
};

const clear = () => {
  emit('update:modelValue', null);
  isOpen.value = false;
};

const onWindowClick = (e: MouseEvent) => {
  if (!isOpen.value) return;
  const target = e.target as Node;
  if (buttonRef.value?.contains(target)) return;
  if (panelRef.value?.contains(target)) return;
  isOpen.value = false;
};

const onKeydown = (e: KeyboardEvent) => {
  if (e.key === 'Escape') isOpen.value = false;
};

onMounted(() => {
  document.addEventListener('click', onWindowClick);
  document.addEventListener('keydown', onKeydown);
});

onUnmounted(() => {
  document.removeEventListener('click', onWindowClick);
  document.removeEventListener('keydown', onKeydown);
});
</script>

<template>
  <div class="w-full">
    <button
      ref="buttonRef"
      type="button"
      :disabled="disabled"
      @click="toggle"
      class="w-full flex items-center justify-between gap-2 truncate text-sm p-2 border border-gray-200 dark:border-gray-700 rounded-xl bg-white dark:bg-gray-800 font-bold transition-all hover:border-gray-300 dark:hover:border-gray-600"
      :class="[isOpen ? 'ring-2 ring-primary-500/40 border-primary-500' : '']"
    >
      <span v-if="selectedLabel" class="truncate text-gray-900 dark:text-gray-100">{{ selectedLabel }}</span>
      <span v-else class="truncate text-gray-400 dark:text-gray-500 font-medium">{{ placeholder }}</span>
      <svg class="w-4 h-4 shrink-0 text-gray-400 transition-transform" :class="isOpen ? 'rotate-180' : ''" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
        <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
      </svg>
    </button>

    <Teleport to="body">
      <Transition
        enter-active-class="transition-all duration-200 ease-out"
        enter-from-class="opacity-0 -translate-y-1 scale-95"
        enter-to-class="opacity-100 translate-y-0 scale-100"
        leave-active-class="transition-all duration-150 ease-in"
        leave-from-class="opacity-100 translate-y-0 scale-100"
        leave-to-class="opacity-0 -translate-y-1 scale-95"
      >
        <div
          v-if="isOpen"
          ref="panelRef"
          :style="panelStyle"
          class="fixed z-[100] bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl shadow-xl shadow-gray-200/50 dark:shadow-black/50"
        >
          <div class="p-2 border-b border-gray-100 dark:border-gray-700">
            <input
              v-model="search"
              type="text"
              :placeholder="searchPlaceholder"
              class="w-full text-sm p-2 bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-primary-500/40 focus:border-primary-500 outline-none font-medium placeholder:text-gray-400"
            />
          </div>
          <div class="max-h-52 overflow-y-auto custom-scrollbar">
            <button
              v-if="modelValue"
              type="button"
              @click="clear"
              class="w-full text-left px-3 py-2 text-sm text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 font-bold flex items-center gap-2 border-b border-gray-100 dark:border-gray-700"
            >
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" /></svg>
              {{ clearLabel }}
            </button>
            <button
              v-for="opt in filteredOptions"
              :key="opt[valueKey]"
              type="button"
              @click="select(opt)"
              class="w-full text-left px-3 py-2.5 text-sm font-bold transition-colors"
              :class="opt[valueKey] === modelValue ? 'bg-primary-50 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300' : 'text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700/50'"
            >
              <span class="block break-words">{{ opt[labelKey] }}</span>
            </button>
            <div v-if="filteredOptions.length === 0 && !allowCreate" class="px-3 py-6 text-center text-sm text-gray-400 font-medium">
              {{ noResultsLabel }}
            </div>
          </div>
          <button
            v-if="allowCreate"
            type="button"
            @click.stop="isOpen = false; $emit('create')"
            class="w-full flex items-center justify-center gap-2 px-3 py-2.5 text-sm font-bold text-primary-600 dark:text-primary-400 hover:bg-primary-50 dark:hover:bg-primary-900/30 border-t border-gray-100 dark:border-gray-700 transition-colors"
          >
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" /></svg>
            {{ createLabel }}
          </button>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<style scoped>
.custom-scrollbar::-webkit-scrollbar { width: 5px; }
.custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
.custom-scrollbar::-webkit-scrollbar-thumb { background-color: #e5e7eb; border-radius: 9999px; }
:root.dark .custom-scrollbar::-webkit-scrollbar-thumb { background-color: #374151; }
</style>
