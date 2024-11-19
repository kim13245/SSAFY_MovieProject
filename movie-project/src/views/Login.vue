<template>
    <div class="container">
        <div class="login">
            <h3>로그인</h3>
            <p>오신것을 환영합니다.</p>
            <form @submit.prevent="LoginCheck">
                <div class="login-username">
                    <input type="text" id="username" v-model.trim="username">
                </div>
                <div class="login-password">
                    <input type="password" id="password" v-model.trim="password">
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
import { ref } from 'vue';
import axios from 'axios';
import { useMovieStore } from '@/stores/movie';
import { useRouter } from 'vue-router';
const store = useMovieStore()
const router = useRouter()
const username = ref(null)
const password = ref(null)

const LoginCheck = function() {
    axios ({
        method:'post',
        url:'http://127.0.0.1:8000/api/v1/accounts/login/',
        data: {
            username:username.value,
            password:password.value
        }
    }).then((res) => {
        const token = res.data.token
        console.log('성공')
        store.Token = res.data.token
        router.push({name:'home'})
    }).catch((err) => {
        console.log('실패:',err)
    })
}

</script>

<style scoped>
.container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: calc(100vh - 200px);
}
</style>