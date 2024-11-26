<template>
    <div class="info">
        <div class="back">
            <h1 class="backfont">Relaxed</h1>
        </div>
        <h1 style="font-size: 3em;">편안한 기분</h1>
        <div class="mind">
            <p>드라마</p>
            <p>가족</p>
            <p>코미디</p>
            <p>애니메이션</p>
        </div>
        <div class="info">
            <p style="font-size: 1.1em; color: #999;">
                편안한 기분일 때는 드라마나 음악처럼 차분한 분위기를 유지할 수 있는 장르가 잘 어울립니다. <br>
                복잡하지 않은 스토리와 조용한 감정선이 긴장을 풀고 마음의 평화를 느끼게 해 줄 거예요. <br>
                여유로운 시간을 더 깊이 즐기며 차분히 감상해 보세요.
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
    await store.getMind('Relaxed')
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