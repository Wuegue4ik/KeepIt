<script setup lang="ts">
import SidebarIcon from '../svgs/SidebarIcon.vue';
import BaseButton from '../buttons/BaseButton.vue';
import SidebarButton from '../buttons/SidebarButton.vue';
import SidebarSettingsWindow from './SidebarSettingsWindow.vue';
import { ref, onMounted } from 'vue';
import { useNotesStore } from '@/stores/notes.ts';
import { storeToRefs } from 'pinia';
import NoteDeletionWindow from './NoteDeletionWindow.vue';
import { toast } from 'vue3-toastify';
import { onClickOutside } from '@vueuse/core'
import { useFloating, offset, flip, shift, autoUpdate } from '@floating-ui/vue'

const isModalOpen = defineModel<boolean>('is-modal-open', { required: true });
const isDeleteModalOpen = defineModel<boolean>('is-delete-modal-open', { required: true });
const selectedNoteId = ref<number>();
const selectedNoteHeader = ref<string>('');

const notesStore = useNotesStore();
const { error, isLoading, isFinished, storedNotes } = storeToRefs(notesStore);
const { fetchNextNotes, deleteNote } = notesStore;
const show = defineModel<boolean>('show', { required: true });

const settingsRef = ref<HTMLElement | null>(null)
const settingsFloating = ref<HTMLElement | null>(null)
const { floatingStyles: settingsFloatingStyles } = useFloating(settingsRef, settingsFloating, {
  strategy: 'fixed',
  placement: 'bottom-start',
  whileElementsMounted: autoUpdate,
  middleware: [
    offset(6),
    flip(),
    shift({ padding: 8 })
  ]
})

const handleDeleteClick = () => {
  isDeleteModalOpen.value = true;
  isModalOpen.value = false;
};

const tryToDeleteNote = () => {
  try {
    const noteId = selectedNoteId.value;
    deleteNote(noteId);
    isDeleteModalOpen.value = false;
    toast.success("Note successfully deleted.");
  } catch (err: any) {
    console.error("Error deleting note:", err);
  }
};

const handleSettingsClick = (noteId: number, noteHeader: string, event: MouseEvent) => {
  settingsRef.value = event.currentTarget as HTMLElement;

  selectedNoteId.value = noteId;
  selectedNoteHeader.value = noteHeader;

  isModalOpen.value = true;
};

defineEmits<{
  (e: 'new-note-click'): void,
  (e: 'search-click'): void
}>();

onClickOutside(settingsFloating, () => {
  isModalOpen.value = false;
})

onMounted(() => {
  if (storedNotes.value.length === 0) {
    fetchNextNotes();
  }
});
</script>

<template>
  <Teleport to="body">
    <div 
      class="fixed top-0 left-0 w-full h-full bg-black/20 dark:bg-stone-200/5 transition-all duration-300 z-10" 
      :class="show ? 'opacity-100' : 'opacity-0 pointer-events-none'" 
      @click="show = !show"
    />

    <aside
      class="p-1 pr-0 fixed flex flex-col top-0 h-full w-72 shadow-2xl z-30 bg-stone-100 dark:bg-stone-900 border-r border-stone-300 dark:border-stone-700 transition-all duration-200"
      :class="show ? 'translate-x-0' : '-translate-x-72 bg-white/5 dark:bg-black/5 border-stone-300/5 dark:border-stone-700/5'"
    >
      <div class="flex mb-2">
        <BaseButton variant="sidebar" @click="show = !show">
          <SidebarIcon/>
        </BaseButton>
      </div>

      <div class="p-1.5 mb-2">
        <!-- New Note Button -->
        <button
          @click="$emit('new-note-click')"
          :class="[
            'mb-2 group relative w-full overflow-hidden rounded-full bg-white dark:bg-stone-800 p-0.5 text-stone-900 dark:text-stone-100 shadow dark:shadow-stone-700/50 transition-all duration-200 ease-out hover:shadow-lg dark:hover:bg-stone-700', 
            (isLoading || error) ? 'cursor-not-allowed pointer-events-none opacity-50' : ''
          ]"
        >
          <div class="relative flex w-full cursor-pointer items-center justify-center p-2">
            <span class="font-medium transition-transform duration-200 ease-out group-hover:-translate-x-6 select-none">
              New note
            </span>
            <span class="absolute right-3 opacity-0 translate-x-4 pointer-events-none transition-all duration-200 ease-out group-hover:opacity-100 group-hover:translate-x-0 select-none">
              <span class="inline-flex items-center rounded-lg border border-stone-200 dark:border-stone-700 bg-stone-50 dark:bg-stone-800 px-2 py-0.5 text-xs text-stone-500 dark:text-stone-400 shadow-sm dark:shadow-none">
                <kbd class="font-sans font-semibold">Ctrl</kbd>
                <span class="mx-1 text-stone-400 dark:text-stone-500">+</span>
                <kbd class="font-sans font-semibold">J</kbd>
              </span>
            </span>
          </div>
        </button>

        <!-- Search Button -->
        <!-- <button
          @click="$emit('search-click')"
          :class="[
            'mb-2 group relative w-full overflow-hidden rounded-full bg-white dark:bg-stone-800 p-0.5 text-stone-900 dark:text-stone-100 shadow dark:shadow-stone-700/50 transition-all duration-200 ease-out hover:shadow-lg dark:hover:bg-stone-700', 
            (isLoading || error) ? 'cursor-not-allowed pointer-events-none opacity-50' : ''
          ]"
        >
          <div class="relative flex w-full cursor-pointer items-center justify-center p-2">
            <span class="font-medium transition-transform duration-200 ease-out group-hover:-translate-x-6 select-none">
              Search
            </span>
            <span class="absolute right-3 opacity-0 translate-x-4 pointer-events-none transition-all duration-200 ease-out group-hover:opacity-100 group-hover:translate-x-0 select-none">
              <span class="inline-flex items-center rounded-lg border border-stone-200 dark:border-stone-700 bg-stone-50 dark:bg-stone-800 px-2 py-0.5 text-xs text-stone-500 dark:text-stone-400 shadow-sm dark:shadow-none">
                <kbd class="font-sans font-semibold">Ctrl</kbd>
                <span class="mx-1 text-stone-400 dark:text-stone-500">+</span>
                <kbd class="font-sans font-semibold">K</kbd>
              </span>
            </span>
          </div>
        </button> -->
      </div>

      <div class="overflow-y-auto custom-scrollbar flex-1 pr-1">
        
        <div v-if="isLoading && storedNotes.length === 0" class="p-2 text-center">
          <div class="p-3 bg-sky-50 dark:bg-sky-950/40 border border-sky-200 dark:border-sky-900/50 rounded-xl">
            <p class="text-xs font-semibold text-sky-600 dark:text-sky-400 mb-1">Loading...</p>
            <p class="text-[11px] text-sky-500/80 dark:text-sky-400/70 truncate">Fetching your notes</p>
          </div>
        </div>

        <div v-else-if="error" class="p-2 text-center">
          <div class="p-3 bg-rose-50 dark:bg-rose-950/40 border border-rose-200 dark:border-rose-900/50 rounded-xl">
            <p class="text-xs font-semibold text-rose-600 dark:text-rose-400 mb-1">An error occurred!</p>
            <p class="text-[11px] text-rose-500/80 dark:text-rose-400/70 truncate">{{ error }}</p>
          </div>
        </div>

        <div v-else-if="storedNotes.length > 0">
          <SidebarButton
            v-for="note in storedNotes"
            :key="note.id"
            @settings-click="handleSettingsClick(note.id, note.header, $event)"
          >
            {{ note.header }}
          </SidebarButton>

          <div v-if="!isFinished" class="p-2 text-center">
            <button
              @click="fetchNextNotes"
              :class="[
                'mb-2 relative w-full overflow-hidden rounded-full bg-white dark:bg-stone-800 p-0.5 text-stone-900 dark:text-stone-100 shadow dark:shadow-stone-700/50 transition-all duration-200 ease-out hover:shadow-lg dark:hover:bg-stone-700', 
                (isLoading || error) ? 'cursor-not-allowed pointer-events-none opacity-50' : ''
              ]"
            >
              <div class="relative flex w-full cursor-pointer items-center justify-center p-2">
                <span class="font-medium transition-transform duration-200 ease-out select-none">
                  {{ isLoading ? 'Loading...' : 'Load more' }}
                </span>
              </div>
            </button>
          </div>
        </div>

        <div v-else class="empty-state">
          <div class="p-3 bg-stone-50 dark:bg-stone-950/40 border border-stone-200 dark:border-stone-900/50 rounded-xl text-center">
            <p class="text-xs font-semibold text-stone-700 dark:text-stone-200 mb-1">You have no notes.</p>
            <p class="text-[11px] text-stone-600/80 dark:text-stone-200/70 truncate">Make your first one!</p>
          </div>
        </div>

      </div>

      <slot name="bottom"/>
    </aside>

    <!-- Modals -->
    <div 
      v-if="isModalOpen" 
      ref="settingsFloating" 
      :style="settingsFloatingStyles" 
      class="z-50 fixed"
    >
      <SidebarSettingsWindow
        :show="isModalOpen"
        :style="settingsFloatingStyles"
        @close="isModalOpen = false"
        @delete="handleDeleteClick"
      />
    </div>

    <NoteDeletionWindow
      :show="isDeleteModalOpen"
      :note-header="selectedNoteHeader"
      @close="isDeleteModalOpen = false"
      @delete="tryToDeleteNote"
    />
  </Teleport>
</template>