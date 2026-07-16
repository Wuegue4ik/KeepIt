<script setup lang="ts">
import { RouterView } from 'vue-router'
</script>

<template>
<header class="app-header">
  <h1>KeepIt</h1>
</header>

<main class="app-content">
  <RouterView />
</main>
</template>

<style scoped>
.app-header {
  background-color: #2c3e50;
  color: white;
  padding: 1.5rem;
  text-align: center;
}

.app-content {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1rem;
}
</style>
