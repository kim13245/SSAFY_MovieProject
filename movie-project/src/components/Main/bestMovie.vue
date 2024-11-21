<template>
    <div>
        <div class="logoBox" :style="{ backgroundImage: 'url(' + imageUrl + ')' }">
            <div class="logoBoxText">
                <div class="logoBoxText-container">
                    <h1>{{ props.movie.title }}</h1>
                    <div class="logoBoxText-info">
                        <span style="color: #61FBFF; font-weight: bold;">{{ (props.movie.vote_average).toFixed(1) }}</span>
                        <span>/10</span>
                        <span style="margin-left: 0.4em; margin-right: 0.4em;">  | </span>
                        <span class="daytitleSpan">{{ year }}.{{ month }}</span>
                    </div>
                    <p>{{ props.movie.overview }}</p>
                </div>
                <div class="button" @click="handleClick">
                    <span>CHECK NOW!</span>
                </div>
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

// 날짜 계산 
const releaseDate = props.movie.release_date
const today = new Date()

const releaseDateObj = new Date(releaseDate)
const year = releaseDateObj.getFullYear()
const month = releaseDateObj.getMonth() + 1
const day = String(releaseDateObj.getDate()).padStart(2,'0')


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
    background-size: 110%; /* 초기 크기 130% 설정 */
    background-repeat: no-repeat; /* 이미지 반복 방지 */
    background-position: center 20%; /* x축은 중앙, y축은 아래로 20% 설정 */
    pointer-events: auto; /* 클릭 이벤트 활성화 */
    padding-bottom: 6%;
    animation: zoomInOut 12s ease-in-out infinite; /* 무한 반복 애니메이션 */
}

@keyframes zoomInOut {
    0% {
        background-size: 110%; /* 시작 크기 */
    }
    10% {
        background-size: 110%; 
    }
    50% {
        background-size: 100%; /* 중간 크기 */
    }
    90% {
        background-size: 110%; 
    }
    100% {
        background-size: 110%; /* 끝 크기 */
    }
}


.logoBox::before {
    content: ""; 
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(to top, rgba(0,13,17, 0.4), rgba(0,13,17, 0.2) 30%, rgba(0,13,17, 0.1) 50%, rgba(0,13,17, 0.05) 80%, rgba(0,13,17, 0));

    pointer-events: none; 
    z-index: 1;
}
.logoBoxText {
    width: 100%;
    display: grid;
    grid-template-rows: auto auto; /* 각 행의 높이를 자동으로 설정 */
    grid-template-columns: 1fr repeat(10, 1fr) 1fr; /* 양옆에 1등분씩 여백, 가운데 10등분 */
    z-index: 2;
}
.logoBoxText-container {
    width: 50%;
    grid-column: 4/10;
    grid-row: 1;
}
.logoBoxText-container p {
    display: -webkit-box; /* 플렉스 박스를 사용 */
    -webkit-line-clamp: 3; /* 2줄 이상이면 ... 표시 */
    -webkit-box-orient: vertical;
    overflow: hidden; /* 넘치는 텍스트 숨김 */
}
.logoBoxText-info {
    margin-bottom: 1em;
}
.button {
    width: 140px;
    grid-column: 4/10;
    grid-row: 2;
    cursor: pointer;
    background-color: #61FBFF;
    padding: 0.5em;
    color: #000d11;
    text-align: center;
    border-radius: 8px;
    margin-top: 2em;
} 
.button span {
    font-weight: bold;
}

h1 {
    font-size: 3.5em;
    margin-bottom: 0.3em;
}

</style>