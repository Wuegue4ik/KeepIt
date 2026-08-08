<script setup lang="ts">
import SidebarIcon from '../svgs/SidebarIcon.vue';
import BaseButton from '../buttons/BaseButton.vue';
import SidebarButton from '../buttons/SidebarButton.vue';

const show = defineModel<boolean>('show', {required: true})

defineEmits<{
  (e: 'settings-click', id: number, event: MouseEvent): void
}>()
</script>

<template>
  <Teleport to="body">
    <div class="modal-bg" :class="show ? 'opacity-100' : 'opacity-0 pointer-events-none'" @click="show = !show"/>

    <aside
      class="p-1 pr-0 fixed flex flex-col top-0 h-full w-72 shadow-2xl z-30 bg-stone-100 dark:bg-stone-900 border-r border-stone-300 dark:border-stone-700 transition-all duration-200"
      :class="show ? 'translate-x-0' : '-translate-x-72 bg-white/5 dark:bg-black/5 border-stone-300/5 dark:border-stone-700/5'"
    >
      <div class="flex mb-2">
        <BaseButton variant="sidebar" @click="show = !show">
          <SidebarIcon/>
        </BaseButton>
      </div>

      <div class="p-1.5 mb-2">
        <!-- Note Button -->
        <button
          class="mb-1 group relative w-full overflow-hidden rounded-full bg-white dark:bg-stone-800 p-0.5 text-stone-900 dark:text-stone-100 shadow dark:shadow-stone-700/50 transition-all duration-200 ease-out hover:shadow-lg dark:hover:bg-stone-700"
        >
          <div class="relative flex w-full cursor-pointer items-center justify-center p-2">
            <span
              class="font-medium transition-transform duration-200 ease-out group-hover:-translate-x-6 select-none"
            >
              New note
            </span>

            <span
              class="absolute right-3 opacity-0 translate-x-4 pointer-events-none transition-all duration-200 ease-out group-hover:opacity-100 group-hover:translate-x-0 select-none"
            >
              <span class="inline-flex items-center rounded-lg border border-stone-200 dark:border-stone-700 bg-stone-50 dark:bg-stone-800 px-2 py-0.5 text-xs text-stone-500 dark:text-stone-400 shadow-sm dark:shadow-none">
                <kbd class="font-sans font-semibold">Ctrl</kbd>
                <span class="mx-1 text-stone-400 dark:text-stone-500">+</span>
                <kbd class="font-sans font-semibold">J</kbd>
              </span>
            </span>
          </div>
        </button>

        <!-- Search Button -->
        <button
          class="mb-2 group relative w-full overflow-hidden rounded-full bg-white dark:bg-stone-800 p-0.5 text-stone-900 dark:text-stone-100 shadow dark:shadow-stone-700/50 transition-all duration-200 ease-out hover:shadow-lg dark:hover:bg-stone-700"
        >
          <div class="relative flex w-full cursor-pointer items-center justify-center p-2">
            <span
              class="font-medium transition-transform duration-200 ease-out group-hover:-translate-x-6 select-none"
            >
              Search
            </span>

            <span
              class="absolute right-3 opacity-0 translate-x-4 pointer-events-none transition-all duration-200 ease-out group-hover:opacity-100 group-hover:translate-x-0 select-none"
            >
              <span class="inline-flex items-center rounded-lg border border-stone-200 dark:border-stone-700 bg-stone-50 dark:bg-stone-800 px-2 py-0.5 text-xs text-stone-500 dark:text-stone-400 shadow-sm dark:shadow-none">
                <kbd class="font-sans font-semibold">Ctrl</kbd>
                <span class="mx-1 text-stone-400 dark:text-stone-500">+</span>
                <kbd class="font-sans font-semibold">K</kbd>
              </span>
            </span>
          </div>
        </button>
      </div>

      <div class="overflow-y-auto custom-scrollbar">
        <SidebarButton
          v-for="v in 50"
          :key="v"
          @settings-click="$emit('settings-click', v, $event)"
        >
          {{ v }}
        </SidebarButton>
      </div>

      <slot name="bottom"/>
    </aside>
  </Teleport>
</template>