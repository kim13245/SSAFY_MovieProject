<template>
    <div class="container">
        <div class="search-area">
            <h3 style="font-weight: 400; color: #6c757d;">찾고 싶은 영화를</h3>
            <h1 style="font-weight: 500;"><span class="serch" >검색</span> 해보세요!</h1>
            <form @submit.prevent="getSearch" class="submit-area">  
                <input type="text" v-model.trim="searchText" class="custom-input" placeholder="제목을 입력해주세요~">
                <input type="submit" value="검색" class="button">
            </form>
        </div>
        <div class="poster-list">
            <div>
                <SearchPoster v-for="movie in movies" :key="movie.id" :movie="movie" class="poster-item"/>
            </div>
        </div>
    </div>
</template>

<script setup>
import SearchPoster from '@/components/Search/SearchPoster.vue';
import axios from 'axios';
import { ref } from 'vue';

const searchText = ref(null)
const movies = ref(null)
const getSearch = function() {
    axios({
        method:'get',
        url:`http://127.0.0.1:8000/api/v1/movies/movie_search/`,
        params:{title:searchText.value}
    }).then((res) => {
        console.log(res.data)
        movies.value = res.data.results
    }).catch((err) => {
        console.error(err)
    })
}
</script>

<style scoped>
.container {

}
.search-area {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 700px;
    background-image: url('@/assets/search/search_background.jpg');
    background-size: 100%; /* 초기 크기 130% 설정 */
    background-repeat: no-repeat; /* 이미지 반복 방지 */
    background-position: center 20%; /* x축은 중앙, y축은 아래로 20% 설정 */
    position: relative;
    animation: zoomInOut 6s ease-in-out; /* 무한 반복 애니메이션 */
}
@keyframes zoomInOut {
    0% {
        background-size: 110%; /* 시작 크기 */
    }
    100% {
        background-size: 100%; /* 끝 크기 */
    }
}
.search-area::before {
    content: ""; 
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(to top, rgba(0,13,17, 1), rgba(0,13,17, 0.1) 30%, rgba(0,13,17, 0.05) 50%, rgba(0,13,17, 0.03) 80%, rgba(0,13,17, 0));

    pointer-events: none; 
    z-index: 1;

}
.poster-list {
    display: grid;
    grid-template-rows: auto auto;
    grid-template-columns: 1fr repeat(10, 1fr) 1fr;
    margin-top: 80px;

}
.poster-list div {
    display: flex; /* Flexbox 사용 */
    flex-wrap: wrap; 
    justify-content: flex-start; 
    gap: 1em; 
    margin: 0; 
    gap: 1em;
    grid-column: 4/10;
    grid-row: 1;
}
.poster-item {
    width: calc((100% - 4em) / 5); 
}

.serch {
    color: #61FBFF; 
    font-weight: 800; 
    text-shadow: 0px 0px 9px rgba(120, 206, 232, 0.802);
}
.submit-area {
    margin-top: 1em;
    width: 800px;
    display: flex;
    justify-content: center;
}
.custom-input {
    width: 65%;  
    padding: 0.8em 1em;  
    font-size: 1em;  
    border: 2px solid #6c757d;  
    border-radius: 8px;  
    background-color: #222;
    color: white;
    outline: none; 
    transition: all 0.3s ease; 
}

.custom-input::placeholder {
    color: #888;  /* 플레이스홀더 텍스트 색상 */
}
.custom-input:hover {
    border-color: #61FBFF;  
    background-color: #333; 
}
.custom-input:hover::placeholder {
    color: #61FBFF;
}

.custom-input:focus {
    border-color: #61FBFF;  
    background-color: #333; 
}

.custom-input:focus::placeholder {
    color: #61FBFF;  
}

.button {
    width: 15%;  
    max-width: 400px; 
    padding: 0.8em 1em;  
    margin-left: 0.3em;
    font-size: 1em; 
    border: 2px solid #61FBFF;
    background-color: #61FBFF;
    color: #000d11;
    font-weight: 800;
    border-radius: 8px;  
    outline: none;  
    transition: all 0.3s ease; 
    cursor: pointer;
}
.button:hover {
    border-color: #61FBFF;  
    color: white;
    background-color: #222;  
    color: #000d11;
    font-weight: bold;
}
</style>