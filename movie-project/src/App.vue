<template>
  <div class="app">
    <header :class="['nav', { 'scrolled': isScrolled }]">
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
import { ref, onMounted, onUnmounted } from 'vue';
import { RouterView } from 'vue-router';
import Nav from './components/Nav.vue';
import Footer from './components/Footer.vue';

const isScrolled = ref(false);

const handleScroll = () => {
  isScrolled.value = window.scrollY > 0; // 스크롤 위치가 0보다 클 때 true
};

onMounted(() => {
  window.addEventListener('scroll', handleScroll);
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
});
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
  position: fixed; /* 화면에 고정 */
  top: 0; /* 화면의 맨 위에 배치 */
  left: 0; /* 왼쪽으로 붙임 */
  width: 100%; /* 화면 전체 너비를 차지 */
  height: 70px; /* Nav의 높이 */
  z-index: 10; /* 다른 요소 위에 표시되도록 */

  transition: background-color 0.3s ease, box-shadow 0.3s ease; /* 부드러운 전환 */
}
.nav.scrolled {
  background-color: #000d11; /* 스크롤 시 배경색 */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* 스크롤 시 그림자 효과 */
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
