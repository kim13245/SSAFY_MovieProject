<template>
    <div class="info">
        <div class="back">
            <h1 class="backfont">Angry</h1>
        </div>
        <h1 style="font-size: 3em;">화남</h1>
        <div class="mind">
            <p>액션</p>
            <p>공포</p>
            <p>범죄</p>
        </div>
        <div class="info">
            <p style="font-size: 1.1em; color: #999;">
                화가 나거나 감정이 격해졌을 땐 액션, 공포, 범죄 같은 강렬한 장르가 카타르시스를 제공해 줄 수 있습니다. <br>
                강한 스토리와 자극적인 장면을 통해 분노를 해소하고, 마음의 균형을 되찾는 데 도움을 줄 거예요. <br>
                속 시원한 감정을 느낄 수 있는 콘텐츠를 즐겨보세요.
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
    await store.getMind('Angry')
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