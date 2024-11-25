<template>
    <div class="container-all">
        <div class="week-movie">
            <div class="week-movie-content">
                <div class="main-slider">
                    <div class="slider">
                        <div v-for="movie in store.movieBestList" :key="movie.id" >
                            <BestMovie :movie="movie" @click="handleChildClick"/>
                        </div>
                    </div>
                    <!-- 태그 정의 후  임의의 클래스를 지정한다.-->
                    <div class="indicaotr">
                        <span class="prevArrow"><img src="@/assets/icon/chevron-left.png" alt="test_img"></span>
                        <span class="nextArrow"><img src="@/assets/icon/chevron-right.png" alt="test_img"></span>          
                    </div>
                </div>
            </div>
        </div>
        <div class="container">
            <div class="front-movie">
                <div class="week-movie-title">
                    <h1>개봉 예정작</h1>
                </div>
                <!-- 무비 리스트 부분 -->
                <div class="front-movie-list">
                    <MoviePost v-for="movie in store.movieList" 
                    :key="movie.id" 
                    :movie="movie" 
                    class="front-movie-list-item" 
                    style="cursor: pointer;"
                    @click="handleChildClick(movie.id)"
                    />
                </div>   
            </div>
    
    
            <div class="today-movie">
                <div class="back-img">
                    <div class="left">
                        <img src="@/assets/main/popcon1.png" alt="">
                    </div>
                    <div class="today-moive">
                        <h3>오늘의 당신은</h3>
                        <h1>어떤 기분인가요?</h1>
                        <p>
                            오늘 하루는 어떤 하루였나요? <br/>
                            저희는 당신의 하루를 위로하고 함께해줄 영화를 추천드리겠습니다.
                        </p>
                        <div class="today-movie-button">
                            <RouterLink :to="{name:'mind'}">지금 체험하기</RouterLink>
                        </div>
                    </div>
                    <div class="right">
                        <img src="@/assets/main/popcon2.png" alt="">
                    </div>
                </div>
            </div>
            <div class="title">
                <h1>이런 리뷰 어떤가요?</h1>
                <p>여러 리뷰를 한번에 확인해보세요!</p>
                <hr>
            </div>
            <div class="head" v-if="reviews">
                <RivewItemComunty 
                    v-for="review in reviews"
                    :key="review.id"
                    :Rivew="review"
                    class="list-item"
                />
            </div>
        </div>

    </div>
</template>

<script setup>

import { onMounted, nextTick, ref } from 'vue';
import $ from 'jquery';
import 'slick-carousel';
import { useMovieStore } from '@/stores/movie';
import MoviePost from '@/components/Main/moviePost.vue';
import BestMovie from '@/components/Main/bestMovie.vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import RivewItemComunty from '@/components/comunty/RivewItemComunty.vue';
const router = useRouter()

// 영화 리스트 들고오기
const store = useMovieStore()

const reviews = ref(null)
const getReview = async function() {
    axios({
        method:'get',
        url:`http://127.0.0.1:8000/api/v1/movies/allreviews/`
    }).then((res) => {
        reviews.value = res.data
    }).catch((err) => {
        console.error(err)
    })
}

onMounted(async() => {
    //비동기 함수로 먼저 api를 먼저 불러오고
    try{
        await store.apimovieBest();
        await store.apiMovie();
        await getReview();
        // 슬라이더 초기화
        nextTick(() => {
            // DOM 업데이트 후 슬라이더 초기화
            $('.slider').slick({
                infinite: true,        // 무한 루프
                slidesToShow: 1,       // 한 번에 보일 슬라이드 수
                slidesToScroll: 1,     // 한 번에 스크롤 될 슬라이드 수
                autoplay: true,        // 자동 슬라이드
                autoplaySpeed: 6000,   // 자동 슬라이드 간격 (6초)
                dots: true,            // 슬라이드 밑에 점 표시
                // fade: true,            // 전환 효과 추가
                draggable: false, // 드래그 비활성화
                preventClicks: false, // 클릭 이벤트 방지 비활성화
                preventClicksPropagation: false, // 클릭 이벤트 전파 방지 비활성화

                prevArrow: $('.prevArrow'), 
                nextArrow: $('.nextArrow'),
            });
        });
    }catch(error) {
        console.error('Error initializing onMounted:', error);
    }
})

// 상세페이지 이동 로직

const handleChildClick = (movieId) => {
    console.log('Received movie ID:', movieId)
    router.push({name:'detail', params:{movie_id:movieId}})
    console.log(1)
}
</script>

<style scoped>
.container {
    display: grid;
    grid-template-rows: auto auto; /* 각 행의 높이를 자동으로 설정 */
    grid-template-columns: 1fr repeat(10, 1fr) 1fr; /* 양옆에 1등분씩 여백, 가운데 10등분 */
    gap: 0;
    padding: 0;
    width: 100%;
}


.week-movie {
    grid-column: 4/10;
    grid-row: 2;

}
.week-movie h1 {
    font-size: 28px;
    font-weight: bold;
}
.week-movie-title {
    margin-bottom: 1em;
}
.week-movie-title div {
    font-size: 0.8em;
    background-color: #B3B3B3;
    color: white;
    padding: 0.5em 0.8em;
}


.front-movie {
    grid-column: 4/10;
    grid-row: 3;

}


/* 기분 추천 부분 스타일 */
.today-movie {
    grid-column: 4/10;
    grid-row: 4;

    margin-top: 250px;
}
.back-img {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10em;
}

.left {
    width: 240px;
    animation: moveUpDown1 2s ease-in-out infinite;
}
/* 애니메이션 정의 */
@keyframes moveUpDown1 {
  0% {
    transform: translateY(0) rotate(0deg); /* 처음 위치와 회전 */
  }
  50% {
    transform: translateY(-50px) rotate(-15deg); /* 위로 50px 이동하고 15도 회전 */
  }
  100% {
    transform: translateY(0) rotate(0deg); /* 다시 원래 위치로 돌아오고 회전 리셋 */
  }
}

.right {
    width: 240px;
    animation: moveUpDown2 3s ease-in-out infinite;
}
@keyframes moveUpDown2 {
  0% {
    transform: translateY(0) rotate(0deg); /* 처음 위치와 회전 */
  }
  50% {
    transform: translateY(-50px) rotate(15deg); /* 위로 50px 이동하고 15도 회전 */
  }
  100% {
    transform: translateY(0) rotate(0deg); /* 다시 원래 위치로 돌아오고 회전 리셋 */
  }
}

.today-moive {
    display: flex;
    flex-direction: column;
    text-align: center;
    align-items: center;
}
.today-movie h3 {
    font-size: 42px;
    margin: 0;
    padding: 0;
    line-height: normal; /* 기본 줄 간격 없애기 */
}
.today-movie h1 {
    font-size: 48px;
}
.today-movie p {
    margin-top: 20px;
}

.today-movie-button {
    width: 100%;  
    max-width: 200px; 
    padding: 0.8em 1em;  
    margin-top: 1.5em;
    font-size: 1em; 
    border: 2px solid #6c757d;
    border-radius: 8px;  
    background-color: #222;  
    color: white; 
    outline: none;  
    transition: all 0.3s ease; 
    cursor: pointer;
}
.today-movie-button:hover {
    border-color: #61FBFF;  
    background-color: #61FBFF;  
    color: #000d11;
    font-weight: bold;
}
/* movie 리스트 정렬 부분 */
.front-movie-list {
    display: grid;
    grid-template-columns: repeat(5,1fr);
    gap: 1em;
    row-gap: 2.5em; /* 상하 간격 */

}
.front-movie-list-item {
    width: 100%;
    height: 100%;
    object-fit: cover;

}



/* 리뷰 추천 */
.revew-movie {
    grid-column: 4/10;
    grid-row: 5;
    margin-top: 250px;
}

.title {
    grid-column: 4/10;
    grid-row: 6;
    margin-top: 200px;
}
.title hr {
    margin-top: 1em;
    margin-bottom: 1em;
    border-color: #333;
}
.head {
    grid-column: 4/10;
    grid-row: 7; 
    display: flex;
    flex-wrap: wrap;
    width: 100%;
    gap: 1em;
    padding: 0;
}
.list-item {
    width: calc((100% - 3em) / 4);
}
/* 슬라이드 이미지 위에 그라데이션 추가 */
.slider {
    margin-top: 0;
    position: relative; /* 자식 요소의 절대 위치를 설정할 수 있도록 함 */
    overflow: hidden;    /* 슬라이더 내용이 라운드 안에 잘리도록 설정 */
}


.slider div {
    height: 752px;
}

/* slide style */
/* 기본 스타일 */

/* 슬라이더 컨테이너의 상대적 위치 설정 */
.main-slider {
    position: relative;
}

/* 슬라이더 화살표 스타일 */
.indicaotr .prevArrow, .indicaotr .nextArrow {
  display: inline-block;

  padding: 10px 10px;
  cursor: pointer;
  font-size: 16px;
  border-radius: 50px;
  user-select: none;
  text-align: center;
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
}

/* 왼쪽 버튼 위치 */
.indicaotr .prevArrow {
  left: 2%;  
}

/* 오른쪽 버튼 위치 */
.indicaotr .nextArrow {
  right: 2%;
}

button {
    z-index: 2;
    position: relative;
}



</style>