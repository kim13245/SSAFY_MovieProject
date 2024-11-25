<template>
    <div class="main">
        <div class="background-img">
            <img src="@/assets/mind/space.jpg" alt="Movie Poster" />
        </div>
        <div class="container">
            <div class="choice">
                <div class="title">
                    <div class="main-title">
                        <h3>오늘의 당신은</h3>
                        <h1>어떤 <span class="serch">기분</span>인가요?</h1>
                    </div>
                    <div class="text">
                        <p>오늘 하루는 어떤 하루였나요?</p>
                        <p>저희는 당신의 하루에 알맞는 영화를 추천드립니다.</p>
                    </div>
                </div>
                <div class="button1">
                    <div class="check"  @click="checkComponents = 'Depressed'">
                        <p class="button --outline" href="#0">우울함</p>
                    </div>
                    <div @click="checkComponents = 'Excited'" class="check">
                        <p class="button --outline" href="#0">설렘</p>
                    </div>
                    <div @click="checkComponents = 'Happy'" class="check">
                        <p class="button --outline" href="#0">행복한</p>
                    </div>
                    <div @click="checkComponents = 'Relaxed'" class="check">
                        <p class="button --outline" href="#0">편안함</p>
                    </div>
                    <div @click="checkComponents = 'Tired'" class="check">
                        <p class="button --outline" href="#0">지침/피곤함</p>
                    </div>
                    <div @click="checkComponents = 'Angry'" class="check">
                        <p class="button --outline" href="#0">화남</p>
                    </div>
                    <div @click="checkComponents = 'Anxious'" class="check">
                        <p class="button --outline" href="#0">불안함</p>
                    </div>
                    <div @click="checkComponents = 'Helpless'" class="check">
                        <p class="button --outline" href="#0">무기력함</p>
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

<style lang="scss" scoped>
.main {
    position: relative;
}
.background-img {
    height: 500px; /* 부모 컨테이너의 높이 설정 (전체 화면 기준) */
    overflow: hidden;
    display: flex;
    justify-content: center; /* 가로 중앙 정렬 */
    align-items: center;    /* 세로 중앙 정렬 */
}
.background-img img {
    max-width: 100%;        /* div 너비에 맞게 이미지 크기 조정 */
    object-fit: contain;    /* 이미지 비율 유지하며 전체 표시 */
}
.background-img::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to top, rgba(0,13,17, 1), rgba(0,13,17, 0.8) 50%, rgba(0,13,17, 1));
  pointer-events: none;
  z-index: 1;
}
.container {
    width: 100%;
    position: absolute;
    z-index: 2;
    top: 5%;
    display: grid;
    grid-template-columns: auto auto;
    grid-template-columns: 1fr repeat(10,1fr) 1fr;
}
.choice {
    grid-column: 4/10;
    grid-row: 1;
    margin-top: 100px;
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    margin-bottom: 100px;
}
.title {
    display: flex;
    flex-direction: column;
    flex-wrap: wrap;
    text-align: center;
    width: 100%;
}
.main-title {

}
.serch {
    color: #61FBFF; 
    font-weight: 800; 
    text-shadow: 0px 0px 9px rgba(120, 206, 232, 0.802);
}
.text {
    width: 100%;
    display: inline-block;
    
    border-radius: 10px;
    padding: 1em;
    margin-bottom: 2em;
    background: rgba(0, 13, 11, 0.5); /* 투명한 흰색 */
    backdrop-filter: blur(10px); /* 배경 흐림 */
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 약간의 그림자 */
    border: 1px solid rgba(255, 255, 255, 0.3); /* 연한 테두리 */
}
.button1 {
    display: flex;
    flex-wrap: wrap;
    gap: 1em;
    justify-content: center;
}


.componentsMind {
    grid-column: 4/10;
    grid-row: 2;
}



/* motion */
.check {
    width: 200px;
    text-align: center;
    cursor: pointer;
}
$color: #61FBFF;
.button {
  text-decoration: none;
  color: white;
  font-weight: 500;
  background: $color;
  padding: 1.25em 3em 1.05em 3em;
  border-radius: 3em;
  position: relative;
  z-index: 1;
  overflow: hidden;
  transition: 1.5s;
  margin: 0 0.5em;
  background-color: #333;
  border: 1px solid #61FBFF;

  &:first-of-type:not(:last-of-type) {
    border-bottom-right-radius: 0.3em;
  }

  &:last-of-type:not(:first-of-type) {
    border-bottom-left-radius: 0.3em;
  }

  &.--outline {
    color: white;
    background: transparent;
  }

  &:before,
  &:after {
    transition: 20s;
    content: '';
    position: absolute;
    top: 0;
    transition: 2s;
    right: -50%;
    left: -50%;
    height: 0;
    padding-bottom: 200%;
    border-radius: 35%;
    z-index: -1;
  }

  &:before {
    background: linear-gradient(
      25deg,
      lighten(adjust-hue($color, 10%), 5%),
      rgba(adjust-hue($color, 10%), 0)
    );
    transform: translate3d(-5%, 4.7em, 0) rotate(330deg);
  }

  &:after {
    background: linear-gradient(
      70deg,
      adjust-hue($color, 20%),
      rgba(adjust-hue($color, 10%), 0)
    );
    transform: translate3d(5%, 4.7em, 0) rotate(0deg);
  }

  &:hover,
  &:focus {

    &.--outline {
      color: white;
      box-shadow: inset 0 0 0 2px rgba($color, 0),
        0 0 40px rgba(adjust-hue($color, 10%), 0.5);
    }

    &:before,
    &:after {
      transform: translate3d(0, -1em, 0) rotate(180deg);
    }
  }
}
</style>