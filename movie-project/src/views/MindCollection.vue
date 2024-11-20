<template>
    <div class="container">
        <div class="choice">
            <div class="title">
                <div class="main-title">
                    <h3>오늘의 당신은</h3>
                    <h1>어떤 기분인가요?</h1>
                </div>
                <div>
                    <p>오늘 하루는 어떤 하루였나요?</p>
                    <p>저희는 당신의 하루에 알맞는 영화를 추천드립니다.</p>
                </div>
            </div>
            <div class="button">
                <div @click="checkComponents = 'Depressed'">
                    <span>우울함</span>
                </div>
                <div @click="checkComponents = 'Excited'">
                    <span>설렘</span>
                </div>
                <div @click="checkComponents = 'Happy'">
                    <span>행복한</span>
                </div>
                <div @click="checkComponents = 'Relaxed'">
                    <span>편안함</span>
                </div>
                <div @click="checkComponents = 'Tired'">
                    <span>지침/피곤함</span>
                </div>
                <div @click="checkComponents = 'Angry'">
                    <span>화남</span>
                </div>
                <div @click="checkComponents = 'Anxious'">
                    <span>불안함</span>
                </div>
                <div @click="checkComponents = 'Helpless'">
                    <span>무기력함</span>
                </div>
            </div>
        </div>
        <div class="componentsMind">
            <Base v-if="checkComponents === 'base'"/>
            <Angry v-if="checkComponents === 'Angry'"/>
            <Anxious v-if="checkComponents === 'Anxious'" />
            <Depressed v-if="checkComponents === 'Depressed'" />
            <Excited v-if="checkComponents === 'Excited'" />
            <Happy v-if="checkComponents === 'Happy'" />
            <Helpless v-if="checkComponents === 'Helpless'" />
            <Relaxed v-if="checkComponents === 'Relaxed'" />
            <Tired v-if="checkComponents === 'Tired'" />
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';

//페이지 임포트
import Angry from '@/components/Mind/Angry.vue';
import Anxious from '@/components/Mind/Anxious.vue';
import Depressed from '@/components/Mind/Depressed.vue';
import Excited from '@/components/Mind/Excited.vue';
import Happy from '@/components/Mind/Happy.vue';
import Helpless from '@/components/Mind/Helpless.vue';
import Relaxed from '@/components/Mind/Relaxed.vue';
import Tired from '@/components/Mind/Tired.vue';
import Base from '@/components/Mind/Base.vue';

const checkComponents = ref('base')

</script>

<style scoped>
.container {
    display: grid;
    grid-template-columns: auto auto;
    grid-template-columns: 1fr repeat(10,1fr) 1fr;
}
.choice {
    grid-column: 4/10;
    grid-row: 1;

    display: flex;
    flex-direction: column;
    align-items: center;
}
.title {
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;
    text-align: center;
}
.main-title {

}
.button {
    display: flex;
    flex-wrap: wrap;
    gap: 1em;
    justify-content: center;
}
.button div {
    background-color: gray;
    padding: 1em;
    width: 18%;
    min-width: 120px;
    border-radius: 50px;
    text-align: center;
    cursor: pointer;
}

.componentsMind {
    grid-column: 4/10;
    grid-row: 2;
}
</style>