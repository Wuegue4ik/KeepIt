<template>
  <div class="fixed inset-0 z-50 flex flex-col items-center justify-center bg-stone-900/10 dark:bg-stone-100/5 transition-all duration-300">
    
    <div class="w-full max-w-lg max-h-[90vh] bg-white dark:bg-stone-900 rounded-2xl shadow-xl transition-all duration-200 flex flex-col">
      <slot />
    </div>

  </div>
</template>