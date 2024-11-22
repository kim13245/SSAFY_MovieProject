<template>
    <div class="container">
        <div class="signup">
            <div class="signup-text">
                <h3>회원가입</h3>
                <p style="font-size: 0.8em; color: #6c757d;">영화, 기분으로 고르다.</p>
            </div>
            <form @submit.prevent="SignUp">
                <div>
                    <input type="text" id="username" placeholder="아이디를 입력해주세요." v-model.trim="username" class="custom-input">
                </div>
                <div>
                    <input type="email" id="email" placeholder="이메일을 입력해주세요." v-model.trim="email" class="custom-input">
                </div>
                <div>
                    <input type="password" id="password" placeholder="비밀번호를 입력해주세요." v-model.trim="password" class="custom-input">
                </div>
                <div>
                    <input type="text" id="nickname" placeholder="프로필 이름을 입력해주세요." v-model.trim="nickname" class="custom-input">
                </div>
                <button type="submit">회원가입</button>
            </form>
        </div>
    </div>
</template>

<script setup>

import axios from 'axios';
import { ref } from 'vue';
import { useRouter } from 'vue-router';
const router = useRouter()

const username = ref(null)
const email = ref(null)
const password = ref(null)
const nickname = ref(null)

const SignUp = function() {
    axios({
        method:'post',
        url:'http://127.0.0.1:8000/api/v1/accounts/register/',
        data: {
            username:username.value,
            email:email.value,
            password:password.value,
            nickname:nickname.value,
        }
    }).then((res) => {
        console.log(res.data)
        console.log('check!')
        router.push({name:'login'})
    }).catch((err) => {
        console.error(err)
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

.signup {
    width: 300px;
}
.signup-text {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-bottom: 0.5em;
}
#username {
    margin-bottom: 0.5em;
}
#email {
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
.custom-input:hover {
    border-color: #61FBFF;  
    background-color: #333; 
}
.custom-input:hover::placeholder {
    color: #61FBFF;
}f
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