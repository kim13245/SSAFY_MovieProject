<template>
    <div>
        <div v-if="userInfo" class="container">
            <div class="user-top-info">
                <div class="background-img">
                    <img src="@/assets/profile/pepole.jpg" alt="Movie Poster" />
                </div>
                <div class="user-profile-master">
                    <div class="user-profile">
                        <div class="user-profile-info">
                            <div class="name">
                                <div class="user-img">
                                    <img src="@/assets/profile/profile-actore.png" alt="profie-img">
                                </div>
                                <div class="name-info">
                                    <h1 style="color: #61FBFF;">{{ userInfo.nickname }}</h1>
                                    <p>{{ userInfo.email }}</p>
                                </div>
                                <div class="follow-info-master">
                                    <div class="follow-info">
                                        <div class="followers">
                                            <p>팔로워</p>
                                            <p> {{ followerscount }} </p>
                                        </div>
                                        <div v-if="userInfo.id === store.userId" class="followings">
                                            <p>팔로잉</p>
                                            <p> {{ followingscount }} </p>
                                        </div>
                                        <div v-if="userInfo.id !== store.userId" class="followings-user" @click.prevent="follow" style="cursor: pointer;">
                                            <p>팔로잉</p>
                                            <p> {{ followingscount }} </p>
                                        </div>
                                        
                                    </div>
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
                </div>
                
            </div>
            <div class="user-bottom">
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
                    <Rivews v-if="isPage === 'Rivews'" :userInfo="userInfo"/>
                    <Comment v-if="isPage === 'Comment'" :userInfo="userInfo"/>
                    <WishMovie v-if="isPage === 'WishMovie'" :userInfo="userInfo"/>
                    <PlayList v-if="isPage === 'PlayList'" :userInfo="userInfo"/>
                    <div class="components">
        
                    </div>
                </div>
            </div>
    
    
            <span @click="out">
                <button>탈퇴다~</button>
            </span>
        </div>
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

// 내가 팔로우 했는제 체크 
const result = ref(false)
const isMyNicknameInFollowers = (followers, myName) => {
  // followers -> 배열
  return followers.includes(myName) ? true : false;
};

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
        if (result.value === false) {
            followerscount.value ++;
            result.value = true
        } else {
            followerscount.value --;
            result.value = false
        }
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

const followerscount = ref(0)
const followingscount = ref(0)
const getUserInfo = function() {
    return axios({
        method: 'get',
        url: `http://127.0.0.1:8000/api/v1/accounts/profile/${route.params.user_id}`,
        headers: {
            Authorization: `Token ${store.Token}`, // 인증 토큰 추가
        },
    })
    .then((res) => {
        console.log(res.data);
        userInfo.value = res.data;
        followerscount.value = userInfo.value.followers_count;
        followingscount.value = userInfo.value.followings_count
        result.value = isMyNicknameInFollowers(res.data.followers_names,store.username)
        console.log(result.value)
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

}
.user-top-info {
    position: relative;
}
.background-img {
    height: 500px; /* 부모 컨테이너의 높이 설정 (전체 화면 기준) */
    overflow: hidden;
    display: flex;
    justify-content: center; /* 가로 중앙 정렬 */
    align-items: center;    /* 세로 중앙 정렬 */
}
.background-img img {
    max-width: 100%;        /* div 너비에 맞게 이미지 크기 조정 */
    object-fit: contain;    /* 이미지 비율 유지하며 전체 표시 */
}
.background-img::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to top, rgba(0,13,17, 1), rgba(0,13,17, 0.8) 50%, rgba(0,13,17, 1));
  pointer-events: none;
  z-index: 1;
}

.user-profile-master {
    position: absolute;

    width: 100%;
    z-index: 2;
    bottom: 80px;
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
    border: 1px solid #323232;
    background-color: #000d11;
    border-radius: 8px;
    padding: 2em 1em;
    box-shadow: 0px 0px 9px rgba(120, 206, 232, 0.4);
}
.user-profile-info {
    width: 100%;
    margin-left: 2em;
    display: flex;
    flex-direction: column;
}
.name {
    display: flex;
    gap: 1em;
    align-items: center;
    margin-bottom: 1.5em;
    padding-bottom: 1.5em;
    border-bottom: 1px solid #323232;
}
.name-info p {
    font-size: 0.8em;
    color: #888;
}
.follow-info {
    display: flex;
    gap: 0.5em;
    height: 100%;
}
.followers {
    display: flex;
    gap: 0.5em;
    background-color: #000d12;
    border: 1px solid #323232;
    padding: 0.5em;
    width: 80px;
    border-radius: 10px;
    align-items: center;
    justify-content: center;
}
.followings {
    display: flex;
    gap: 0.5em;
    background-color: #000d12;
    border: 1px solid #323232;
    padding: 0.5em;
    width: 80px;
    border-radius: 10px;
    align-items: center;
    justify-content: center;
}
.followings-user {
    display: flex;
    gap: 0.5em;
    background-color: #000d12;
    border: 1px solid #323232;
    padding: 0.5em;
    width: 80px;
    border-radius: 10px;
    align-items: center;
    justify-content: center;
}
.followings-user:hover {
    border: 1px solid #61FBFF;
}


@keyframes gradient-move {
    0% {
    background-position: 0% 50%;
    }
    50% {
        background-position: 5  0% 50%;
    }
    100% {
        background-position: 0% 50%;
    }
}

.info-detial {
    display: flex;
    justify-content: space-between;
    width: 100%;
}

.info-detial div {
    width: 32%;
    border: 1px solid #323232;
    border-radius: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0 0.8em;

}
.my-point {
    background: linear-gradient(35deg, #000d12, #61FBFF);
    background-size: 300% 100%; /* 배경 크기 조정 */
    animation: gradient-move 6s infinite; /* 6초 동안 반복 애니메이션 */
}
.user-img {
    width: 100px;
    overflow: hidden;
    border-radius: 200px;
}

/* 하단 */
.user-bottom {
    display: grid;
    grid-template-rows: auto auto;
    grid-template-columns: 1fr repeat(10,1fr) 1fr;
}
.user-file {
    grid-column: 4/10;
    grid-row: 1;
}
.buttons {
    margin-top: 10px;
    margin-bottom: 2em;
    padding-bottom: 1em;
    border-bottom: 1px solid #323232;
}
.buttons ul {
    display: flex;
    gap: 1em;
}
.buttons ul li {
    background-color: #000d12;
    border: 1px solid #323232;
    min-width: 150px;
    border-radius: 50px;
    text-align: center;
    padding: 0.5em 1em;
    cursor: pointer;
}
.buttons ul li:hover {
    border: 1px solid #61FBFF;
    box-shadow: 0px 0px 9px rgba(120, 206, 232, 0.802);
}
/* 클릭된 항목에 대해 배경 색상 변경 */
.buttons ul li.active {
    background-color: #61FBFF; 
    color: #000d12; 
    font-weight: bold;
}
</style>