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

const username = ref(null)
const password = ref(null)

const LoginCheck = function() {
    
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