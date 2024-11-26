<template>
    <div>
        <h1>Comment</h1>
        <div v-if="comments">
            <div v-for="comment in comments" :key="comment.id" class="comment-head">
                <div>
                    <p class="comment-nickname">
                        {{ comment.nickname }}
                    </p>
                    <p class="comment-content" style="font-size: 1.2em;">
                        {{ comment.content }}
                    </p>
                </div>
                <button v-if="userInfo.id === store.userId" @click="deleteComment(comment.id)" class="comment-button">삭제</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useMovieStore } from '@/stores/movie';
import axios from 'axios';
import { onMounted, ref } from 'vue';
const store = useMovieStore()

const props = defineProps({
    userInfo: Object,
})

const comments = ref([])

// 댓글 가져오기
const getComments = function() {
    return axios({
        method:'get',
        url:`http://127.0.0.1:8000/api/v1/accounts/profile/${props.userInfo.id}/rcomments`,
        headers: {
            Authorization: `Token ${store.Token}`,
        },
    }).then((res) => {
        comments.value = res.data
        console.log(comments.value)
    }).catch((err) => {
        console.error(err)
    })
}

onMounted( async() => {
    try{
        await getComments()
    }catch(err) {
        console.error(err)
    }
})

</script>

<style scoped>
.comment {
    grid-column: 4/10;
    grid-row: 3;
    margin-top: 50px;
}
.comment-head {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #222;
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
</style>