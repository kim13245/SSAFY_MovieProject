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
                    <RouterLink :to="{name:'home'}">홈</RouterLink>
                </li>
                <li>
                    <RouterLink :to="{name:'mind'}">감정 추천</RouterLink>
                </li>
                <li>
                    <RouterLink :to="{name:'moviesearch'}">영화 검색</RouterLink>
                </li>
                <li>
                    <RouterLink :to="{name:'comunity'}">커뮤니티</RouterLink>
                </li>
                <li>
                    <RouterLink :to="{name:'profile', params:{ user_id: userId || 1 } }">마이 프로필</RouterLink>
                </li>
                <!-- li_center를 끝으로 이동 -->
                <li class="li_center">
                    <div class="button">
                        <a href="">로그인</a>
                    </div>
                    <div class="button SignUp">
                        <a href="">회원가입</a>
                    </div>
                </li>
            </ul>
        </nav>
    </div>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';
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
    color: #141414;
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
    grid-column: 2 / 12; /* 2번째 칸부터 12번째 칸까지 차지 */
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
    width: 130px;
    text-align: center;
    margin-left: 1em;
    border-radius: 8px;
    color: #5e5e64;
}
.SignUp {
    /* background-color: #acacb0 !important; */
}
</style>
