<template>
    <div class="posterItem">
        <img :src="imageUrl" alt="img">
        <p>{{ props.movie.title }}</p>
        <p class="remainingDays">D-{{ remainingDays }}</p>
        <p class="daytitleP">극장 <span class="daytitleSpan">{{ year }}.{{ month }}.{{ day }}</span></p>
    </div>
</template>
c
<script setup>
const props = defineProps({
    movie:Object,
})

const Base_URL = 'https://image.tmdb.org/t/p/w300'
const imageUrl = `${Base_URL}${props.movie.poster_path}`

const releaseDate = props.movie.release_date
const today = new Date()

const releaseDateObj = new Date(releaseDate)
const year = releaseDateObj.getFullYear()
const month = releaseDateObj.getMonth() + 1
const day = String(releaseDateObj.getDate()).padStart(2,'0')

const timeDiff = releaseDateObj - today
const remainingDays = Math.ceil(timeDiff / (1000 * 3600 * 24))

</script>

<style scoped>
.posterItem {
    position: relative;
}
.remainingDays {
    position: absolute;
    top: 0.3em;
    left: 0.3em;
    z-index: 1;
    padding: 0.3em 1em;
    background-color: rgba(0, 0, 0, 0.8);
    color: white;
    max-width: 80px;
    text-align: center;
    border-radius: 5px;
}
img {
    aspect-ratio: 49 / 70;  /* 49:70 비율 설정 */
    overflow: hidden;
    border-radius: 8px;  /* 둥근 모서리 */
}
.daytitleP {
    font-size: 0.8em;
}
.daytitleSpan {
    color: #61FBFF;
}

</style>