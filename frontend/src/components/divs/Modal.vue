<template>
  <div class="fixed inset-0 z-40 flex flex-col items-center justify-center transition-all duration-300">
    
    <div class="w-full max-w-lg max-h-[90vh] bg-white dark:bg-stone-900 rounded-2xl shadow-xl transition-all duration-200 flex flex-col">
      <slot />
    </div>

  </div>
</template>