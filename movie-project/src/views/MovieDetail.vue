<template>
    <div v-if="movie" class="container">
        <div class="background-container">
            <div class="background-img">
                <img :src="'https://image.tmdb.org/t/p/original' + movie.backdrop_path" alt="Movie Poster" />
            </div>
            <div class="movie-title">
                <div class="movie-title-info">
                    <div>
                        <h1>{{ movie.title }}</h1>
                        <p>{{ movie.release_date }}</p>
                        <span v-for="genre in movie.genres" :key="genre.id">
                            <p>{{ genre.name }}</p>
                        </span>
                        <p>{{ movie.overview }}</p>
                    </div>
                </div>
            </div>
        </div>
        <div class="detail-movie">
            <div class="top-info">
                <div class="movie-title-detail">
                    <div class="movie-poster">
                        <img :src="'https://image.tmdb.org/t/p/w500' + movie.poster_path" alt="Movie Poster" />
                    </div>
                    <div class="movie-title-detail-content">
                        <div class="movie-score">
                            {{ movie.vote_average }}
                            <p>TMDB 기준</p>
                        </div>
                        <hr />
                        <div class="score">
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

                            <!-- <div class="info-box">
                                {{ movie.origin_country[0] }}
                            </div> -->
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
    </div>
</template>

<script setup>
import { useMovieStore } from "@/stores/movie";
import axios from "axios";
import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
const store = useMovieStore();
const route = useRoute();
const movieId = route.params.movie_id;

// 영화 정보 가져오기 (테스트용)
// movie.origin_country는 model에 없음
const movie = ref(null);
const END_POINT = "http://127.0.0.1:8000/api/v1/movies";
const API_KEY = "421615aa6350c166650b4d15fdd09550";
const getMovieDetails = async () => {
  try {
    const response = await axios.get(`${END_POINT}/movie_detail/${movieId}/`);
    movie.value = response.data;
    console.log(movie.value);
  } catch (error) {
    console.error(error);
  }
};

onMounted(() => {
  getMovieDetails();
});
</script>

<style scoped>
/* 전체 스타일 */
.background-container {
  position: relative; /* 배경과 텍스트를 겹치기 위해 기준을 설정 */
  width: 100%;
  height: 500px; /* 원하는 높이로 조정 */
  overflow: hidden;
}

.background-img::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to top, rgba(0, 0, 0, 1), rgba(0, 0, 0, 0.5) 50%, rgba(0, 0, 0, 0));
  pointer-events: none;
  z-index: 1;
}

.background-img img {
  width: 100%;
  height: 100%;
  object-fit: cover; /* 이미지가 컨테이너에 맞게 채워지도록 설정 */
}

.movie-title {
  position: absolute; /* 배경 위에 텍스트를 배치 */
  bottom: 20px; /* 컨테이너의 하단에서 여백 설정 */
  width: 100%;
  color: white; /* 텍스트 색상 */
  z-index: 1; /* 배경 이미지 위에 표시 */
}
.movie-title-info {
  display: grid;
  grid-template-rows: auto auto; /* 각 행의 높이를 자동으로 설정 */
  grid-template-columns: 1fr repeat(10, 1fr) 1fr; /* 양옆에 1등분씩 여백, 가운데 10등분 */
  gap: 0;
}
.movie-title-info div {
  grid-column: 4/10;
  grid-row: 1;
}

.movie-title h1 {
  font-size: 2.5rem; /* 제목 크기 */
  margin: 0;
}

.movie-title p {
  margin: 5px 0;
  font-size: 1rem;
}

.movie-title span {
  display: inline-block; /* 줄바꿈 방지 */
  margin-right: 10px;
}

/* 하단 info */
.detail-movie {
    display: grid;
    grid-template-rows: auto auto; /* 각 행의 높이를 자동으로 설정 */
    grid-template-columns: 1fr repeat(10, 1fr) 1fr; /* 양옆에 1등분씩 여백, 가운데 10등분 */
    gap: 0;
}
.top-info {
    grid-column: 4/10;
    grid-row: 1;
    padding-top: 50px;
}
.movie-title-detail {
    display: flex;
}
.movie-title-detail-content {
    display: flex;
    flex-direction: column;
    width: 100%;
    margin-left: 1em;
}
.score {
    display: flex;
    justify-content: space-between;
}
.comment {
    display: flex;
    gap: 1em;
}
.detail-info {
    display: flex;
    justify-content: space-between;
    gap: 0.6em;
    margin-top: auto;
}
.info-box {
    width: 33%;
    text-align: center;
    background-color: rgb(209, 209, 209);
    padding: 1.5em;
    border-radius: 10px;
}

/* 하단 */
.all-comment {
    grid-column: 4/10;
    grid-row: 2;
}
</style>
