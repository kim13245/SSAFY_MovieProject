<template>
    <div>
        <h1>check1</h1>
        <h1>BUT 우울1</h1>
    </div>
    <div v-if="store.MindMoveList">
        {{ store.MindMoveList }}
    </div>
</template>

<script setup>
import { useMovieStore } from '@/stores/movie';
import { onMounted, ref } from 'vue';

const store = useMovieStore()


onMounted( async () => {
    await store.getMind('우울함')
})

</script>

<style scoped>

</style>