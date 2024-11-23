<template>
    <div class="card">
        <div class="card-head">
            <RouterLink :to="{name:'profile', params:{ user_id: riview.user } }" class="link" style="color: #6c757d;">{{ riview.nickname }}</RouterLink>
            <div>
                <img src="@/assets/moviedetail/star-active.png" alt="star-img">
                <p>
                    {{ riview.rating }}
                </p>
            </div>
        </div>
        <hr>
        <div class="content">
            <p style="font-size: 1.2em; color: #f8f9fa;">{{ riview.content }}</p>
        </div>

        <hr>
        <div class="card-fotter">
            <div class="card-fotter-like">
                <div class="card-fotter-img">
                    <img src="@/assets/moviedetail/like.png" alt="">
                </div>
                <p>{{ riview.likes_count }}</p>
            </div>
            <div>
                <RouterLink :to="{name:'review',params:{review_id:riview.id}}">상세히 보기</RouterLink>
            </div>
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
    border: 1px solid #323232;
    background-color: #010C0E;
    border-radius: 10px;
    padding: 1em

}
.card-head {
    width: 100%;
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.5em;
}

hr {
    border-color: #323232;
}

.card-head div {
    display: flex;
    padding: 0.2em 0.8em;
    background-color: #282828;
    border-radius: 50px;
    width: 60px;
    height: 30px;
    align-items: center;
    justify-content: center;
    gap: 0.4em;
}
.card-head div img {
    width: 100%;
    height: 100%;
}
.content {
    padding-top: 0.8em;
    padding-bottom: 0.8em;
}
.card-fotter {
    display: flex;
    gap: 0.5em;
    padding-top: 1em;
    align-items: center;
    justify-content: space-between;
}
.card-fotter-like {
    display: flex;
    background-color: #282828;
    gap: 0.5em;
    justify-content: center;
    height: 30px;
    padding: 0.3em 1em;
    border-radius: 50px;
}
.card-fotter-img {
    width: 20px;
}
.card-fotter div img {
    width: 100%;
}
.link {
    color: #323232;
}
</style>