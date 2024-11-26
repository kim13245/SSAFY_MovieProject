<template>
    <div class="container">
        <div class="answer" :style="{ marginTop: answerMarginTop }">
            <TransitionGroup 
                name="message"
                enter-active-class="animate-enter"
                enter-from-class="enter-from"
                enter-to-class="enter-to"
            >
                <div v-if="question" class="my-q">
                    <p>{{ question }}</p>
                </div>
                <div v-show="isLoading" class="ai-q loading" :key="'loading'">
                    <p>당신의 감정을 분석중입니다...</p>
                </div>
                <div v-if="answer" class="ai-q" :key="'a'+answer.openai_response">
                    <p>{{ answer.openai_response }}</p>
                </div>
                <div class="movie-post" v-if="answer" @click="goDetail(movie.id)">
                    <div v-if="imageUrl">
                        <img :src="imageUrl" alt="postr-img">
                    </div>
                    <p v-if="imageUrl">{{ movie.title }}</p>
                    <div style="display: flex; flex-direction: column; border: none;">
                        <p v-if="!imageUrl" class="next-title">'<span style="font-weight: 600; text-decoration: underline;">{{ answer.recommend }}</span>'<br>
                        을 추천합니다. <br> 
                        </p>
                        <span v-if="!imageUrl" style="color: #777; font-size: 0.9em; line-height: 1; margin-top: 0.8em;">해당 영화는 현재 TMDB DB에 등록되어 있지 않습니다.</span>
                    </div>
                </div>
                <div class="form-area" v-show="formview">
                    <form @submit.prevent="getApi" class="form">
                        <input type="text" v-model.trim="question" class="custom-input" placeholder="오늘 하루는 어떤 하루였나요?">
                        <button type="submit" class="button">질문하기</button>
                    </form>
                </div>
                
            </TransitionGroup>
        </div>
        <div class="componentsMind">
            <Base v-if="checkComponents === 'base'"/>
            <Angry v-if="checkComponents === 'Angry'"/>
            <Anxious v-if="checkComponents === 'Anxious'" />
            <Depressed v-if="checkComponents === 'Depressed'" />
            <Excited v-if="checkComponents === 'Excited'" />
            <Happy v-if="checkComponents === 'Happy'" />
            <Helpless v-if="checkComponents === 'Helpless'" />
            <Relaxed v-if="checkComponents === 'Relaxed'" />
            <Tired v-if="checkComponents === 'Tired'" />
        </div>
    </div>
</template>

<script setup>
import axios from 'axios';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
//페이지 임포트
import Angry from '@/components/Mind/Angry.vue';
import Anxious from '@/components/Mind/Anxious.vue';
import Depressed from '@/components/Mind/Depressed.vue';
import Excited from '@/components/Mind/Excited.vue';
import Happy from '@/components/Mind/Happy.vue';
import Helpless from '@/components/Mind/Helpless.vue';
import Relaxed from '@/components/Mind/Relaxed.vue';
import Tired from '@/components/Mind/Tired.vue';
import Base from '@/components/Mind/Base.vue';

const formview = ref(true)
const question = ref(null)
const answer = ref(null)
const isLoading = ref(false)
const movies = ref(null)
const movie = ref(null)
const Base_URL = 'https://image.tmdb.org/t/p/original'
const imageUrl = ref(null)
const router = useRouter()
const checkComponents = ref('')
const getSearch = async (moviename) => {
    try {
        const res = await axios({
            method: 'get',
            url: `http://127.0.0.1:8000/api/v1/movies/movie_search/`,
            params: { title: moviename },
        });
        movies.value = res.data.results || []; // 응답 데이터가 없을 경우 기본값 설정
        movie.value = movies.value[0] || {};   // 첫 번째 영화 선택 (없을 경우 빈 객체)

        if (movie.value.poster_path) {
            imageUrl.value = `${Base_URL}${movie.value.poster_path}`;
        } else {
            imageUrl.value = require('@/assets/mind/space.jpg'); // 기본 이미지 설정
        }
        console.log(movie.value);
    } catch (err) {
        console.error('영화 검색 중 오류 발생:', err);
    }
};

const answerMarginTop = ref('500px'); // 기본 margin-top 값

const getApi = async () => {
    try {
        isLoading.value = true;          // 로딩 시작
        answer.value = null;             // 기존 답변 초기화
        answerMarginTop.value = '100px'; // margin-top 값 변경

        // Chat API 호출
        const res = await axios({
            method: 'post',
            url: `http://127.0.0.1:8000/api/v1/chatbot/chat/`,
            data: { message: question.value },
        });
        
        console.log(res.data);
        answer.value = res.data;                        // 응답 데이터 저장
        checkComponents.value = answer.value.user_emotion; // 사용자 감정 데이터 설정
        formview.value = false;                         // 폼 숨김

        // 추천 영화 검색 호출
        if (answer.value.recommend) {
            await getSearch(answer.value.recommend);
        } else {
            console.warn('추천 데이터가 없습니다.');
        }
    } catch (err) {
        console.error('챗봇 API 호출 중 오류 발생:', err);
    } finally {
        isLoading.value = false; // 로딩 종료
    }
};


const goDetail = function(movieId) {
    router.push({name:'detail', params:{movie_id:movieId}})
}



</script>

<style scoped>
.container {
    display: grid;
    grid-template-rows: auto auto;
    grid-template-columns: 1fr repeat(10, 1fr) 1fr;
}  
.form-area {
    margin-top: auto;
    display: flex;
    justify-content: center;
    width: 100%;
    background: rgba(0, 13, 11, 0.5); /* 투명한 흰색 */
    padding: 0.5em;
    border-radius: 8px;
    
} 
.form {
    display: flex;
    width: 100%;
    gap: 0.5em;
    justify-content: space-between;
}

.answer {
    grid-column: 5/9;
    grid-row: 1;
    margin-top: 50px;
    margin-bottom: 100px;
    padding-top: 2em;
    padding-left: 1.5em;
    padding-right: 1.5em;
    padding-bottom: 0.5em;
    border-radius: 25px;
    display: flex;
    flex-direction: column;
    gap: 1em;
    min-height: 150px;
    transition: all 0.3s ease-out;
    height: auto;
    overflow: hidden;
    background: rgba(0, 13, 11, 0.5); /* 투명한 흰색 */
    backdrop-filter: blur(10px); /* 배경 흐림 */
    box-shadow: 0px 0px 12px rgba(120, 206, 232, 0.502);
    border: 1px solid rgba(255, 255, 255, 0.3); /* 연한 테두리 */
}
.my-q {
    align-self: flex-start;
    border: 1px solid #333;
    display: inline-block;
    padding: 0.5em 1em;
    border-radius: 20px;
    max-width: 70%;
    text-align: left;
    background-color: #000d11;
}
.loading {
    animation: glow 1.5s infinite ease-in-out;
}

@keyframes glow {
    0% {
        border-color: #333;
        
    }
    50% {
        border-color: #61FBFF;
        box-shadow: 0px 0px 9px rgba(120, 206, 232, 0.802);
    }
    100% {
        border-color: #333;
    }
}

.ai-q {
    align-self: flex-end;
    border: 1px solid #61FBFF;
    display: inline-block;
    padding: 0.5em 1em;
    border-radius: 20px;
    max-width: 70%;
    text-align: left;
}
.next-title {
    border: 1px solid #61FBFF;
    margin-right: 0;
    float: right;
    padding: 0.5em 1em;
    border-radius: 20px;
    max-width: 100%;
}

/* Animation classes */
.animate-enter {
    transition: all 0.3s ease-out;
}

.enter-from {
    opacity: 0;
    transform: translateY(30px);
}

.enter-to {
    opacity: 1;
    transform: translateY(0);
}

.custom-input {
    width: 85%;  
    padding: 0.5em 1em;  
    font-size: 1em;  
    border: 1px solid #6c757d;  
    border-radius: 8px;  
    background-color: #222;
    color: white;
    outline: none; 
    transition: all 0.3s ease; 
}
.button {
    width: 15%;
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
    width: 20%;   
    padding: 0.5em 1em;  
    font-size: 1em; 
    border: 1px solid #6c757d;
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




.movie-post {
    align-self: flex-end;
    width: 200px;
    cursor: pointer;

}
.movie-post div {
    border-radius: 10px;
    border: 1px solid #61FBFF;
    overflow: hidden;
}

.componentsMind {
    grid-column: 4/10;
    grid-row: 3;
}
</style>