<script setup lang="ts">
import { computed } from 'vue';  

interface Props {
  variant?: "primary" | "secondary" | "sidebar" | "settings" | "delete" | "dropdown"
  disabled?: boolean
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: "primary",
  disabled: false,
  loading: false
})

const variantClasses = {
  "primary": "items-center font-bold bg-amber-400 dark:bg-amber-600 hover:bg-amber-500 text-white dark:text-stone-900 rounded-xl transition-all duration-200",
  "secondary": "items-center font-medium text-stone-400 dark:text-stone-600 hover:text-stone-700 dark:hover:text-stone-300 hover:bg-stone-200 dark:hover:bg-stone-700 rounded-xl transition-all duration-200",
  "sidebar": "items-center font-normal text-left text-stone-800 dark:text-stone-200 p-2 hover:bg-stone-200 dark:hover:bg-stone-800 rounded-lg overflow-hidden",
  "dropdown": "items-center font-normal text-left text-stone-800 dark:text-stone-200 p-2 hover:bg-stone-200 dark:hover:bg-stone-800 overflow-hidden",
  "settings": "items-center font-normal text-left text-stone-800 dark:text-stone-200 p-2 hover:bg-stone-200 dark:hover:bg-stone-700 rounded-lg overflow-hidden",
  "delete": "items-center font-bold bg-rose-500 hover:bg-rose-600 dark:hover:bg-rose-400 text-white dark:text-stone-900 rounded-xl transition-all duration-200"
}

const buttonClasses = computed(() => [
  "flex cursor-pointer",
  variantClasses[props.variant],
  { "cursor-not-allowed pointer-events-none opacity-50": props.disabled || props.loading }
])

</script>

<template>
  <button
    :disabled="disabled || loading"
    :class="buttonClasses"
  >
    <svg 
      v-if="loading" 
      class="animate-spin m-1 mr-2 h-4 w-4 text-current" 
      xmlns="http://www.w3.org/2000/svg" 
      fill="none" 
      viewBox="0 0 24 24"
    >
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
    </svg>
    <slot/>
  </button>
</template>