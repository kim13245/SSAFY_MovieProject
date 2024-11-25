<template>
    <div>
        <form @submit.prevent="getApi">
            <input type="text">
            <input type="submit" value="check">
        </form>
    </div>
</template>

<script setup>
import axios from 'axios';

const getApi = function() {
    axios({
        method:'post',
        url:`http://127.0.0.1:8000/api/v1/chatbot/chat/`,
        data: {
            message:'오늘 기분이 별로인데 어떻하냐 아무거나 영화 추천좀'
        }
    }).then((res) => {
        console.log(res.data)
    }).catch((err) => {
        console.error(err)
    })
}
</script>

<style scoped>

</style>