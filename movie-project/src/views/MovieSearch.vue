<template>
    <div class="container">
        <div class="search-area">
            <h3>검색창</h3>
            <form @submit.prevent="getSearch">  
                <input type="text" v-model.trim="searchText">
                <input type="submit" value="검색">
            </form>
        </div>
        <div class="poster-list">
            <SearchPoster v-for="movie in movies" :key="movie.id" :movie="movie" />
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
.poster-list {
    display: flex;
}
</style>