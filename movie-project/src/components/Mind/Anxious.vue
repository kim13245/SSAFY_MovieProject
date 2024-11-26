<template>
    <div class="info">
        <div class="back">
            <h1 class="backfont">Anxious</h1>
        </div>
        <h1 style="font-size: 3em;">불안함</h1>
        <div class="mind">
            <p>판타지</p>
            <p>SF</p>
            <p>서부</p>
        </div>
        <div class="info">
            <p style="font-size: 1.1em; color: #999;">
                불안할 때는 판타지, SF, 모험 같은 비현실적인 장르가 현실로부터 잠시 벗어날 수 있는 기회를 제공합니다. <br>
                새로운 세계에 몰입하며 마음을 진정시키고, 걱정에서 벗어날 수 있는 특별한 경험을 즐겨보세요. <br>
                잠시나마 더 가벼운 마음으로 휴식을 취할 수 있을 겁니다.
            </p>
        </div>
    </div>
    <div class="MovieList" v-if="store.MindMoveList">
        <MindMoviePoster v-for="movie in store.MindMoveList" :key="movie.id" :movie="movie" class="movie-poster"/>
    </div>
</template>

<script setup>
import { useMovieStore } from '@/stores/movie';
import { onMounted, ref } from 'vue';
import MindMoviePoster from './MindMoviePoster.vue';

const store = useMovieStore()


onMounted( async () => {
    await store.getMind('Anxious')
})

</script>

<style scoped>
.MovieList {
    display: flex;
    flex-wrap: wrap;
    gap: 1em;
    margin: 0; 
}
.movie-poster {
    width: calc((100% - 4em) / 5); 
}

/* 여기서 부터 공용 */
.info {
    margin-bottom: 50px;
}
.back {
    display: flex;
    justify-content: center;
    align-items: center;
}
.backfont {
    font-size: 8vw;
    opacity: 10%;
}
.mind {
    display: flex;
    gap: 0.5em;
    margin-bottom: 30px;
}
.mind p {
    text-align: center;
    min-width: 80px;
    display: inline-block;
    padding: 0.6em 1em;
    border-radius: 50px;
    background-color: #6c757d;
}
</style>