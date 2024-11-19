<template>
    <div>
        <nav>
            <ul>
                <li>
                    <div class="img">
                        <RouterLink :to="{name:'home'}">
                            <img src="@/assets/logo/testLogo.jpg" alt="test_img">
                        </RouterLink>
                    </div>
                </li>
                <li>
                    <RouterLink :to="{name:'home'}" class="navTag">홈</RouterLink>
                </li>
                <li>
                    <RouterLink :to="{name:'mind'}" class="navTag">감정 추천</RouterLink>
                </li>
                <li>
                    <RouterLink :to="{name:'moviesearch'}" class="navTag">영화 검색</RouterLink>
                </li>
                <li>
                    <RouterLink :to="{name:'comunity'}" class="navTag">커뮤니티</RouterLink>
                </li>
                <li>
                    <RouterLink :to="{name:'profile', params:{ user_id: userId || 1 } }" class="navTag">마이 프로필</RouterLink>
                </li>
                <!-- li_center를 끝으로 이동 -->
                <li class="li_center">
                    <div v-if="!isLoggedIn">
                        <div class="button">
                            <RouterLink :to="{name:'login'}">로그인</RouterLink>
                        </div>
                        <div class="button SignUp">
                            <a href="">회원가입</a>
                        </div>
                    </div>
                    <div v-else>
                        <div class="button">
                            <RouterLink :to="{name:'login'}">로그아웃</RouterLink>
                        </div>
                    </div>
                </li>
            </ul>
        </nav>
    </div>
</template>

<script setup>
import { useMovieStore } from '@/stores/movie';
import { onMounted,ref,computed } from 'vue';
import { RouterLink, RouterView } from 'vue-router';
import axios from 'axios';
const store = useMovieStore()

// 로그인 상태 체크!
// 페이지 로드 시 로그인 상태 확인
const isLoggedIn = computed(() => !!store.Token)

// 로그아웃
const logout = function() {
    axios ({
        method:'delete',
        url:'http://127.0.0.1:8000/api/v1/accounts/logout/',
    }).then((res) => {
        console.log('로그아웃')
    }).catch((err) => {
        console.error(err)
    })
    store.Token = null
    alert('로그아웃 되었습니다.')
}

</script>

<style scoped>
nav {
    background-color: f9f9f9;
    border-bottom: 1px solid #00000026;
    padding: 1em;

    /* 그리드 */
    display: grid;
    grid-template-columns: 1fr repeat(10, 1fr) 1fr; /* 양옆에 1등분씩 여백, 가운데 10등분 */
    gap: 0;
    padding: 0;
    width: 100%;
}

a {
    font-size: 1em;
    font-weight: 400;
    color: #656565;
    transition: color 0.3s ease; /* 색상 변경을 부드럽게 0.3초 동안 */
}

.navTag:hover {
    color: #222; /* 마우스를 올렸을 때 변경할 색상 (예: 토마토색) */
    font-weight: 600;
}

.img {
    margin-right: 2em;
}

img {
    width: 131px;
}

ul {
    display: flex; /* 가로 정렬 */
    list-style: none; /* 기본 불릿 제거 */
    align-items: center;
    margin: 0;
    padding: 0;
    gap: 2em; /* 항목 간 간격 (선택 사항) */
    grid-column: 4 / 10; /* 2번째 칸부터 12번째 칸까지 차지 */
    width: 100%;
}

.li_center {
    margin-left: auto; /* 오른쪽 끝으로 밀기 */
    display: flex; /* flexbox로 설정 */
    flex-wrap: wrap;
}

.button {
    border: 1px solid #7e7e7e;
    padding: 0.3em;
    width: 110px;
    text-align: center;
    margin-left: 1em;
    border-radius: 8px;
    color: #5e5e64;
}
.button:hover {
    background-color:#acacac ;
    color: white;
}
.button:hover a {
    color: white; /* 호버 시 텍스트 색상 변경 */
}








/* 반응형 작업 */
@media screen and (max-width: 1920px) {
    ul {
        grid-column: 3 / 11; /* 2번째 칸부터 12번째 칸까지 차지 */
        gap: 1em; /* 항목 간 간격 (선택 사항) */
    }
}
</style>
