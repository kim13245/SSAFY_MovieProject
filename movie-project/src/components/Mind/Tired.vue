<template>
    <div class="info">
        <div class="back">
            <h1 class="backfont">Tired</h1>
        </div>
        <h1 style="font-size: 3em;">지침/피곤함</h1>
        <div class="mind">
            <p>애니메이션</p>
            <p>가족</p>
            <p>코미디</p>
        </div>
        <div class="info">
            <p style="font-size: 1.1em; color: #999;">
                피곤하고 지칠 때는 가볍게 즐길 수 있는 애니메이션이나 코미디가 가장 적합합니다. <br>
                복잡하지 않은 스토리와 따뜻한 분위기가 편안한 휴식을 제공하며, <br>
                에너지를 천천히 회복하도록 도와줄 거예요. <br>
                마음껏 쉬면서 웃을 수 있는 콘텐츠를 만나보세요.
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
    await store.getMind('Tired')
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