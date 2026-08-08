<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { useNotesStore } from '@/stores/notes';
import type { Note, NoteOnCreate } from '@/api/types';

const props = defineProps<{
  noteToEdit?: Note | null
}>()

const emit = defineEmits(['close'])

const notesStore = useNotesStore()
const isSubmitting = ref(false)
const localError = ref<string | null>(null)

const formData = reactive({
  header: '',
  text: '',
  tagsString: ''
})

onMounted(() => {
  if (props.noteToEdit) {
    formData.header = props.noteToEdit.header
    formData.text = props.noteToEdit.text || ''

    if (props.noteToEdit.tags && props.noteToEdit.tags.length > 0) {
      formData.tagsString = props.noteToEdit.tags.map(t => t.name).join(', ')
    }
  }
})

const handleSubmit = async() => {
  if (!formData.header.trim()) {
    localError.value = "Header must be not null!"
    return
  }

  isSubmitting.value = true
  localError.value = null

  try {
    const parseTags: string[] = formData.tagsString
      .split(',')
      .map(tag => tag.trim())
      .filter(tag => tag.length > 0)

    const payload = {
      header: formData.header.trim(),
      text: formData.text.trim() || null,
      tags: parseTags
    }

    if (props.noteToEdit) {
      await notesStore.editNote(props.noteToEdit.id, payload)
    } else {
      await notesStore.addNote(payload)
    }

    emit('close')
  } catch (err: any) {
    localError.value = err.response?.data?.detail || "Не удалось сохранить заметку."
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
<div class="modal-backdrop" @click.self="emit('close')">
    <div class="modal-content">
      <header class="modal-header">
        <h3>Новая заметка</h3>
        <button class="btn-close-x" @click="emit('close')">✕</button>
      </header>

      <form @submit.prevent="handleSubmit" class="modal-form">
        <div v-if="localError" class="form-error">
          ⚠️ {{ localError }}
        </div>

        <div class="form-group">
          <label for="header">Заголовок *</label>
          <input 
            id="header"
            v-model="formData.header" 
            type="text" 
            placeholder="Введите название заметки..."
            maxlength="50"
            :disabled="isSubmitting"
          />
        </div>

        <div class="form-group">
          <label for="text">Текст заметки</label>
          <textarea 
            id="text"
            v-model="formData.text" 
            placeholder="Напишите что-нибудь умное..."
            rows="5"
            :disabled="isSubmitting"
          ></textarea>
        </div>

        <div class="form-group">
          <label for="tags">Теги (через запятую)</label>
          <input 
            id="tags"
            v-model="formData.tagsString" 
            type="text" 
            placeholder="например: учеба, python, важные дела"
            :disabled="isSubmitting"
          />
        </div>

        <footer class="modal-footer">
          <button type="button" class="btn-cancel" @click="emit('close')" :disabled="isSubmitting">
            Отмена
          </button>
          <button type="submit" class="btn-submit" :disabled="isSubmitting">
            {{ isSubmitting ? 'Сохранение...' : 'Создать заметку' }}
          </button>
        </footer>
      </form>
    </div>
  </div>
</template>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  width: 100%;
  max-width: 500px;
  border-radius: 12px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  display: flex;
  flex-direction: column;
  animation: scaleUp 0.15s ease-out;
}

@keyframes scaleUp {
  from { transform: scale(0.95); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

.modal-header {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #edf2f7;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  color: #1a202c;
  font-size: 1.25rem;
}

.btn-close-x {
  background: none;
  border: none;
  font-size: 1.2rem;
  color: #718096;
  cursor: pointer;
}

.modal-form {
  padding: 1.5rem;
}

.form-error {
  background-color: #fff5f5;
  color: #c53030;
  padding: 0.75rem;
  border-radius: 6px;
  margin-bottom: 1rem;
  font-size: 0.9rem;
  border: 1px solid #fed7d7;
}

.form-group {
  margin-bottom: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.form-group label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #4a5568;
}

.form-group input, .form-group textarea {
  padding: 0.6rem 0.75rem;
  border: 1px solid #cbd5e0;
  border-radius: 6px;
  font-size: 0.95rem;
  font-family: inherit;
  transition: border-color 0.2s;
}

.form-group input:focus, .form-group textarea:focus {
  outline: none;
  border-color: #42b983;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 1.75rem;
}

.btn-cancel {
  background-color: #edf2f7;
  color: #4a5568;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
}

.btn-cancel:hover {
  background-color: #e2e8f0;
}

.btn-submit {
  background-color: #42b983;
  color: white;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
}

.btn-submit:hover {
  background-color: #3aa876;
}

.btn-submit:disabled, .btn-cancel:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>