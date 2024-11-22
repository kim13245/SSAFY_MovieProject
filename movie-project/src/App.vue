<template>
  <head>

  </head>
  <div>
    <Nav />
    <RouterView />
  </div>
  
  </template>

<script setup>
// nav 가져오기
import { RouterLink, RouterView } from 'vue-router';
import Nav from './components/Nav.vue';

// slide
</script>

<style scoped>
/* Nav의 높이를 설정 (예: 60px) */
.Nav {
  height: 60px; 
}
</style>