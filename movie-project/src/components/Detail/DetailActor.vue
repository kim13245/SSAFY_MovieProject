<template>
    <div class="container">
        <div class="profile-img">
            <img :src="imageUrl" alt="">
        </div>
        <div class="profie-text">
            <p class="name">{{ credit.name }}</p>
            <p class="character">{{ credit.character }}</p>
        </div>
    </div>
</template>

<script setup>
const props = defineProps({
    credit:Object,
})

const Base_URL = 'https://image.tmdb.org/t/p/original'
let imageUrl = `${Base_URL}${props.credit.profile_path}`


</script>

<style scoped>
.container {
    display: flex;
    align-items: center;
    justify-content: flex-start;
    border: 1px solid #6c757d;
    border-radius: 8px;
    padding: 0.4em;
    height: 100%;
    transition: box-shadow 0.3s ease-in-out; /* box-shadow가 0.3초 동안 자연스럽게 변화 */
}
.profile-img {
    width: 80px;
    height: 80px;
    overflow: hidden;
    border-radius: 8px;
}
.profile-img img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    
}
.container:hover {
    box-shadow: 0 0px 20px rgba(0, 123, 255, 0.6); /* 호버 시 그림자 추가 */
    border: 1px solid #007bff;
}
.profie-text {
    margin-left: 0.4em;
}
.character {
    font-size: 0.8em;
    color: #6c757d;
    line-height: 1.2; /* 기본 폰트 크기의 1.5배로 행간 설정 */
}
.profie-text {
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

</style>