<template>
    <div class="container">
        <div class="form-area">
            <form @submit.prevent="getApi" class="form">
                <input type="text" v-model.trim="question" class="custom-input" placeholder="기분을 알려주세요.">
                <button type="submit" class="button">질문하기</button>
            </form>
        </div>
        <div class="answer">
            <TransitionGroup 
                name="message"
                enter-active-class="animate-enter"
                enter-from-class="enter-from"
                enter-to-class="enter-to"
            >
                <div v-if="question" class="my-q" :key="'q'+question">
                    <p>{{ question }}</p>
                </div>
                <div v-if="isLoading" class="ai-q loading" :key="'loading'">
                    <p>LOADING</p>
                </div>
                <div v-if="answer" class="ai-q" :key="'a'+answer.openai_response">
                    <p>{{ answer.openai_response }}</p>
                </div>
            </TransitionGroup>
        </div>
    </div>
</template>

<script setup>
import axios from 'axios';
import { ref } from 'vue';
const question = ref(null)
const answer = ref(null)
const isLoading = ref(false)

const getApi = async function() {
    try {
        isLoading.value = true
        answer.value = null
        const res = await axios({
            method:'post',
            url:`http://127.0.0.1:8000/api/v1/chatbot/chat/`,
            data: {
                message:question.value
            }
        }).then((res) => {
            console.log(res.data)
        })
        answer.value = res.data
    } catch (err) {
        console.error(err)
    } finally {
        isLoading.value = false
    }
}
</script>

<style scoped>
.container {
    display: grid;
    grid-template-rows: auto auto;
    grid-template-columns: 1fr repeat(10, 1fr) 1fr;
}  
.form-area {
    margin-top: 50px;
    grid-column: 4/10;
    grid-row: 1;
    display: flex;
    justify-content: center;
    width: 100%;
    margin-bottom: 30px;
} 
.form {
    display: flex;
    width: 80%;
    gap: 0.5em;
}
.answer {
    grid-column: 4/10;
    grid-row: 2;
    border: 1px solid #333;
    padding: 2em;
    border-radius: 10px;
    display: flex;
    flex-direction: column;
    gap: 1em;
    min-height: 50px;
    transition: all 0.3s ease-out;
    height: auto;
    overflow: hidden;
}
.my-q {
    align-self: flex-start;
    border: 1px solid #333;
    display: inline-block;
    padding: 0.5em 1em;
    border-radius: 20px;
    max-width: 70%;
    text-align: left;
}
.loading {
    animation: glow 1.5s infinite ease-in-out;
}

@keyframes glow {
    0% {
        border-color: #333;
        
    }
    50% {
        border-color: #61FBFF;
        box-shadow: 0px 0px 9px rgba(120, 206, 232, 0.802);
    }
    100% {
        border-color: #333;
    }
}

.ai-q {
    align-self: flex-end;
    border: 1px solid #61FBFF;
    display: inline-block;
    padding: 0.5em 1em;
    border-radius: 20px;
    max-width: 70%;
    text-align: left;
}

/* Animation classes */
.animate-enter {
    transition: all 0.3s ease-out;
}

.enter-from {
    opacity: 0;
    transform: translateY(30px);
}

.enter-to {
    opacity: 1;
    transform: translateY(0);
}

.custom-input {
    width: 78%;  
    padding: 0.5em 1em;  
    font-size: 1em;  
    border: 1px solid #6c757d;  
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
    width: 20%;   
    padding: 0.5em 1em;  
    font-size: 1em; 
    border: 1px solid #6c757d;
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