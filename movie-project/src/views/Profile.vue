<template>
    <div>
        <h1>{{ store.username }}</h1>

        <span @click="out">
            <button>탈퇴다~</button>
        </span>
    </div>
</template>

<script setup>

import { useMovieStore } from '@/stores/movie';
import axios from 'axios';
import { useRouter } from 'vue-router';
const store = useMovieStore()
const router = useRouter()

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

</script>

<style scoped>

</style>