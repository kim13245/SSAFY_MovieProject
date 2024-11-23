<template>
    <div class="container" :style="{ backgroundImage: 'url(' + imageUrl + ')' }">
        <div class="login">
            <div class="login-text">
                <h3>로그인</h3>
                <p style="font-size: 0.8em; color: #C1C1C1;">오신것을 환영합니다.</p>
            </div>
            <form @submit.prevent="LoginCheck">
                <div class="login-username">
                    <input type="text" id="username" v-model.trim="username" class="custom-input" placeholder="아이디를 입력해주세요.">
                </div>
                <div class="login-password">
                    <input type="password" id="password" v-model.trim="password"  class="custom-input" placeholder="비밀번호를 입력해주세요.">
                </div>
                <button type="submit">로그인</button>
            </form>
        </div>

        <div class="login-foter">
            <div>
                <h4>test</h4>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import axios from 'axios';
import { useMovieStore } from '@/stores/movie';
import { useRouter } from 'vue-router';
const store = useMovieStore()
const router = useRouter()
const username = ref(null)
const password = ref(null)

// 로그인 api 요청 
const LoginCheck = function() {
    axios ({
        method:'post',
        url:'http://127.0.0.1:8000/api/v1/accounts/login/',
        data: {
            username:username.value,
            password:password.value
        },
        headers: {
        'Content-Type': 'application/json',  // 헤더 추가
        
        },    
    }).then((res) => {
        const token = res.data.token
        console.log('성공')
        store.Token = res.data[0].token
        store.userId = res.data[1].userId
        console.log(store.userId)
        store.username = res.data[2].userName
        router.push({name:'home'})
    }).catch((err) => {
        console.log('실패:',err)
        alert('로그인 실패')
        username.value = ''
        password.value = ''
    })
}

const imageUrl = ref(null)
// 랜덤 이미지 생성
// 랜덤 영화 이미지 가져오기
const BASE_URL = 'https://api.themoviedb.org/3';
async function getRandomMovieImage() {
  try {

    // 인기 영화 목록 가져오기
    const response = await axios.get(`${BASE_URL}/movie/upcoming?api_key=${store.API_KEY}&language=ko-KR&page=1`)

    // 영화 목록에서 랜덤 영화 선택
    const movies = response.data.results;
    const randomMovie = movies[Math.floor(Math.random() * movies.length)];

    // 영화 배경 이미지 URL 생성
    imageUrl.value = `https://image.tmdb.org/t/p/original${randomMovie.backdrop_path}`;

    return imageUrl;
  } catch (error) {
    console.error('영화 이미지를 가져오는 데 실패했습니다.', error);
  }
}

// 랜덤 영화 이미지를 출력하는 함수 호출
getRandomMovieImage().then((imageUrl) => {
  console.log('랜덤 영화 이미지 URL:', imageUrl);
});

</script>

<style scoped>
.container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: calc(100vh - 60px); /* Nav의 높이를 빼줍니다. */

    background-size: cover; /* 이미지가 전체 영역을 덮도록 */
    background-position: center center; /* 이미지 중앙에 배치 */
    background-repeat: no-repeat; /* 이미지 반복 방지 */
}
.container::before {
    content: ""; 
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(to bottom, rgba(0,13,17, 1), rgba(0,13,17, 0.8) 30%, rgba(0,13,17, 0.5) 50%, rgba(0,13,17, 0.3) 80%, rgba(0,13,17, 0));
    top: 55px; /* Nav의 높이를 고려하여 그라디언트를 60px 아래로 시작 */
    pointer-events: none; 
    z-index: 1;
}
.login {
    width: 300px;

    z-index: 2;
}
.login-text {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-bottom: 0.5em;
}
#username {
    margin-bottom: 0.5em;
}
.custom-input {
    width: 100%;  
    max-width: 400px;  
    padding: 0.8em 1em;  
    font-size: 1em;  
    border: 2px solid #6c757d;  
    border-radius: 8px;  
    background-color: #222;
    color: white;
    outline: none; 
    transition: all 0.3s ease; 
}

.custom-input::placeholder {
    color: #888;  /* 플레이스홀더 텍스트 색상 */
}
.custom-input:hover {
    border-color: #61FBFF;  
    background-color: #333; 
}
.custom-input:hover::placeholder {
    color: #61FBFF;
}

.custom-input:focus {
    border-color: #61FBFF;  
    background-color: #333; 
}

.custom-input:focus::placeholder {
    color: #61FBFF;  
}
button {
    width: 100%;  
    max-width: 400px; 
    padding: 0.8em 1em;  
    margin-top: 1em;
    font-size: 1em; 
    border: 2px solid #6c757d;
    border-radius: 8px;  
    background-color: #222;  
    color: white; 
    outline: none;  
    transition: all 0.3s ease; 
    cursor: pointer;
}
button:hover {
    border-color: #61FBFF;  
    background-color: #61FBFF;  
    color: #000d11;
    font-weight: bold;
}

</style>