<script setup lang="ts">
import SearchComponent from './components/SearchComponents.vue'
</script>

<template>
  <div class="container">
    <SearchComponent />
  </div>
</template>

<style>
body {
  margin: 0;
  padding: 0;
  background-color: var(--bg-color);
  color: var(--text-color);
  transition: background-color 0.3s, color 0.3s;
}

.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-height: 100vh;
  padding-top: 15vh;
  background-color: var(--bg-color);
  transition: background-color 0.3s;
}
</style>