<template>
    <div v-if="Rivew_id">
        <h1>Detail</h1>
        <p>{{ Rivew_id }}</p>
        <p>{{ reviewInfo }}</p>
    </div>
    <hr>
    <div>
        <form @submit.prevent="createComment">
            <input type="text" v-model.trim="comment">
            <button>생성</button>
        </form>
    </div>
    <hr>
    <div>
        <button>좋아요</button>
    </div>
    <hr>
    <div>
        <div v-for="comment in comments" :key="comment.id">
            {{ comment.nickname }}
            {{ comment.content }}
            <button @click="deleteComment(comment.id)">click</button>
        </div>
    </div>
</template>

<script setup>
import { useMovieStore } from '@/stores/movie';
const store = useMovieStore()
import axios from 'axios';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute()
const Rivew_id = ref(null)
const getReivewId = function() {
    Rivew_id.value = route.params.review_id
}
const reviewInfo = ref(null)
const getRivew = async function() {
    axios({
        method:'get',
        url:`http://127.0.0.1:8000/api/v1/movies/reviews/${Rivew_id.value}`
    }).then((res) => {
        reviewInfo.value = res.data
        console.log(res.data)
    }).catch((err) => {
        console.log(err)
    })
}
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


//좋아요
// const checkLike = function() {
//     axios({
//         method:'post',
//         url:`http://127.0.0.1:8000/api/v1/movies/reviews/likes/${CommentId}/`
//     })
// }
</script>

<style scoped>

</style>