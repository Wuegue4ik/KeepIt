import { ref } from 'vue'
import { defineStore } from 'pinia'
import { onKeyStroke } from '@vueuse/core'
import { toast } from 'vue3-toastify'

export const useUiStore = defineStore('ui', () => {
  const isSidebarOpen = ref(false)
  const isModalOpen = ref(false)
  const isSettingsModalOpen = ref(false)
  const isDeleteModalOpen = ref(false)
  const isNoteModalOpen = ref(false)
  const isSettingsExtended = ref(false)

  const openNewNoteModal = () => {
    isSettingsModalOpen.value = false
    isDeleteModalOpen.value = false
    isModalOpen.value = false
    isNoteModalOpen.value = true
  }

  const closeNoteModal = () => {
    isNoteModalOpen.value = false
    toast.success('Note successfully created.')
  }

  const closeAllModals = () => {
    isModalOpen.value = false
    isSidebarOpen.value = false
    isNoteModalOpen.value = false
    isSettingsModalOpen.value = false
    isDeleteModalOpen.value = false
  }

  onKeyStroke('Escape', (e) => {
    e.preventDefault()
    closeAllModals()
  })

  onKeyStroke('j', (e) => {
    if (e.ctrlKey || e.metaKey) {
      e.preventDefault()
      openNewNoteModal()
    }
  })

  // onKeyStroke('k', (e) => {
  //   if (e.ctrlKey || e.metaKey) {
  //     e.preventDefault()
  //     isSidebarOpen.value = false
  //     isModalOpen.value = false
  //   }
  // })

  return {
    isSidebarOpen,
    isModalOpen,
    isSettingsModalOpen,
    isDeleteModalOpen,
    isNoteModalOpen,
    isSettingsExtended,
    openNewNoteModal,
    closeNoteModal,
    closeAllModals,
  }
})