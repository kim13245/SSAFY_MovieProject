<template>
    <div class="info">
        <div class="back">
            <h1 class="backfont">Depressed</h1>
        </div>
        <h1 style="font-size: 3em;">우울함</h1>
        <div class="mind">
            <p>코미디</p>
            <p>가족</p>
            <p>음악</p>
        </div>
        <div class="info">
            <p style="font-size: 1.1em; color: #999;">
                우울할 때는 밝고 유쾌한 장르를 즐겨보는 게 좋습니다. <br>
                코미디, 가족, 음악 같은 따뜻한 분위기의 콘텐츠는 마음을 부드럽게 풀어주고, 자연스럽게 웃음을 찾아주는 효과가 있어요. <br>
                이럴 때 편안한 웃음을 줄 수 있는 영화나 프로그램을 추천드릴게요.
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
    await store.getMind('Depressed')
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