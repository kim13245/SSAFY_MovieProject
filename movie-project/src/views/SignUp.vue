<template>
    <div>
        <h1>회원가입</h1>
        <div>
            <form @submit.prevent="SignUp">
                <div>
                    <input type="text" id="username" placeholder="아이디를 입력해주세요." v-model.trim="username">
                </div>
                <div>
                    <input type="email" id="email" placeholder="이메일을 입력해주세요." v-model.trim="email">
                </div>
                <div>
                    <input type="password" id="password" placeholder="비밀번호를 입력해주세요." v-model.trim="password">
                </div>
                <input type="submit" value="회원가입">
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

const SignUp = function() {
    axios({
        method:'post',
        url:'http://127.0.0.1:8000/api/v1/accounts/register/',
        data: {
            username:username.value,
            email:email.value,
            password:password.value,
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

</style>