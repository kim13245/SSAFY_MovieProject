<template>
    <div v-if="movie">
        <div class="background-img">
            <img :src="'https://image.tmdb.org/t/p/original'+ movie.backdrop_path" alt="Movie Poster">
        </div>
        <div class="detail-movie">
            <div class="movie-title">
                <h1>{{ movie.title }}</h1>
                <p>{{ movie.release_date }}</p>
                <span v-for="genre in movie.genres" :key="genre.id">
                    <p>{{ genre.name }}</p>
                </span>
                <p>{{ movie.origin_country[0] }}</p>
            </div>
            <div class="movie-title-detail">
                <div class="movie-poster">
                    <img :src="'https://image.tmdb.org/t/p/w500'+ movie.poster_path" alt="Movie Poster">
                </div>
                <div class="movie-title-detail-content">
                    <div class="movie-score">
                        {{ movie.vote_average }}
                        <p>TMDB 기준</p>
                    </div>
                    <hr>
                    <div>
                        <div class="star-score">
                        <!-- 별점 기능 추가 -->
                            <h3>3.4</h3>
                            <p>평균 별점</p>
                        </div>
                        <div class="comment">
                            <div>
                                <div></div>
                                <p>보고싶어요!</p>
                            </div>
                            <div>
                                <div></div>
                                <p>코멘트 작성</p>
                            </div>
                        </div>
                    </div>
                    <div class="detail-info">
                        <div class="info-box">
                            {{ movie.runtime }}
                        </div>
                        <div class="info-box">
                            {{ movie.budget }}
                        </div>
                        <div class="info-box">
                            {{ movie.origin_country[0] }}
                        </div>
                        <div class="info-box">
                            {{ movie.popularity }}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="all-comment">
            <h1>이런 코멘트 어떤가요?</h1>
        </div>
    </div>
</template>

<script setup>
import { useMovieStore } from '@/stores/movie';
import axios from 'axios';
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
const store = useMovieStore()
const route = useRoute()
const movieId = route.params.movie_id




// 영화 정보 가져오기 (테스트용)
const movie = ref(null)
const END_POINT = 'https://api.themoviedb.org/3'
const API_KEY = '421615aa6350c166650b4d15fdd09550'
const getMovieDetails = async () => {
    try {
        const response = await axios.get(`${END_POINT}/movie/${movieId}?api_key=${API_KEY}&language=ko-KR`)
        movie.value = response.data
        console.log(movie.value)
    }catch(error) {
        console.error(error)
    }
}

onMounted(() => {
    getMovieDetails()
})

</script>

<style scoped>

</style>