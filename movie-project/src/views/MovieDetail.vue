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
                        <div class="movie-title-info-detail">
                            <p class="relase-date" style="margin-right: 0.6em;">{{ year }}.{{ month }}.{{ day }}</p>
                            <div v-for="genre in genreNames" class="genre">
                                <p>{{genre}}</p>
                            </div>
                        </div>
                        <div class="movie-title-info-overview">
                            <p>{{ movie.overview }}</p>
                        </div>
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
                            <div>
                                {{ movie.vote_average }}
                            </div>
                            <p>TMDB 기준</p>
                        </div>
                        <hr />
                        <div class="score">
                            <div class="score-point">
                                <div class="star-score">
                                    <!-- 별점 기능 추가 -->
                                    <div class="inner">
                                        <div class="star-rating">
                                            <div
                                                class="star"
                                                v-for="index in 5"
                                                :key="index"
                                                @click="check(index)"
                                            >
                                                <span v-if="index <= score">🍎</span>
                                                <span v-if="index > score">🍏</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div>
                                    <h3>3.4</h3>
                                    <p>평균 별점</p>
                                </div>
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
            <div class="actor">
                <h1>출연/제작</h1>
                <div class="actor-list">
                    <DetailActor v-for="credit in credits" :key="credit" :credit="credit" class="actor-item"/>
                </div>
            </div>
            <!-- <div class="all-comment">
                <h1>이런 코멘트 어떤가요?</h1>
            </div> -->
        </div>
    </div>
</template>

<script setup>
import DetailActor from "@/components/Detail/DetailActor.vue";
import { useMovieStore } from "@/stores/movie";
import axios from "axios";
import { computed, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";

const store = useMovieStore();
const route = useRoute();
const movieId = route.params.movie_id;

// movie.origin_country는 model에 없음
const movie = ref(null);
const credits = ref(null)
const END_POINT = "http://127.0.0.1:8000/api/v1/movies";

const getMovieDetails = async () => {
  try {
    const response = await axios.get(`${END_POINT}/movie_detail/${movieId}/`);
    movie.value = response.data.movie;
    credits.value = response.data.credits.cast
    console.log(movie.value);
    console.log(credits.value)

    if (credits.value && credits.value.length > 12) {
        console.log('slice!')
      credits.value = credits.value.slice(0, 12); // 0번째부터 10개까지만 자르기
    }
  } catch (error) {
    console.error(error);
  }
};


// 장르 이름 들고오기
const genreNames = computed(() => {
  return movie.value.genres
    .map((id) => {
      const genre = store.genres.find((g) => g.id === id);
      return genre ? genre.name : null;
    })
    .filter((name) => name !== null);
});




onMounted(() => {
  getMovieDetails();
});

//별점
const score = ref(0);

const check = (index) => {
    score.value = index
    console.log(score.value)
}

const year = ref(null)
const month = ref(null)
const day = ref(null)

// 날짜 업데이트 구역
watch(() => movie.value, (newMovie) => {
  if (newMovie && newMovie.release_date) {
    const releaseDateObj = new Date(newMovie.release_date);
    year.value = releaseDateObj.getFullYear();
    month.value = releaseDateObj.getMonth() + 1
    day.value = String(releaseDateObj.getDate()).padStart(2,'0')
  }
});



</script>

<style scoped>

/* 전체 스타일 */
.background-container {
    position: relative;
    display: flex; /* Flexbox 활성화 */
    justify-content: center; /* 가로축 중앙 정렬 */
    align-items: center; /* 세로축 중앙 정렬 */
    height: 500px; /* 부모 컨테이너의 높이 설정 (전체 화면 기준) */
    overflow: hidden;
}

.background-img {
    margin-top: 15%; /* 컨테이너 상단 기준으로 20% 아래로 이동 */
    animation: moveMargin 4s ease-in-out alternate; /* 애니메이션 적용 */
}

/* @keyframes로 마진 변경 정의 */
@keyframes moveMargin {
  from {
    margin-top: 0; /* 시작 지점 */
  }
  to {
    margin-top: 15%; /* 끝 지점 */
  }
}


.background-img::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to top, rgba(0,13,17, 1), rgba(0,13,17, 0.6) 50%, rgba(0, 0, 0, 0));
  pointer-events: none;
  z-index: 1;
}

.background-img img {
  object-fit: cover; /* 이미지가 컨테이너에 맞게 채워지도록 설정 */
  object-position: center 20%;
  width: 100%; 
  height: 100%;
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
.movie-title-info-detail {
    display: flex;
}
.relase-date {
    margin-right: 0.4em;
}

.genre {
    display: inline-block;
    margin-right: 0.4em;
}

.movie-title-info-overview {
    width: 70%;
}
.movie-title-info-overview p {
    display: -webkit-box; /* 플렉스 박스를 사용 */
    -webkit-line-clamp: 2; /* 2줄 이상이면 ... 표시 */
    -webkit-box-orient: vertical;
    overflow: hidden; /* 넘치는 텍스트 숨김 */
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

/* 출연진 컴포넌트  */

.actor {
    grid-column: 4/10;
    grid-row: 2;
    margin-top: 150px;
}
.actor-list {
    display: flex;
    flex-wrap: wrap;
    gap: 1em;
    justify-content: flex-start;
    padding: 0; /* 양쪽 끝에 여백 없음 */
}
.actor-item {
    flex: 1 1 calc(25% - 10px); /* 4개씩 한 줄에 배치되도록 설정 */
    box-sizing: border-box; /* 패딩과 테두리를 포함하여 크기를 계산 */
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
.movie-score {
    max-width: 100px;
    text-align: center;
}
.movie-score div {
    background-color: gray;
    padding: 0.5em 1em;
    border-radius: 10px;
    font-size: 1.3em;
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
/* 별점 */
.inner {
    
}
.star-rating {
    display: flex;
}
</style>
