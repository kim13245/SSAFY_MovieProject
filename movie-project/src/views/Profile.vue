<template>
    <div v-if="userInfo" class="container">
        <div class="user-profile">
            <div class="user-img">
                <img src="@/assets/profile/profile-actore.png" alt="profie-img">
            </div>
            <div class="user-profile-info">
                <div class="name">
                    <div class="name-info">
                        <h1>{{ userInfo.nickname }}</h1>
                        <h4>{{ userInfo.email }}</h4>
                    </div>
                    <div class="follow-info">
                        <div class="followers">
                            <p>팔로워</p>
                            <p> {{ userInfo.followers_count }} </p>
                        </div>
                        <div class="followings">
                            <p>팔로잉</p>
                            <p> {{ userInfo.followings_count }} </p>
                        </div>
                        <button @click.prevent="follow">click</button>
                    </div>
                </div>
                <div class="info-detial">
                    <div class="my-point">
                        <p>나의 평가 개수</p>
                        <h1>{{ userInfo.review_count }}</h1>
                    </div>
                    <div class="my-score">
                        <p>나의 평균 점수</p>
                        <h1>{{ (userInfo.rating_average).toFixed(1) }}</h1>
                    </div>
                    <div class="my-count">
                        <p>내가 보고싶은 영화</p>
                        <h1>{{ userInfo.kept_movies_count }}</h1>
                    </div>
                </div>
            </div>
        </div>
        <div class="user-file">
            <div class="buttons" v-if="userInfo">
                <ul>
                    <li 
                        @click="isPage='Rivews'"
                        :class="{ 'active': isPage === 'Rivews' }">리뷰</li>
                    <li 
                        @click="isPage='Comment'"
                        :class="{ 'active': isPage === 'Comment' }">코멘트</li>
                    <li 
                        @click="isPage='WishMovie'"
                        :class="{ 'active': isPage === 'WishMovie' }">보고싶은 영화</li>
                    <li 
                        @click="isPage='PlayList'"
                        :class="{ 'active': isPage === 'PlayList' }">플레이 리스트</li>
                </ul>
            </div>
            <hr>
            <Rivews v-if="isPage === 'Rivews'" :userInfo="userInfo"/>
            <Comment v-if="isPage === 'Comment'" :userInfo="userInfo"/>
            <WishMovie v-if="isPage === 'WishMovie'" :userInfo="userInfo"/>
            <PlayList v-if="isPage === 'PlayList'" :userInfo="userInfo"/>
            <hr>
            <div class="components">

            </div>
        </div>


        <span @click="out">
            <button>탈퇴다~</button>
        </span>
    </div>
</template>

<script setup>

import Comment from '@/components/profile/Comment.vue';
import PlayList from '@/components/profile/PlayList.vue';
import Rivews from '@/components/profile/Rivews.vue';
import WishMovie from '@/components/profile/WishMovie.vue';
import { useMovieStore } from '@/stores/movie';
import axios from 'axios';
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute()

const store = useMovieStore()
const router = useRouter()
const userInfo = ref(null)
// 페이지 전환
const isPage = ref('Rivews')

// test 팔로워 팔로잉
const follow = function() {
    axios({
        method:'post',
        url:`http://127.0.0.1:8000/api/v1/accounts/users/${route.params.user_id}/follow`,
        headers: {
            Authorization: `Token ${store.Token}`, // 인증 토큰 추가
        },
    }).then(() => {
        console.log('성공s')
    }).catch((err) => {
        console.error(err)
    })
}

const out = function() {
    axios({
        method:'delete',
        url:'http://127.0.0.1:8000/api/v1/accounts/signout/',
        headers: {
            Authorization: `Token ${store.Token}`, // 인증 토큰 추가
        },
    }).then((res) => {
        alert('탈퇴 성공')
        console.log('check')
        router.push({name:'home'})
        store.Token = null
    }).catch((err) => {
        console.log(err)
        // 로그아웃도
    })
}

const getUserInfo = function() {
    return axios({
        method: 'get',
        url: `http://127.0.0.1:8000/api/v1/accounts/profile/${route.params.user_id}`,
        headers: {
            Authorization: `Token ${store.Token}`, // 인증 토큰 추가
        },
    })
    .then((res) => {
        console.log(res);
        userInfo.value = res.data;
    })
    .catch((err) => {
        console.error(err);
    });
}


onMounted(async () => {
    try {
        await getUserInfo();
    } catch (err) {
        console.error("Error occurred while fetching user info:", err);
    }
});




//  버튼 클릭 유무 체크 

</script>

<style scoped>
.container {
    display: grid;
    grid-template-rows: auto auto;
    grid-template-columns: 1fr repeat(10,1fr) 1fr;
}
.user-profile {

    grid-column: 4/10;
    grid-row: 1;
    display: flex;
    align-items: center;
    width: 100%;
}
.user-profile-info {
    width: 100%;
    margin-left: 2em;
}
.name {
    display: flex;
    gap: 1em;
    align-items: center;
    
}
.follow-info {
    display: flex;
    gap: 1em;
    height: 100%;
}
.follow-info div {
    display: flex;
    gap: 0.5em;
    background-color: gray;
    padding: 0.5em;
    width: 80px;
    border-radius: 8px;
}
.info-detial {
    display: flex;
    justify-content: space-between;
}
.info-detial div {
    width: 30%;
    background-color: gray;
    border-radius: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 0.8em;
}
.user-img {
    width: 200px;
    overflow: hidden;
    border-radius: 200px;
}

/* 하단 */
.user-file {
    grid-column: 4/10;
    grid-row: 2;
}
.buttons {
    margin-top: 50px;
}
.buttons ul {
    display: flex;
    gap: 1em;
}
.buttons ul li {
    background-color: gray;
    min-width: 150px;
    border-radius: 50px;
    text-align: center;
    padding: 0.5em 1em;
    cursor: pointer;
}
/* 클릭된 항목에 대해 배경 색상 변경 */
.buttons ul li.active {
    background-color: #4CAF50; /* 예시로 활성화된 항목의 배경을 녹색으로 설정 */
    color: white; /* 글자 색을 흰색으로 변경 */
}
</style>