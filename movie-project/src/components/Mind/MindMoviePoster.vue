<template>
    <div class="posterItem" @click="goDetail(props.movie.id)">
        <img :src="imageUrl" alt="img">
        <p>{{ props.movie.title }}</p>
    </div>
</template>
c
<script setup>
import { useRouter } from 'vue-router';

const router = useRouter()
const props = defineProps({
    movie:Object,
})

const Base_URL = 'https://image.tmdb.org/t/p/w300'
const imageUrl = `${Base_URL}${props.movie.poster_path}`

const goDetail = function(movieId) {
    router.push({name:'detail',params:{movie_id:movieId}})
}
</script>

<style scoped>
.posterItem {
    position: relative;
    cursor: pointer;
}
img {
    aspect-ratio: 49 / 70;  /* 49:70 비율 설정 */
    overflow: hidden;
    border-radius: 8px;  /* 둥근 모서리 */
}

</style>