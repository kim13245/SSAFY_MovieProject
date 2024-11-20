<template>
    <div class="container">
        <div class="login">
            <div class="login-text">
                <h3>로그인</h3>
                <p style="font-size: 0.8em; color: #6c757d;">오신것을 환영합니다.</p>
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
        },
        headers: {
        'Content-Type': 'application/json',  // 헤더 추가
        
        },    
    }).then((res) => {
        const token = res.data.token
        console.log('성공')
        store.Token = res.data[0].token
        store.userId = res.data[1].userId
        store.username = res.data[2].userName
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
.login {
    width: 300px;
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