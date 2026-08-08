<script setup lang="ts">
import { ref } from 'vue';
import { onKeyStroke } from '@vueuse/core';

import SearchWindow from './components/divs/NewNoteCreationWindow.vue';
import BaseButton from './components/buttons/BaseButton.vue';
import Sidebar from './components/divs/Sidebar.vue';
import SidebarIcon from './components/svgs/SidebarIcon.vue';
import SidebarSettingsWindow from './components/divs/SidebarSettingsWindow.vue';

const isSidebarOpen = ref(false)
const isModalOpen = ref(false)
const modalPosition = ref({top: 0, left: 0})
const isNewNoteCreationWindowOpen = ref(false)
const isSettingsExtended = ref(false)

const handleSettingsClick = (v: number, event: MouseEvent) => {
  const target = event.currentTarget as HTMLElement
  const rect = target.getBoundingClientRect()

  modalPosition.value = {
    top: rect.bottom + 4,
    left: rect.left
  }

  isModalOpen.value = true
}

onKeyStroke('Escape', (e) => {
  e.preventDefault()
  if (isModalOpen.value) {
    isModalOpen.value = false
  } else if (isSidebarOpen.value) {
    isSidebarOpen.value = false
  } else if (isNewNoteCreationWindowOpen) {
    isNewNoteCreationWindowOpen.value = false
  }
})
onKeyStroke('j', (e) => {
  if (e.ctrlKey || e.metaKey) {
    e.preventDefault()
    isSidebarOpen.value = false
    isModalOpen.value = false
    isNewNoteCreationWindowOpen.value = true
  }
})
onKeyStroke('k', (e) => {
  if (e.ctrlKey || e.metaKey) {
    e.preventDefault()
    isSidebarOpen.value = false
    isModalOpen.value = false
  }
})

</script>

<template>
  <Sidebar v-model:show="isSidebarOpen" @settings-click="handleSettingsClick"/>

  <Teleport to="body">
    <SidebarSettingsWindow
      :show="isModalOpen"
      :position="modalPosition"
      @close="isModalOpen = false"
    ></SidebarSettingsWindow>
  </Teleport>

  <!-- Main page -->
  <div class="flex">
    <SearchWindow
      v-model:show="isNewNoteCreationWindowOpen"
      v-model:settings="isSettingsExtended"
    />

    <BaseButton class="m-1 border border-stone-200 dark:border-stone-800" variant="sidebar" @click="isSidebarOpen = !isSidebarOpen">
      <SidebarIcon/>
    </BaseButton>
  </div>

</template>