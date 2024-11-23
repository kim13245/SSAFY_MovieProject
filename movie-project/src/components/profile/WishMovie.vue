<template>
    <div>
        <h1>보고싶은 영화</h1>
        <div>
            <WishMovieItem v-for="whishMovie in whishMovies" :key="whishMovie.id" :whishMovie="whishMovie"/>
        </div>
    </div>
</template>

<script setup>

const props = defineProps({
    userInfo:Object,
})

import axios from 'axios';
import { onMounted } from 'vue';
import WishMovieItem from './ProfileList/WishMovieItem.vue';
import { ref } from 'vue';

const whishMovies = ref([])
const getWishMovie = async function() {
    axios({
        method:'get',
        url:`http://127.0.0.1:8000/api/v1/accounts/profile/${props.userInfo.id}/movies/`
    }).then((res) => {
        console.log(res)
        whishMovies.value = res.data
    }).catch((err) => {
        console.error(err)
    })
}


onMounted( async() => {
    try{
        await getWishMovie()
    }catch(err) {
        console.error(err)
    } 
})

</script>

<style scoped>

</style>