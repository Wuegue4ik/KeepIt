import { ref, computed } from 'vue';
import { defineStore } from 'pinia';
import api from '@/services/api';
import type { Note, NoteOnCreate } from '@/api/types';

export const useNotesStore = defineStore('notes', () => {
  const notes = ref<Note[]>([])
  const isLoading = ref<boolean>(false)
  const error = ref<string | null>(null)
  const totalNotes = computed(() => notes.value.length)

  const fetchNotes = async() => {
    isLoading.value = true
    error.value = null

    try {
      const response = await api.get<Note[]>("/notes")
      notes.value = response.data
    } catch (err: any) {
      console.error("Error retrieving notes:", err)
      error.value = "Failed to load notes from the server!"
    } finally {
      isLoading.value = false
    }
  }

  const addNote = async(newNoteData: NoteOnCreate) => {
    error.value = null
    
    try {
      const response = await api.post<Note>("/notes", newNoteData)
      notes.value.unshift(response.data)
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
    } catch (err: any) {
      console.error("Error editing note:", err)
      error.value = "Failed to edit note!"
      throw err
    }
  }

  const deleteNote = async (noteId: number | undefined) => {
    error.value = null

    try {
      await api.delete(`/notes/${noteId}`)
      notes.value = notes.value.filter(note => note.id !== noteId)
    } catch (err: any) {
      console.error("Error deleting note:", err)
      error.value = "Failed to delete note!"
    }
  }

  return {
    notes,
    isLoading,
    error,
    totalNotes,
    fetchNotes,
    addNote,
    editNote,
    deleteNote
  }
})