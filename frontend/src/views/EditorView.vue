<script setup lang="ts">
import BaseButton from '@/components/buttons/BaseButton.vue';
import StarterKit from '@tiptap/starter-kit';
import Highlight from '@tiptap/extension-highlight';
import Subscript from '@tiptap/extension-subscript'
import Superscript from '@tiptap/extension-superscript'
import { useEditor, EditorContent } from '@tiptap/vue-3';
import { Markdown } from 'tiptap-markdown';

const editor = useEditor({
  extensions: [
    StarterKit,
    Markdown,
    Highlight,
    Subscript,
    Superscript
  ]
})
const getMarkdown = () => {
  if (!editor.value) return ''

  return (editor.value as any).storage.markdown.getMarkdown()
}
</script>

<template>
  <header class="border-b border-stone-200 dark:border-stone-800 p-1">
    <div class="flex flex-wrap gap-0.5 max-h-30 overflow-y-auto justify-center">
      <BaseButton
        variant="sidebar"
        :class="['header-button w-9 justify-center', {'is-active': editor?.isActive('bold')}]"
        @click="editor?.chain().focus().toggleBold().run()"
        title="Bold"
      >
        <b>B</b>
      </BaseButton>
      <BaseButton
        variant="sidebar"
        :class="['header-button w-9 justify-center', {'is-active': editor?.isActive('italic')}]"
        @click="editor?.chain().focus().toggleItalic().run()"
        title="Italic"
      >
        <i>I</i>
      </BaseButton>
      <BaseButton
        variant="sidebar"
        :class="['header-button w-9 justify-center', {'is-active': editor?.isActive('strike')}]"
        @click="editor?.chain().focus().toggleStrike().run()"
        title="Strikethrough"
      >
        <del>S</del>
      </BaseButton>
      <BaseButton
        variant="sidebar"
        :class="['header-button w-9 justify-center', {'is-active': editor?.isActive('underline')}]"
        @click="editor?.chain().focus().toggleUnderline().run()"
        title="Underline"
      >
        <u>U</u>
      </BaseButton>
      <BaseButton
        variant="sidebar"
        :class="['header-button w-9 justify-center', {'is-active': editor?.isActive('highlight')}]"
        @click="editor?.chain().focus().toggleHighlight().run()"
        title="Highlight"
      >
        H
      </BaseButton>
      <BaseButton variant="sidebar" class="header-button w-30">
        Headers
      </BaseButton>
      <BaseButton
        variant="sidebar"
        :class="['header-button w-9 justify-center', {'is-active': editor?.isActive('subscript')}]"
        @click="editor?.chain().focus().toggleSubscript().run()"
        title="Subscript"
      >
        X<sub>2</sub>
      </BaseButton>
      <BaseButton
        variant="sidebar"
        :class="['header-button w-9 justify-center', {'is-active': editor?.isActive('superscript')}]"
        @click="editor?.chain().focus().toggleSuperscript().run()"
        title="Superscript"
      >
        X<sup>2</sup>
      </BaseButton>
      <BaseButton variant="sidebar" class="header-button w-9 justify-center">
        `
      </BaseButton>
      <BaseButton variant="sidebar" class="header-button w-9 justify-center">
        >
      </BaseButton>
      <BaseButton variant="sidebar" class="header-button w-9 justify-center">
        [x]
      </BaseButton>
      <BaseButton variant="sidebar" class="header-button w-30">
        Lists
      </BaseButton>
      
    </div>
  </header>

  <main>
    <div class="flex-col overflow-y-auto custom-scrollbar">
      <div class="flex justify-between mr-2 ml-2 mt-2">
        <div class="border-r border-b border-stone-200 dark:border-stone-800 w-4 h-4"></div>
        <div class="border-l border-b border-stone-200 dark:border-stone-800 w-4 h-4"></div>
      </div>
      <div class="">
        <EditorContent :editor="editor" class="focus:outline-none mr-7 ml-7 mt-1 mb-1" />
      </div>
      <div class="flex justify-between mr-2 ml-2 mb-2">
        <div class="border-r border-t border-stone-200 dark:border-stone-800 w-4 h-4"></div>
        <div class="border-l border-t border-stone-200 dark:border-stone-800 w-4 h-4"></div>
      </div>
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