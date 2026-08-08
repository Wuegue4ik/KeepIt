<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { storeToRefs } from 'pinia';
import { useNotesStore } from '@/stores/notes';
import NoteModal from '@/components/NoteModal.vue';

const notesStore = useNotesStore()

const { notes, error, isLoading, totalNotes } = storeToRefs(notesStore)
const { fetchNotes, deleteNote } = notesStore

const isModalOpen = ref(false)
const selectedNote = ref<any | null>(null)

const openCreateModal = () => {
  selectedNote.value = null
  isModalOpen.value = true
}

const openEditModal = (note: any) => {
  selectedNote.value = note
  isModalOpen.value = true
}

onMounted(() => {
  fetchNotes()
})
</script>

<template>
  <div class="container">
    <header class="home-header">
      <h2>Мои заметки (Всего: {{ totalNotes }})</h2>
      <button @click="openCreateModal" class="btn-create">Новая заметка</button>
    </header>

    <div v-if="isLoading" class="status-message">
      ⏳ Загрузка заметок из базы данных...
    </div>

    <div v-else-if="error" class="error-message">
      ❌ {{ error }}
    </div>

    <div v-else class="notes-grid">
      <div v-if="notes.length === 0" class="empty-state">
        Заметок нет. Напиши что-нибудь!
      </div>

      <div v-for="note in notes" :key="note.id" class="note-card">
        <div class="card-top">
          <h3>{{ note.header }}</h3>
          <button @click="openEditModal(note)" class="btn-edit" title="Редактировать">
            R
          </button>
          <button @click="deleteNote(note.id)" class="delete-btn" title="Удалить заметку">
            🗑️
          </button>
        </div>
        
        <p class="note-text">{{ note.text || 'Нет описания' }}</p>

        <div v-if="note.tags?.length" class="tags">
          <span v-for="tag in note.tags" :key="tag.id" class="tag-badge">
            #{{ tag.name }}
          </span>
        </div>
      </div>
    </div>
    <NoteModal v-if="isModalOpen" :noteToEdit="selectedNote" @close="isModalOpen = false"/>
  </div>
</template>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  font-family: Arial, sans-serif;
}
.home-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2px solid #eee;
  padding-bottom: 1rem;
  margin-bottom: 2rem;
}
.status-message {
  text-align: center;
  color: #666;
  font-size: 1.2rem;
  margin-top: 2rem;
}
.error-message {
  text-align: center;
  color: #d32f2f;
  background: #ffebee;
  padding: 1rem;
  border-radius: 8px;
  margin-top: 2rem;
}
.notes-grid {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
.note-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1.5rem;
  background: #fff;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}
.card-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.card-top h3 {
  margin: 0;
  color: #2c3e50;
}
.delete-btn {
  background: none;
  border: none;
  font-size: 1.2rem;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: background 0.2s;
}
.delete-btn:hover {
  background: #f5f5f5;
}
.note-text {
  color: #555;
  line-height: 1.5;
  margin: 1rem 0;
}
.tags {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}
.tag-badge {
  background: #e0f2f1;
  color: #00796b;
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: bold;
}
.empty-state {
  text-align: center;
  color: #999;
  font-size: 1.1rem;
  margin-top: 3rem;
}
.card-actions {
  display: flex;
  gap: 0.25rem;
}
.btn-edit {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.1rem;
  padding: 0.25rem;
  border-radius: 6px;
  transition: background 0.2s;
  line-height: 1;
}
.btn-edit:hover {
  background-color: #ebf8ff;
}
</style>