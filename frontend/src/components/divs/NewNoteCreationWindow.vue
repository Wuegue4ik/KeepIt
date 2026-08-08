<script setup lang="ts">
import Modal from './Modal.vue';
import BaseButton from '../buttons/BaseButton.vue';
import ExitIcon from '../svgs/ExitIcon.vue';
import ArrowIcon from '../svgs/ArrowIcon.vue';

const show = defineModel<boolean>('show', {required: true})
const settings = defineModel<boolean>('settings', {required: true})
</script>

<template>
  <Modal :class="show ? 'opacity-100' : 'opacity-0 pointer-events-none'">
    <div class="fixed inset-0 -z-10 bg-stone-900/10 dark:bg-stone-100/5" @click="show = false"/>

    <div class="flex shrink-0 justify-between items-center p-2 border-b border-stone-200 dark:border-stone-700">
      <span class="pl-2 font-bold text-stone-600 dark:text-stone-300">NEW NOTE</span>
      <BaseButton variant="sidebar" @click="show = false">
        <ExitIcon/>
      </BaseButton>
    </div>
    
    <div class="space-y-2 p-4 overflow-y-auto custom-scrollbar flex-1 min-h-0">
      <div class="group">
        <p class="font-medium focus-on-input">Title</p>
        <input
          type="text"
          placeholder="Note title..."
          class="w-full px-2 py-2 border border-stone-200 dark:border-stone-700 rounded-lg focus:outline-none focus:border-stone-400 dark:focus:border-stone-500 placeholder:italic transition-colors"
        />
      </div>

      <div class="group">
        <p class="font-medium focus-on-input">Main text</p>
        <textarea
          placeholder="What are you thinking about?"
          rows="4"
          class="w-full px-2 py-2 border border-stone-200 dark:border-stone-700 rounded-lg focus:outline-none focus:border-stone-400 dark:focus:border-stone-500 placeholder:italic transition-colors resize-none"
        />
      </div>

      <div class="group">
        <p class="font-medium focus-on-input">Tags</p>
        <input
          type="text"
          placeholder="Tags goes here"
          class="w-full px-2 py-2 border border-stone-200 dark:border-stone-700 rounded-lg focus:outline-none focus:border-stone-400 dark:focus:border-stone-500 placeholder:italic transition-colors"
        />
      </div>

      <button
        class="mt-2 flex justify-between font-medium items-center cursor-pointer w-full p-2 rounded-xl hover:text-stone-950 dark:hover:text-stone-100 hover:bg-stone-100 dark:hover:bg-stone-800 transition-all duration-200"
        :class="settings ? 'text-stone-950 dark:text-stone-100' : ''"
        @click="settings = !settings"
      >
        <span>Additional settings</span>
        <ArrowIcon :class="['w-5 h-5 transition-all duration-200', settings ? 'rotate-180' : '']"/>
      </button>
      <div 
        class="grid transition-all duration-300 ease-in-out"
        :class="settings ? 'grid-rows-[1fr] opacity-100 mt-2' : 'grid-rows-[0fr] opacity-0 pointer-events-none'"
      >
        <div class="overflow-hidden flex flex-col">
          <button v-for="i in 15" :key="i" class="m-1 hover:bg-stone-700">
            {{ i }}
          </button>
        </div>
      </div>
    </div>

    <div class="rounded-b-2xl shrink-0 p-2 bg-stone-100 dark:bg-stone-800 border-t border-stone-200 dark:border-stone-700 flex items-center justify-end">
      <BaseButton class="h-10 w-20 p-2 justify-center">Create</BaseButton>
    </div>
  </Modal>
</template>

<style scoped>
@reference "@/assets/base.css";

.focus-on-input {
  @apply group-has-focus:text-stone-950 dark:group-has-focus:text-stone-50 transition-all pl-2;
}
</style>