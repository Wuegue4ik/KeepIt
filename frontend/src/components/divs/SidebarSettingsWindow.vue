<script setup lang="ts">
import type { StyleValue } from 'vue';
import EditIcon from '../svgs/EditIcon.vue';
import DeleteIcon from '../svgs/DeleteIcon.vue';
import BaseButton from '../buttons/BaseButton.vue';

const props = defineProps<{
  show: boolean
  style?: StyleValue
}>()

defineEmits<{
  (e: 'close'): void,
  (e: 'rename'): void,
  (e: 'delete'): void,
}>()

</script>

<template>
  <div
    v-if="show"
    class="bg-white dark:bg-stone-800 shadow-xl rounded-2xl p-2"
  >
    <div>
      <!-- Rename -->
        <BaseButton
          variant="settings"
          class="w-full flex"
          @click="$emit('rename')"
        >
          <EditIcon class="w-6 h-5 mr-2"/>
          <span>Rename</span>
        </BaseButton>
      <!-- Delete -->
        <BaseButton
          variant="settings"
          class="w-full flex"
          @click="$emit('delete')"
        >
          <DeleteIcon class="w-6 h-5 mr-2 text-red-600"/>
          <span class="text-red-600">Delete</span>
        </BaseButton>
    </div>
  </div>
</template>