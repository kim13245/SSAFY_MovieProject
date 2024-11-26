<template>
    <div class="info">
        <div class="back">
            <h1 class="backfont">Helpless</h1>
        </div>
        <h1 style="font-size: 3em;">무기력함</h1>
        <div class="mind">
            <p>드라마</p>
            <p>다큐멘터리</p>
            <p>역사</p>
        </div>
        <div class="info">
            <p style="font-size: 1.1em; color: #999;">
                무기력할 때는 드라마나 다큐멘터리처럼 의미 있는 스토리가 담긴 작품이 좋습니다. <br>
                이런 콘텐츠는 깊은 감동을 주며 삶의 방향성을 다시 생각하게 하고, 동기부여를 얻는 데 도움을 줄 거예요. <br>
                마음에 울림을 줄 수 있는 작품을 감상하며 에너지를 회복해 보세요.
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
    await store.getMind('Helpless')
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