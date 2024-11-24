<template>
    <div v-if="Rivew_id && reviewInfo" class="container">
        <div class="review-head">
            <div class="user-info">
                <RouterLink :to="{name:'otherprofile', params:{ user_id: reviewInfo.review.user } }" class="link" style="color: white;">
                    {{ reviewInfo.review.nickname }}
                </RouterLink>
                <p class="movie-title">
                    {{ reviewInfo.review.movie_title }}
                </p>
                <div class="footer-div">
                    <div class="img">
                        <img src="@/assets/moviedetail/star-active.png" alt="star-img">
                        <p>{{ reviewInfo.review.rating }}</p>
                    </div>
    
                    <div class="card-fotter-like" @click="checkLike">
                        <div class="card-fotter-img">
                            <img src="@/assets/moviedetail/like.png" alt="" v-if="!is_liked">
                            <img src="@/assets/moviedetail/like-ac.png" alt="" v-if="is_liked">
                        </div>
                        <p>{{ li_liked_count }}</p>
                    </div>
                </div>
            </div>
            <div class="poster">
                <img :src="'https://image.tmdb.org/t/p/original' + reviewInfo.review.poster_path" alt="">
            </div>
            
        </div>
        <div class="review-content">
            <p>
                {{ reviewInfo.review.content }}
            </p>
        </div>
        <div class="comment">
            <h2>코멘트</h2>
            <hr>
            <div>
                <div v-for="comment in comments" :key="comment.id" class="comment-head">
                    <div>
                        <p class="comment-nickname">
                            {{ comment.nickname }}
                        </p>
                        <p class="comment-content">
                            {{ comment.content }}
                        </p>
                    </div>
                    <button @click="deleteComment(comment.id)" class="comment-button">삭제</button>
                </div>
            </div>
            <form @submit.prevent="createComment" class="input">
                <input type="text" v-model.trim="comment" class="custom-input" placeholder="여러분의 의견을 들려주세요.">
                <button>생성</button>
            </form>
        </div>
    </div>



    
</template>

<script setup>
import { useMovieStore } from '@/stores/movie';
const store = useMovieStore()
import axios from 'axios';
import { onMounted, ref } from 'vue';
import { RouterLink, useRoute } from 'vue-router';

const is_liked  = ref(false)
const li_liked_count = ref(0)
const route = useRoute()
const Rivew_id = ref(null)
const getReivewId = function() {
    Rivew_id.value = route.params.review_id
}
const reviewInfo = ref(null)
const getRivew = async function() {
    const config = {
        method: 'get',
        url: `http://127.0.0.1:8000/api/v1/movies/reviews/${Rivew_id.value}`,
    };

    // Token이 존재하면 헤더 추가
    if (store.Token) {
        config.headers = {
            Authorization: `Token ${store.Token}`, // 인증 토큰 추가
        };
    }

    axios(config)
        .then((res) => {
            reviewInfo.value = res.data;
            is_liked.value = res.data.review.is_liked
            li_liked_count.value = reviewInfo.value.review.likes_count
            console.log(Rivew_id.value);
            console.log(res.data);
        })
        .catch((err) => {
            console.log(err);
        });
};


const comments = ref(null)
const getComments = async function() {
    axios({
        method:'get',
        url:`http://127.0.0.1:8000/api/v1/movies/reviews/${Rivew_id.value}/comments/`
    }).then((res) => {
        comments.value = res.data
    }).catch((err) => {
        console.error(err)
    })
}
onMounted( async() => {
    try{
        getReivewId()
        await getRivew()
        await getComments()
    }catch(err) {
        console.error(err)
    }
})

//댓글 생성d
const comment = ref('')
const createComment = function() {
    axios({ 
        method:'post',
        url:`http://127.0.0.1:8000/api/v1/movies/reviews/${Rivew_id.value}/comments/`,
        headers: {
            Authorization: `Token ${store.Token}`, // 인증 토큰 추가
        },
        data:{
            content:comment.value
        }
    }).then((res) => {
        console.log(res)
        comment.value = ''
        comments.value.push(res.data)
    }).catch((err) => {
        console.log(err)
    })
}


// 코멘트 삭제
const deleteComment = function(CommentId) {
    axios({
        method:'delete',
        url:`http://127.0.0.1:8000/api/v1/movies/comments/${CommentId}`,
        headers: {
            Authorization: `Token ${store.Token}`, // 인증 토큰 추가
        },
    }).then((res) => {
        console.log(res)
        comments.value = comments.value.filter(comment => comment.id !== CommentId);
    }).catch((err) => {
        console.log(err)
    })
}



const checkLike = function() {
    axios({
        method:'patch',
        url:`http://127.0.0.1:8000/api/v1/movies/reviews/${Rivew_id.value}/`,
        headers: {
            Authorization: `Token ${store.Token}`, // 인증 토큰 추가
        },
    }).then((res) => {
        console.log('성공')
        console.log(res)
        if (is_liked.value === false) {
            li_liked_count.value ++;
            is_liked.value = true
        } else {
            li_liked_count.value --;
            is_liked.value = false
        }
    }).catch((err) => {
        console.error(err)
    })
}
</script>

<style scoped>
* {
    border-color: #0c0c0c;
}
.container {
    display: grid;
    grid-template-rows: auto auto;
    grid-template-columns: 1fr repeat(10, 1fr) 1fr;
    padding: 0;

}
.review-head {
    grid-column: 4/10;
    grid-row: 1;
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5em;
    border: 1px solid #323232;
    border-radius: 10px;
    padding: 1em;
    margin-top: 50px;
}
.user-info {
    display: flex;
    flex-direction: column;
    justify-content: center;
    height: 100%;
}
.footer-div {
    display: flex;
    gap: 0.5em;
}
.img {
    display: flex;
    padding: 0.2em 0.8em;
    background-color: #282828;
    border-radius: 50px;
    width: 60px;
    height: 30px;
    align-items: center;
    justify-content: center;
    gap: 0.4em;
    margin-top: 0.5em;
}
.img img {
    width: 100%;
    height: 100%;
}
.user-info a {
    font-size: 1.2em;
}
.movie-title {
    font-size: 0.8em;
    color: #6f6f6f;
}
.like-head {
    display: flex;
    align-items: center;
}
.like {
    width: 60px;
    padding: 1em;
    text-align: center
}
.card-fotter-like {
    display: flex;
    background-color: #282828;
    gap: 0.5em;
    justify-content: center;
    align-items: center;
    height: 30px;
    padding: 0.3em;
    border-radius: 50px;
    cursor: pointer;
    width: 60px;
    margin-top: 0.5em;
    transition: all 0.3s ease; 
}
.card-fotter-like:hover {
    border-color: #61FBFF;  
    background-color: #61FBFF; 
}
.card-fotter-img {
    width: 20px;
}
.poster {
    width: 100px;
    border-radius: 10px;
    overflow: hidden;
}
.poster img {
    width: 100%;
    object-fit: cover;
    object-position: center; /* 이미지를 중앙에 배치 */
}

.review-content {
    grid-column: 4/10;
    grid-row: 2;
    border: 1px solid #323232;
    border-radius: 10px;
    padding: 1em;
}
.comment {
    grid-column: 4/10;
    grid-row: 3;
    margin-top: 50px;
}
.comment-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.comment-nickname {
    color: #6f6f6f;
}
.comment-button {
    width: 60px;  
    padding: 0.5em;  
    font-size: 1em; 
    border: 1px solid #6c757d;
    border-radius: 8px;  
    background-color: #222;  
    color: white; 
    outline: none;  
    transition: all 0.3s ease; 
    cursor: pointer;
    text-align: center;
}
.comment-button:hover {
    border-color: #61FBFF;  
    background-color: #61FBFF;  
    color: #000d11;
    font-weight: bold;
}
.input {
    display: flex;
    margin-top: 2em;
}
.custom-input {
    width: 90%;    
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
    width: 10%;  
    max-width: 400px; 
    padding: 0.8em 1em;  
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