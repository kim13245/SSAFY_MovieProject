<template>
    <div class="card">
        {{ riview.content }}
        {{ riview.rating }}
        {{ riview.nickname }}
        <p>좋아요 수</p>
        {{ riview.likes_count }}
        <div>
            <RouterLink :to="{name:'profile', params:{ user_id: riview.user } }">clcik</RouterLink>
            <p>{{ riview.user }}</p>
        </div>
    </div>
</template>

<script setup>
import { RouterLink } from 'vue-router';


defineProps({
    riview:Object,
})
</script>

<style scoped>
.card {
    border: 1px solid red;
}
</style>