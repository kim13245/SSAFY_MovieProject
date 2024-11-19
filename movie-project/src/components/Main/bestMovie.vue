<template>
    <div>
        <div class="logoBox" :style="{ backgroundImage: 'url(' + imageUrl + ')' }">
            <div class="logoBoxText">
                <h1>{{ props.movie.title }}</h1>
                <p>{{ props.movie.release_date }}</p>
                <div>
                    <span>{{ props.movie.vote_average }}</span>
                </div>
                <button @click="handleClick">check</button>
            </div>
        </div>
    </div>
</template>

<script setup>
const props = defineProps({
    movie:Object
})

const Base_URL = 'https://image.tmdb.org/t/p/original'
let imageUrl = `${Base_URL}${props.movie.backdrop_path}`

// 클릭 이벤트 -> 부모 전달
const emit = defineEmits(['click'])
const handleClick = function(event) {
    event.stopPropagation(); // 클릭 이벤트 전파 방지
    emit('click',props.movie.id)
}

</script>

<style scoped>
.logoBox {
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: flex-start; /* 수평 방향으로 왼쪽 정렬 */
    align-items: flex-end;      /* 수직 방향으로 하단 정렬 */
    background-color: black;
    color: white;
    padding: 3em;
    background-size: cover; /* 배경 이미지를 요소 크기에 맞게 꽉 차게 표시 */
    background-repeat: no-repeat; /* 이미지 반복 방지 */
    background-position: center; /* 이미지가 중앙에 오도록 설정 */
    pointer-events: auto; /* 클릭 이벤트 활성화 */
}




.logoBox::before {
    content: ""; 
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(to top, rgba(0, 0, 0, 0.1), rgba(0, 0, 0, 0.05) 50%, rgba(0, 0, 0, 0));
    pointer-events: none; 
    z-index: 1;
}
.logoBoxText {
    z-index: 2;
}
</style>