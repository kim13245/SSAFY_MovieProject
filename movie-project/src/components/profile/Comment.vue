<template>
    <div>
        <h1>Comment</h1>
        <div v-if="comments">
            <div v-for="comment in comments" :key="comment.id">
                {{ comment }}
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

</style>