<script setup lang="ts">
import BaseButton from '../buttons/BaseButton.vue';
import Modal from './Modal.vue';

const show = defineModel<boolean>('show', {required: true})
const noteHeader = defineModel<string>('note-header', {required: true})

defineEmits<{
  (e: 'close'): void
  (e: 'delete'): void
}>()
</script>

<template>
  <Modal :class="show ? 'opacity-100' : 'opacity-0 pointer-events-none'">
    <div class="fixed inset-0 -z-10 bg-black/20 dark:bg-transparent" @click="$emit('close')"/>

    <div class="flex shrink-0 justify-between items-center p-2 border-b border-stone-200 dark:border-stone-700">
      <span class="pl-2 font-bold text-stone-600 dark:text-stone-300">Delete note "{{ noteHeader }}"?</span>
    </div>
    
    <div class="space-y-2 p-4 overflow-y-auto custom-scrollbar flex-1 min-h-0">
      <p>Are you sure you want to delete this note? <strong>This action cannot be undone!</strong></p>
    </div>

    <div class="rounded-b-2xl shrink-0 p-2 bg-stone-100 dark:bg-stone-800 border-t border-stone-200 dark:border-stone-700 flex items-center justify-end">
      <BaseButton class="mr-1 h-10 w-20 p-2 justify-center" variant="secondary" @click="$emit('close')">Cancel</BaseButton>
      <BaseButton class="h-10 w-20 p-2 justify-center" variant="delete" @click="$emit('delete')">Delete</BaseButton>
    </div>
  </Modal>
</template>