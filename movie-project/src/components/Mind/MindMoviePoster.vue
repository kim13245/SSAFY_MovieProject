<template>
    <div class="posterItem">
        <img :src="imageUrl" alt="img">
        <p>{{ props.movie.title }}</p>
    </div>
</template>
c
<script setup>
const props = defineProps({
    movie:Object,
})

const Base_URL = 'https://image.tmdb.org/t/p/w300'
const imageUrl = `${Base_URL}${props.movie.poster_path}`


</script>

<style scoped>
.posterItem {
    position: relative;
}
img {
    aspect-ratio: 49 / 70;  /* 49:70 비율 설정 */
    overflow: hidden;
    border-radius: 8px;  /* 둥근 모서리 */
}

</style>