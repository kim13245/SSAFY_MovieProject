<template>
    <div class="container">
        <div class="title">
            <h1>커뮤니티</h1>
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
</template>

<script setup>
import RivewItemComunty from '@/components/comunty/RivewItemComunty.vue';
import { useMovieStore } from '@/stores/movie';
import axios from 'axios';
import { onMounted, ref } from 'vue';
RivewItemComunty

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

onMounted( async () => {
    await getReview()
})

</script>

<style scoped>
.container {
    display: grid;
    grid-template-rows: auto auto;
    grid-template-columns: 1fr repeat(10,1fr) 1fr;
}
.title {
    grid-column: 4/10;
    grid-row: 1;
    margin-top: 50px;
    margin-bottom: 20px;
}
.title hr {
    margin-top: 1em;
    margin-bottom: 1em;
    border-color: #333;
}
.title p {
    color: #666;
}
.head {
    grid-column: 4/10;
    grid-row: 2;
    display: flex;
    flex-wrap: wrap;
    width: 100%;
    gap: 1em;
    padding: 0;
}
.list-item {
    width: calc((100% - 3em) / 4);
}
</style>