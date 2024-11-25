<template>
    <div v-if="reviews">
        <h1>커뮤니티</h1>
        <div>
            {{ reviews }}
        </div>
    </div>
</template>

<script setup>
import { useMovieStore } from '@/stores/movie';
import axios from 'axios';
import { onMounted, ref } from 'vue';
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

</style>