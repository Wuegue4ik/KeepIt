<script setup lang="ts">
import EditIcon from '../svgs/EditIcon.vue';
import SettingsIcon from '../svgs/SettingsIcon.vue';
import DeleteIcon from '../svgs/DeleteIcon.vue';
import BaseButton from '../buttons/BaseButton.vue';
import { computed } from 'vue';

const props = defineProps<{
  show: boolean
  position?: {top: number, left: number}
}>()

const modalStyle = computed(() => {
  if (!props.position) return {}
  return {
    top: `${props.position.top}px`,
    left: `${props.position.left}px`
  }
})

defineEmits<{
  (e: 'close'): void,
  (e: 'rename'): void,
  (e: 'delete'): void
}>()

</script>

<template>
  <div
    v-if="show"
    class="fixed z-50 bg-white dark:bg-stone-800 shadow-xl rounded-2xl p-2"
    :style="modalStyle"
  >
    <div class="fixed inset-0 -z-10" @click="$emit('close')"/>

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
      <!-- Configure -->
        <BaseButton
          variant="settings"
          class="w-full flex"
          @click="$emit('delete')"
        >
          <SettingsIcon class="w-6 h-5 mr-2"/>
          <span>Configure</span>
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