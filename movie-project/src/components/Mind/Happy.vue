<template>
    <div class="info">
        <div class="back">
            <h1 class="backfont">Happy</h1>
        </div>
        <h1 style="font-size: 3em;">행복한 기분</h1>
        <div class="mind">
            <p>코미디</p>
            <p>가족</p>
            <p>음악</p>
        </div>
        <div class="info">
            <p style="font-size: 1.1em; color: #999;">
                "행복한 기분일 때는 코미디, 가족 영화 같은 밝고 유쾌한 장르를 선택하면 더욱 좋습니다. <br>
                지금의 긍정적인 감정을 극대화하며 소중한 순간을 더 즐길 수 있을 거예요. <br>
                주변 사람들과 함께 웃고 즐길 수 있는 콘텐츠를 감상해 보세요."
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
    await store.getMind('Happy')
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