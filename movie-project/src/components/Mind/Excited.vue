<template>
    <div class="info">
        <div class="back">
            <h1 class="backfont">Excited</h1>
        </div>
        <h1 style="font-size: 3em;">설렘</h1>
        <div class="mind">
            <p>로맨스</p>
            <p>모험</p>
            <p>판타지</p>
        </div>
        <div class="info">
            <p style="font-size: 1.1em; color: #999;">
                설렘을 느끼는 순간에는 로맨스나 모험, 판타지 같은 장르가 어울립니다. <br>
                사랑스러운 이야기나 새로운 세상을 탐험하는 스토리는 설레는 기분을 더욱 풍부하게 만들어줄 거예요. <br>
                그런 기분을 유지하며 더 많은 즐거움을 느낄 수 있도록 추천 장르를 선택해 보세요.
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
    await store.getMind('Excited')
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