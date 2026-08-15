<script setup lang="ts">
import { ref } from 'vue';
import { onKeyStroke } from '@vueuse/core';

import NoteModal from './components/divs/NoteModal.vue';
import BaseButton from './components/buttons/BaseButton.vue';
import Sidebar from './components/divs/Sidebar.vue';
import SidebarIcon from './components/svgs/SidebarIcon.vue';
import { toast } from 'vue3-toastify';

const isSidebarOpen = ref(false)
const isModalOpen = ref(false)
const isSettingsModalOpen = ref(false)
const isDeleteModalOpen = ref(false)

const isNoteModalOpen = ref(false)
const isSettingsExtended = ref(false)

const handleNewNoteClick = () => {
  isSettingsModalOpen.value = false
  isDeleteModalOpen.value = false
  isModalOpen.value = false
  isNoteModalOpen.value = true
}

onKeyStroke('Escape', (e) => {
  e.preventDefault()
  if (isModalOpen.value) {
    isModalOpen.value = false
  }
  if (isSidebarOpen.value) {
    isSidebarOpen.value = false
  }
  if (isNoteModalOpen) {
    isNoteModalOpen.value = false
  }
  if (isSettingsModalOpen.value) {
    isSettingsModalOpen.value = false
  }
  if (isDeleteModalOpen.value) {
    isDeleteModalOpen.value = false
  }
})
onKeyStroke('j', (e) => {
  if (e.ctrlKey || e.metaKey) {
    e.preventDefault()
    handleNewNoteClick()
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
  <Sidebar
    v-model:show="isSidebarOpen"
    v-model:is-modal-open="isSettingsModalOpen"
    v-model:is-delete-modal-open="isDeleteModalOpen"
    @new-note-click="handleNewNoteClick"
  />

  <!-- Main page -->
  <div class="flex">
    <NoteModal
      v-model:show="isNoteModalOpen"
      v-model:settings="isSettingsExtended"
      @close="isNoteModalOpen = false; toast.success('Note successfully created.')"
    />

    <BaseButton class="m-1 border border-stone-200 dark:border-stone-800" variant="sidebar" @click="isSidebarOpen = !isSidebarOpen">
      <SidebarIcon/>
    </BaseButton>
  </div>

</template>