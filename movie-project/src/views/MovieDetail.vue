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
                        <div class="movie-scroe-parent">
                            <div class="movie-score">
                                <div class="custom-font">
                                    <p style="font-size: 1.5em; text-shadow: 0px 0px 9px rgba(120, 206, 232, 0.802);">{{ (movie.vote_average).toFixed(1) }}</p>
                                </div>
                                <p style="color: #6c757d; font-size: 0.8em;">TMDB 기준</p>
                            </div>
                            <div>
                                <div class="want-movie">
                                    <div @click="wantMovie" class="tag-img">
                                        <img :src="getTagImage" alt="tag-img" />
                                    </div>
                                    <p style="color: #6c757d; font-size: 0.8em;">보고싶어요!</p>
                                </div>
                            </div>
                        </div>
                        <div class="score">
                            <div class="score-point">
                                <!-- 리뷰 기능 테스트 -->
                                <div class="reveiw">
                                    <form @submit.prevent="review" class="reveiw-form">
                                        <textarea  class="review-text" type="text" v-model="reviwContent"
                                        :placeholder="userContent"></textarea>
                                        <div class="reveiw-detail">
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
                                                            <div v-if="index <= score" class="span-tag">
                                                                <img src="@/assets/moviedetail/star-active.png" alt="">
                                                            </div>
                                                            <div v-if="index > score" class="span-tag">
                                                                <img src="@/assets/moviedetail/star-deactive.png" alt="">
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div class="star-score">
                                                        <p><span style="
                                                            color: #61FBFF; 
                                                            font-weight: 800; 
                                                            text-shadow: 0px 0px 9px rgba(120, 206, 232, 0.802);
                                                            font-size: 1.4em;"
                                                            >{{ score }}</span> / 5</p>
                                                    </div>
                                                </div>
                                            </div>
                                            <button class="reveiw-button">리뷰 작성</button>
                                        </div>
                                    </form>     
                                </div>
                            </div>
                        </div>

                        <div class="detail-info">
                            <div class="info-box">
                                <p>상영시간</p>
                                <p class="info-box-maintext">{{ movie.runtime }} <span style="font-size: 0.6em; font-weight: 400;">분</span></p>
                            </div>
                            <div class="info-box">
                                <p>총 제작비</p>
                                <p class="info-box-maintext">{{ movie.budget }} <span style="font-size: 0.6em; font-weight: 400;">$</span></p>
                            </div>

                            <!-- <div class="info-box">
                                {{ movie.origin_country[0] }}
                            </div> -->
                            <div class="info-box">
                                <p>인기지수</p>
                                <p class="info-box-maintext">{{ movie.popularity }} <span style="font-size: 0.6em; font-weight: 400;">POINT</span></p>
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
            <!-- 여기서 리뷰 뜨는지 체크 -->
            </div>
            <div class="rivew-list">
                <h1>리뷰</h1>
                <div class="rivew-list-items">
                    <ReviewItem class="rivew-list-item" v-for="riview in reviews" :key="riview.id" :riview="riview"/>
                </div>
                <div>
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
import ReviewItem from "@/components/Main/reviewItem.vue";
import { useMovieStore } from "@/stores/movie";
import axios from "axios";
import { computed, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";

// 상단에 이미지 import 추가
import tagActivateImg from '@/assets/moviedetail/tag-activate.png'
import tagDeactivateImg from '@/assets/moviedetail/tag-deactivae.png'

const store = useMovieStore();
const route = useRoute();
const movieId = route.params.movie_id;

// movie.origin_country는 model에 없음
const movie = ref(null);
const credits = ref(null)
const reviews = ref(null);
const END_POINT = "http://127.0.0.1:8000/api/v1/movies";

//별점
const score = ref(0);
const currentUserId = store.userId
const userContent = ref(""); // userContent 초기화

// 찜하기 기능
const isFavorite = ref(false); // 초기값: false
const getTagImage = computed(() => {
    return isFavorite.value ? tagActivateImg : tagDeactivateImg
})


const getMovieDetails = async () => {
  try {
    // 조건부로 헤더 설정: 토큰이 있으면 Authorization 헤더 추가
    const headers = store.Token
      ? { Authorization: `Token ${store.Token}` }
      : {};

    // 요청 전송
    const response = await axios.get(`${END_POINT}/movie_detail/${movieId}/`, { headers });

    // 응답 데이터 처리
    movie.value = response.data.movie;
    credits.value = response.data.credits.cast;
    reviews.value = response.data.reviews;
    // 별점 준거 그대로 넣어주기
    score.value = response.data.movie.is_kept.rating
    isFavorite.value = response.data.movie.is_kept.is_kept
    console.log(movie.value);
    console.log(credits.value);
    console.log(reviews.value);

    // 캐스트 데이터 슬라이스
    if (credits.value && credits.value.length > 12) {
      console.log("slice!");
      credits.value = credits.value.slice(0, 12); // 0번째부터 12개까지만 자르기
    }


        // 현재 사용자 ID에 해당하는 리뷰의 content 찾기
    if (Array.isArray(reviews.value)) {
        const userReview = reviews.value.find((review) => review.user === currentUserId);
        userContent.value = userReview ? userReview.content : ""; // 없으면 빈 문자열
    } else {
      console.warn("Reviews is not an array:", reviews.value);
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



const reviwContent = ref(null)
const reviewNumber = ref(null)

// review test
const review = function() {
    axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/api/v1/movies/reviews/',
        headers: {
            Authorization: `Token ${store.Token}`, // 인증 토큰 추가
        },
        data: {
            content: reviwContent.value,
            rating: score.value,
            movie: movieId,
            emotion: 1,
        }
    }).then((res) => {
        console.log(res.data);
        // 작성된 리뷰를 기존 리뷰 리스트에 추가
        reviews.value.unshift(res.data); // 최신 리뷰가 위로 올라오도록 추가
        reviwContent.value = ''; // 입력값 초기화
        reviewNumber.value = null;
    }).catch((err) => {
        console.error(err.response);
    });
};


// 찜하기 기능
const wantMovie = function() {
    axios({
        method:'post',
        url:`http://127.0.0.1:8000/api/v1/movies/keep/${movieId}/`,
        headers: {
            Authorization: `Token ${store.Token}`
        },
    }).then((res) => {
        console.log(res.data)
        isFavorite.value = !isFavorite.value; // 상태를 토글
    }).catch((err) => {
        console.error(err)
    })
}

// id title vote_vaerage, movies




// 리뷰 작성 placeholder
</script>

<style scoped>

.custom-font {
    font-family: 'CWDangamAsac-Bold', sans-serif;
    color: #61FBFF;
    font-size: 3em;
}

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
    margin-top: 100px;
}
.actor-list {
    display: flex;
    flex-wrap: wrap;
    gap: 1em;
    justify-content: flex-start;
    padding: 0; /* 양쪽 끝에 여백 없음 */
    margin: 0;
}
.actor-item {
    width: calc((100% - 3em) / 4); 
    box-sizing: border-box; /* 패딩과 테두리를 포함하여 크기를 계산 */
}

/* 리뷰 */
.rivew-list {
    grid-column: 4/10;
    grid-row: 3;;
    width: 100%;
    margin-top: 100px;
}
.rivew-list-items {
    display: flex;
    flex-wrap: wrap;
    gap: 1em; 
    margin: 0;
    justify-content: flex-start;
}
.rivew-list-item {
    width: calc((100% - 2em) / 3); 
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
    align-items: flex-start;
}
.movie-poster {
    border-radius: 15px;
    overflow: hidden;
    max-width: 300px;
}
.movie-title-detail-content {
    display: flex;
    flex-direction: column;
    width: 100%;
    margin-left: 1em;
}
.movie-scroe-parent {
    display: flex;
    gap: 1em;
}
.movie-score {
    max-width: 100px;
    text-align: center;
    margin-bottom: 0.8em;
}
.movie-score div {
    background-color: #000d12;
    border: 1px solid #323232;
    padding: 0.2em 1em;
    border-radius: 10px;
    font-size: 1.3em;
    height: 60px;
}
.score {
    display: flex;
    width: 100%;
}
.score-point {
    width: 100%;
}
.reveiw {
    width: 100%;
}
.review-text {
    width: 100%;
    height: 100px;
    background-color: #000d11;
    border: 1px solid #323232;  
    border-radius: 8px;  
    padding: 0.8em 1em;  
    position: relative;
    color: white;
    resize: none; /* 크기 조절 버튼 비활성화 */
    font-family: 'Spoqa Han Sans Neo', 'sans-serif'; /* 기본 폰트 */
}
.review-text::placeholder {
    font-family: 'Spoqa Han Sans Neo', 'sans-serif'; /* 기본 폰트 */
    color: #888;  /* 플레이스홀더 텍스트 색상 */
    position: absolute;
    top: 5px;  /* 위로 5px 이동 */
    left: 10px; /* 왼쪽으로 10px 이동 */
}
.reveiw-detail {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1em;
}
.reveiw-button {
    width: 100%;  
    max-width: 130px; 
    padding: 0.4em 1em;  
    font-size: 1em; 
    border: 1px solid #6c757d;
    border-radius: 8px;  
    background-color: #000d11;  
    color: white; 
    outline: none;  
    transition: all 0.3s ease; 
    cursor: pointer;
    text-align: center;
}
.reveiw-button:hover {
    border-color: #61FBFF;  
    background-color: #61FBFF;  
    color: #000d11;
    font-weight: bold;
}
.tag-img {
    height: 60px;
    padding: 1em;
    background-color: #000d12;
    border: 1px solid #323232;
    border-radius: 10px;
    cursor: pointer;
}
.tag-img:hover {
    border: 1px solid #61FBFF;
    box-shadow: 0px 0px 9px rgba(120, 206, 232, 0.802);
}
.tag-img img {
    width: 100%;
    height: 100%
}
.comment {
    display: flex;
    gap: 1em;
}
.detail-info {
    display: flex;
    justify-content: space-between;
    gap: 0.6em;
    margin-top: 1em;
}
.info-box {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 33%;
    text-align: center;
    background-color: #000d12;
    border: 1px solid #323232;
    padding: 1.5em;
    border-radius: 10px;
    color: #6c757d;
}
.info-box-maintext {
    color: white;
    font-size: 1.8em;
    font-weight: 900;
}
/* 하단 */
.all-comment {
    grid-column: 4/10;
    grid-row: 2;
}
/* 별점 */
.inner {
    display: flex;
    gap: 0.5em;
    align-items: center;
}
.star-rating {
    display: flex;
}
.span-tag {
    width: 40px;
}
.span-tag img {
    width: 100%;
}
.star-score {
    display: flex;
    font-size: 1.2em;
    color: #6c757d;
}
</style>
