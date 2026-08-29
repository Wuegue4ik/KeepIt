import { ref, computed } from 'vue';
import { defineStore } from 'pinia';
import api from '@/services/api';
import type { Note, NoteOnCreate, PaginatedNotesResponse } from '@/api/types';

export const useNotesStore = defineStore('notes', () => {
  const notes = ref<Note[]>([])
  const isLoading = ref<boolean>(false)
  const isInitialLoading = ref<boolean>(true);
  const isFinished = ref<boolean>(false)

  const currentNote = ref<Note | null>(null)

  const pagination = ref({
    page: 1,
    size: 30,
    total: 0,
    pages: 0
  })

  const error = ref<string | null>(null)
  const totalNotes = computed(() => notes.value.length)

  const storedNotes = computed(() => {
    return[...notes.value].sort((a, b) => {
      return new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
    })
  })

  const channel = new BroadcastChannel('notes_sync_channel')

  channel.onmessage = (ev) => {
    if (ev.data === "sync_notes") {
      resetNotes()
    }
  }

  const syncNotes = () => {
    channel.postMessage("sync_notes")
  }

  const fetchNoteById = async(id: number) => {
    const existingNote = notes.value.find(n => n.id === id)
    if (existingNote) {
      currentNote.value = existingNote
      return existingNote
    }
    isLoading.value = true

    try {
      const response = await api.get<Note>(`/notes/${id}`)
      currentNote.value = response.data
      return response.data
    } catch (err) {
      console.error("Error fetching note by id:", err)
      error.value = "Failed to load the selected note"
      return null
    } finally {
      isLoading.value = false
    }
  }

  const fetchNextNotes = async () => {
    if (isLoading.value || isFinished.value) return;

    isLoading.value = true;
    error.value = null;

    try {
      const response = await api.get<PaginatedNotesResponse>('/notes', {
        params: {
          page: pagination.value.page,
          size: pagination.value.size
        }
      });

      const { items, total, pages } = response.data;

      notes.value.push(...items);
      pagination.value.total = total;
      pagination.value.pages = pages;

      if (pages === 0 || pagination.value.page >= pages) {
        isFinished.value = true;
      } else {
        pagination.value.page++;
      }
    } catch (err: any) {
      console.error('Error retrieving notes:', err);
      error.value = 'Failed to load notes from the server!';
    } finally {
      isLoading.value = false;
      isInitialLoading.value = false;
    }
  };

  const resetNotes = async () => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await api.get<PaginatedNotesResponse>('/notes', {
        params: {
          page: 1,
          size: pagination.value.size
        }
      });

      notes.value = response.data.items;
      pagination.value.total = response.data.total;
      pagination.value.pages = response.data.pages;

      if (response.data.pages <= 1) {
        isFinished.value = true;
      } else {
        pagination.value.page = 2;
        isFinished.value = false;
      }
    } catch (err: any) {
      console.error('Error resetting notes:', err);
      error.value = 'Failed to reset notes';
    } finally {
      isLoading.value = false;
      isInitialLoading.value = false;
    }
  };

  const addNote = async(newNoteData: NoteOnCreate) => {
    error.value = null
    
    try {
      const response = await api.post<Note>("/notes", newNoteData)
      notes.value.unshift(response.data)
      syncNotes()
    } catch (err: any) {
      console.error("Error adding note:", err)
      error.value = "Failed to add new note!"
      throw err
    }
  }

  const editNote = async(noteId: number, noteData: NoteOnCreate) => {
    error.value = null

    try {
      const response = await api.put<Note>(`/notes/${noteId}`, noteData)
      const index = notes.value.findIndex(note => note.id === noteId)
      if (index !== -1) {
        notes.value[index] = response.data
      }
      syncNotes()
    } catch (err: any) {
      console.error("Error editing note:", err)
      error.value = "Failed to edit note!"
      throw err
    }
  }

  const deleteNote = async (noteId: number | undefined) => {
    if (!noteId) return;
    error.value = null;

    try {
      await api.delete(`/notes/${noteId}`);
      notes.value = notes.value.filter(note => note.id !== noteId);
      syncNotes();
    } catch (err: any) {
      console.error('Error deleting note:', err);
      error.value = 'Failed to delete note!';
      throw err;
    }

    if (currentNote.value?.id === noteId) {
      currentNote.value = null;
    }
  };

  return {
    notes,
    currentNote,
    storedNotes,
    isLoading,
    isInitialLoading,
    isFinished,
    error,
    totalNotes,
    pagination,
    fetchNoteById,
    fetchNextNotes,
    resetNotes,
    addNote,
    editNote,
    deleteNote
  }
})