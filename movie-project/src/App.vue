<template>
  <div class="app">
    <header class="nav">
      <Nav />
    </header>

    <main class="content">
      <RouterView />
    </main>

    <footer class="footer">
      <Footer />
    </footer>
  </div>
</template>

<script setup>
import { RouterView } from 'vue-router';
import Nav from './components/Nav.vue';
import Footer from './components/footer.vue';
</script>

<style scoped>
/* Flexbox 레이아웃으로 화면 전체를 채움 */
.app {
  display: flex;
  flex-direction: column;
  min-height: 100vh; /* 전체 화면 높이를 차지 */
}

/* Nav 스타일 */
.nav {
  height: 70px; /* Nav의 높이 */
}

/* 메인 콘텐츠 영역 */
.content {
  flex: 2; /* 남는 공간을 모두 차지 */
}

/* Footer 스타일 */
.footer {
  text-align: center; /* 내용 중앙 정렬 */
}
</style>
