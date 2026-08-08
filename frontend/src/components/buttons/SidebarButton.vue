<script setup lang="ts">
import SidebarSettingsSVG from '../svgs/SidebarSettingsIcon.vue'

const emit = defineEmits<{
  (e: "menuClick", event: MouseEvent): void
  (e: "settingsClick", event: MouseEvent): void
}>()

const handleMainClick = (event: MouseEvent) => {
  emit("menuClick", event)
}

const handleSettingsClick = (event: MouseEvent) => {
  emit("settingsClick", event)
}
</script>

<template>
  <div class="mr-1 flex group bg-stone-100 dark:bg-stone-900 hover:bg-stone-200 dark:hover:bg-stone-800 rounded-lg">
    <button
      class="cursor-pointer p-2 flex-1 text-left"
      @click="handleMainClick"
    >
      <span class="truncate block">
        <slot/>
      </span>
    </button>
    <button
      class="w-8 m-1 cursor-pointer p-0 ml-auto rounded-lg pointer-events-none opacity-0 text-stone-600 dark:text-stone-400 hover:bg-stone-300 dark:hover:bg-stone-700 group-hover:pointer-events-auto group-hover:opacity-100"
      @click="handleSettingsClick"
    >
      <SidebarSettingsSVG/>
    </button>
  </div>
</template>