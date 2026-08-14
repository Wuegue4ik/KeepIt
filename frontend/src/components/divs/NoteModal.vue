<script setup lang="ts">
import Modal from './Modal.vue';
import BaseButton from '../buttons/BaseButton.vue';
import ExitIcon from '../svgs/ExitIcon.vue';
import ArrowIcon from '../svgs/ArrowIcon.vue';
import { ref, reactive } from 'vue';
import type { Note } from '@/api/types';
import { useNotesStore } from '@/stores/notes.ts';

const show = defineModel<boolean>('show', {required: true})
const settings = defineModel<boolean>('settings', {required: true})

const notesStore = useNotesStore()
const isSubmitting = ref(false)
const localError = ref<string | null>(null)

const initialFormData = {
  header: '',
  text: '',
  tags: ''
}

const formData = reactive({ ...initialFormData })

const emit = defineEmits<{
  (e: 'close'): void
}>()

const resetForm = () => {
  Object.assign(formData, initialFormData)
}

const handleSubmit = async() => {
  if (!formData.header.trim() && !formData.text.trim()) {
    localError.value = "The title or text fields must be filled in!"
    return
  } else if (!formData.header.trim() && formData.text.trim()) {
    formData.header = formData.text.trim().slice(0, 50)
  }

  isSubmitting.value = true
  localError.value = null

  try {
    const parseTags: string[] = formData.tags
      .split(',')
      .map(tag => tag.trim())
      .filter(tag => tag.length > 0)

    const payload = {
      header: formData.header.trim(),
      text: formData.text.trim() || null,
      tags: parseTags
    }

    await notesStore.addNote(payload)
    emit('close')
    resetForm()
  } catch (err: any) {
    localError.value = err.response?.data?.detail || "Failed to save the note."
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <Modal :class="show ? 'opacity-100' : 'opacity-0 pointer-events-none'">
    <div class="fixed inset-0 -z-10 bg-black/20" @click="show = false"/>

    <header class="flex shrink-0 justify-between items-center p-2 border-b border-stone-200 dark:border-stone-700">
      <span class="pl-2 font-bold text-stone-600 dark:text-stone-300">New note</span>
      <BaseButton variant="sidebar" @click="show = false" :disabled="isSubmitting">
        <ExitIcon/>
      </BaseButton>
    </header>

    <div v-if="localError" class="">
        <div class="p-3 bg-rose-50 dark:bg-rose-950/40 border-b border-t border-rose-200 dark:border-rose-900/50">
          <p class="text-rose-500/80 dark:text-rose-400/70 truncate font-medium">
            {{ localError }}
          </p>
        </div>
    </div>
    
    <form @submit.prevent="handleSubmit">
      <main class="space-y-2 p-4 overflow-y-auto custom-scrollbar flex-1 min-h-0">
        <div class="group">
          <label for="header" class="font-medium focus-on-input">Title</label>
          <input
            id="header"
            v-model="formData.header"
            type="text"
            placeholder="Note title..."
            maxlength="50"
            :disabled="isSubmitting"
            class="w-full px-2 py-2 border border-stone-200 dark:border-stone-700 rounded-lg focus:outline-none focus:border-stone-400 dark:focus:border-stone-500 placeholder:italic transition-colors"
          />
        </div>

        <div class="group">
          <label for="text" class="font-medium focus-on-input">Main text</label>
          <textarea
            id="text"
            v-model="formData.text"
            placeholder="What are you thinking about?"
            rows="4"
            :disabled="isSubmitting"
            class="w-full px-2 py-2 border border-stone-200 dark:border-stone-700 rounded-lg focus:outline-none focus:border-stone-400 dark:focus:border-stone-500 placeholder:italic transition-colors resize-none"
          />
        </div>

        <div class="group">
          <label for="tags" class="font-medium focus-on-input">Tags</label>
          <input
            id="tags"
            v-model="formData.tags"
            type="text"
            placeholder="Tags goes here"
            :disabled="isSubmitting"
            class="w-full px-2 py-2 border border-stone-200 dark:border-stone-700 rounded-lg focus:outline-none focus:border-stone-400 dark:focus:border-stone-500 placeholder:italic transition-colors"
          />
        </div>

        <button
          class="mt-2 flex justify-between font-medium items-center cursor-pointer w-full p-2 rounded-xl hover:text-stone-950 dark:hover:text-stone-100 hover:bg-stone-100 dark:hover:bg-stone-800 transition-all duration-200"
          :class="settings ? 'text-stone-950 dark:text-stone-100' : ''"
          @click="settings = !settings"
          type="button"
        >
          <span>Additional settings</span>
          <ArrowIcon :class="['w-5 h-5 transition-all duration-200', settings ? 'rotate-180' : '']"/>
        </button>
        <div 
          class="grid transition-all duration-300 ease-in-out"
          :class="settings ? 'grid-rows-[1fr] opacity-100 mt-2' : 'grid-rows-[0fr] opacity-0 pointer-events-none'"
        >
          <div class="overflow-hidden flex flex-col">

            <label class="flex items-center justify-between p-2 rounded-xl hover:bg-stone-100 dark:hover:bg-stone-800 cursor-pointer group transition-colors select-none">
              
              <div class="flex items-center space-x-1.5">
                <span class="text-sm font-medium text-stone-600 dark:text-stone-300 group-hover:text-stone-900 dark:group-hover:text-stone-100 transition-colors">
                  Favorite
                </span>

                <div class="relative flex items-center group/tooltip">
                  ?

                  <div class="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 hidden group-hover/tooltip:flex flex-col items-center w-48 z-20 pointer-events-none">
                    <div class="bg-stone-800 dark:bg-stone-100 text-stone-100 dark:text-stone-900 text-xs rounded-lg py-1.5 px-2.5 shadow-xl text-center leading-tight font-normal">
                      Favorite notes/groups are showed on top of a sidebar
                    </div>
                    <div class="w-2 h-2 -mt-1 rotate-45 bg-stone-800 dark:bg-stone-100"></div>
                  </div>
                </div>
              </div>

              <div class="relative inline-flex items-center">
                <input type="checkbox" class="peer sr-only" />
                <div class="w-9 h-5 bg-stone-300 dark:bg-stone-700 rounded-full peer-checked:bg-stone-800 dark:peer-checked:bg-stone-200 transition-colors duration-200"></div>
                <div class="absolute left-0.5 w-4 h-4 bg-white dark:bg-stone-900 rounded-full transition-transform duration-200 ease-in-out peer-checked:translate-x-4"></div>
              </div>

            </label>

          </div>
        </div>
      </main>

      <footer class="rounded-b-2xl shrink-0 p-2 bg-stone-100 dark:bg-stone-800 border-t border-stone-200 dark:border-stone-700 flex items-center justify-end">
        <BaseButton @click="resetForm" type="button" :disabled="isSubmitting" variant="secondary" class="h-10 w-20 p-2 justify-center font-medium mr-1">Reset</BaseButton>
        <BaseButton type="submit" :disabled="isSubmitting" class="h-10 w-20 p-2 justify-center">Save</BaseButton>
      </footer>
    </form>

  </Modal>
</template>

<style scoped>
@reference "@/assets/base.css";

.focus-on-input {
  @apply group-has-focus:text-stone-950 dark:group-has-focus:text-stone-50 transition-all pl-2 text-stone-600 dark:text-stone-300;
}
</style>