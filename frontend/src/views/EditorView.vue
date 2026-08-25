<script setup lang="ts">
import BaseButton from '@/components/buttons/BaseButton.vue';
import StarterKit from '@tiptap/starter-kit';
import Highlight from '@tiptap/extension-highlight';
import Subscript from '@tiptap/extension-subscript'
import Superscript from '@tiptap/extension-superscript'
import { ref } from 'vue';
import { useEditor, EditorContent } from '@tiptap/vue-3';
import { Markdown } from 'tiptap-markdown';
import { useFloating, offset, flip, shift, autoUpdate } from '@floating-ui/vue'

const editor = useEditor({
  extensions: [
    StarterKit,
    Markdown,
    Highlight,
    Subscript,
    Superscript
  ],
  editorProps: {
    attributes: {
      class: 'flex-1 h-full p-8 focus:outline-none',
    },
  },
})
const getMarkdown = () => {
  if (!editor.value) return ''

  return (editor.value as any).storage.markdown.getMarkdown()
}

const isHeadersOpen = ref(false)
const headersRef = ref(null)
const headersFloating = ref(null)
const { floatingStyles: headersFloatingStyles } = useFloating(headersRef, headersFloating, {
  placement: 'bottom-end',
  whileElementsMounted: autoUpdate,
  middleware: [
    offset(6),
    flip(),
    shift({padding: 8})
  ]
})
</script>

<template>
  <header class="bg-white border-b border-stone-200 dark:border-stone-800 p-1 sticky top-0 z-50">
    <div class="flex flex-wrap gap-0.5 max-h-30 overflow-y-auto justify-center">
      <BaseButton
        variant="sidebar"
        :class="['header-button w-9', {'is-active': editor?.isActive('bold')}]"
        @click="editor?.chain().focus().toggleBold().run()"
        title="Bold"
      >
        <b>B</b>
      </BaseButton>
      <BaseButton
        variant="sidebar"
        :class="['header-button w-9', {'is-active': editor?.isActive('italic')}]"
        @click="editor?.chain().focus().toggleItalic().run()"
        title="Italic"
      >
        <i>I</i>
      </BaseButton>
      <BaseButton
        variant="sidebar"
        :class="['header-button w-9', {'is-active': editor?.isActive('strike')}]"
        @click="editor?.chain().focus().toggleStrike().run()"
        title="Strikethrough"
      >
        <del>S</del>
      </BaseButton>
      <BaseButton
        variant="sidebar"
        :class="['header-button w-9', {'is-active': editor?.isActive('underline')}]"
        @click="editor?.chain().focus().toggleUnderline().run()"
        title="Underline"
      >
        <u>U</u>
      </BaseButton>
      <BaseButton
        variant="sidebar"
        :class="['header-button w-9', {'is-active': editor?.isActive('highlight')}]"
        @click="editor?.chain().focus().toggleHighlight().run()"
        title="Highlight"
      >
        H
      </BaseButton>
      <div class="h-9 border border-stone-200"/>

      <div class="flex">
        <BaseButton
          @click="editor?.chain().focus().toggleHeading({ level: 1 }).run()"
          variant="dropdown"
          :class="['header-button rounded-l-lg w-25', {'is-active': editor?.isActive('heading', { level: 1 })}]">
          Header 1
        </BaseButton>
        <BaseButton variant="dropdown" class="header-button rounded-r-lg w-9" ref="headersRef" @click="isHeadersOpen = !isHeadersOpen">
          \/
        </BaseButton>
      </div>
      <Teleport to="body">
        <div v-if="isHeadersOpen" ref="headersFloating" :style="headersFloatingStyles" class="border border-stone-200 rounded-lg p-px w-34 bg-white">
          <BaseButton
            @click="isHeadersOpen = !isHeadersOpen; editor?.chain().focus().toggleHeading({ level: 1 }).run()"
            variant="sidebar"
            :class="['header-button rounded-l-lg w-full', {'is-active': editor?.isActive('heading', { level: 1 })}]"
          >
            Header 1
          </BaseButton>
          <BaseButton
            @click="isHeadersOpen = !isHeadersOpen; editor?.chain().focus().toggleHeading({ level: 2 }).run()"
            variant="sidebar"
            :class="['header-button rounded-l-lg w-full', {'is-active': editor?.isActive('heading', { level: 2 })}]"
          >
            Header 2
          </BaseButton>
          <BaseButton
            @click="isHeadersOpen = !isHeadersOpen; editor?.chain().focus().toggleHeading({ level: 3 }).run()"
            variant="sidebar"
            :class="['header-button rounded-l-lg w-full', {'is-active': editor?.isActive('heading', { level: 3 })}]"
          >
            Header 3
          </BaseButton>
        </div>
      </Teleport>
      <div class="h-9 border border-stone-200"/>

      <BaseButton
        variant="sidebar"
        :class="['header-button w-9', {'is-active': editor?.isActive('subscript')}]"
        @click="editor?.chain().focus().toggleSubscript().run()"
        title="Subscript"
      >
        X<sub>2</sub>
      </BaseButton>
      <BaseButton
        variant="sidebar"
        :class="['header-button w-9', {'is-active': editor?.isActive('superscript')}]"
        @click="editor?.chain().focus().toggleSuperscript().run()"
        title="Superscript"
      >
        X<sup>2</sup>
      </BaseButton>
      <BaseButton variant="sidebar" class="header-button w-9">
        `
      </BaseButton>
      <BaseButton variant="sidebar" class="header-button w-9">
        >
      </BaseButton>
      <BaseButton variant="sidebar" class="header-button w-9">
        [x]
      </BaseButton>
      <BaseButton variant="sidebar" class="header-button w-30">
        Lists
      </BaseButton>
      
    </div>
  </header>

  <main>
    <div class="bg-stone-100 flex overflow-y-auto custom-scrollbar p-8 flex-1">
      <div class="bg-white min-h-full flex flex-1 border border-stone-200">
        <EditorContent :editor="editor" class="flex-1 flex p-4" />
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
  @apply shrink-0 h-9 flex items-center justify-center
}

:global(.dark) .is-active {
  @apply bg-stone-800
}

:deep(.ProseMirror:focus) {
  @apply outline-none;
}

:deep(.ProseMirror h1) {
  @apply text-3xl font-bold mt-4 mb-2;
}

:deep(.ProseMirror h2) {
  @apply text-2xl font-semibold mt-3.5 mb-1.5;
}

:deep(.ProseMirror h3) {
  @apply text-xl font-semibold mt-3 mb-1;
}
</style>