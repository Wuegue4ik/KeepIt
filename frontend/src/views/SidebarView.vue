<script setup lang="ts">
import { useUiStore } from '@/stores/uis'
import NoteModal from '@/components/divs/NoteModal.vue'
import BaseButton from '@/components/buttons/BaseButton.vue'
import Sidebar from '@/components/divs/Sidebar.vue'
import SidebarIcon from '@/components/svgs/SidebarIcon.vue'

const ui = useUiStore()
</script>

<template>
  <Sidebar
    v-model:show="ui.isSidebarOpen"
    v-model:is-modal-open="ui.isSettingsModalOpen"
    v-model:is-delete-modal-open="ui.isDeleteModalOpen"
    @new-note-click="ui.openNewNoteModal"
  />

  <div class="flex min-h-screen w-full">
    
    <div class="flex-none p-1 border-r border-stone-200 dark:border-stone-800">
      <BaseButton
        class="sticky top-1"
        variant="sidebar" 
        @click="ui.isSidebarOpen = !ui.isSidebarOpen"
      >
        <SidebarIcon />
      </BaseButton>
    </div>

    <main class="flex-1 w-full min-w-0 bg-stone-100 dark:bg-stone-800">
      <RouterView />
    </main>

  </div>

  <NoteModal
    v-model:show="ui.isNoteModalOpen"
    v-model:settings="ui.isSettingsExtended"
    @close="ui.closeNoteModal"
  />
</template>