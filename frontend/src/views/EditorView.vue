<script setup lang="ts">
import BaseButton from '@/components/buttons/BaseButton.vue';
import StarterKit from '@tiptap/starter-kit';
import { useEditor, EditorContent } from '@tiptap/vue-3';
import { Markdown } from 'tiptap-markdown';

const editor = useEditor({
  extensions: [
    StarterKit,
    Markdown
  ]
})
const getMarkdown = () => {
  if (!editor.value) return ''

  return (editor.value as any).storage.markdown.getMarkdown()
}
</script>

<template>
  <header class="border-b border-stone-200 dark:border-stone-800 p-1">
    <div class="flex flex-wrap gap-0.5 max-h-30 overflow-y-auto">
      <BaseButton
        variant="sidebar"
        :class="['header-button w-9 justify-center', {'is-active': editor?.isActive('bold')}]"
        @click="editor?.chain().focus().toggleBold().run()"
      >
        B
      </BaseButton>
      <BaseButton
        variant="sidebar"
        :class="['header-button w-9 justify-center', {'is-active': editor?.isActive('italic')}]"
        @click="editor?.chain().focus().toggleItalic().run()"
      >
        I
      </BaseButton>
      <BaseButton variant="sidebar" class="header-button w-9 justify-center">
        S
      </BaseButton>
      <BaseButton variant="sidebar" class="header-button w-9 justify-center">
        H
      </BaseButton>
      <BaseButton variant="sidebar" class="header-button w-30">
        Headers
      </BaseButton>
      <BaseButton variant="sidebar" class="header-button w-9 justify-center">
        /\
      </BaseButton>
      <BaseButton variant="sidebar" class="header-button w-9 justify-center">
        \/
      </BaseButton>
      <BaseButton variant="sidebar" class="header-button w-9 justify-center">
        `
      </BaseButton>
      <BaseButton variant="sidebar" class="header-button w-9 justify-center">
        >
      </BaseButton>
      
    </div>
  </header>

  <main>
    <div class="">
      <EditorContent :editor="editor" />
    </div>
  </main>
</template>

<style scoped>
@import "tailwindcss";

.is-active {
  @apply bg-stone-200
}

.header-button {
  @apply shrink-0 h-9 flex items-center
}

:global(.dark) .is-active {
  @apply bg-stone-800
}
</style>