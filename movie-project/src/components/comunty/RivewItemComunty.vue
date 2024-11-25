<template>
    <div class="card">
        <div class="card-head">
            <p>{{ props.Rivew.content }}</p>
            <div class="score">
                <img src="@/assets/moviedetail/star-active.png" alt="star-img">
                <p>
                    {{ props.Rivew.rating }}
                </p>
            </div>
        </div>
        <RouterLink :to="{name:'review',params:{review_id:props.Rivew.id}}">상세히 보기</RouterLink>
    </div>
</template>

<script setup>
import { useMovieStore } from '@/stores/movie';
import axios from 'axios';
import { RouterLink } from 'vue-router';
const store = useMovieStore();
const props = defineProps({
    Rivew: Object,
    userInfo: Object,
    onDelete: Function, // 삭제 후 처리 콜백 함수
});

const DeleteRivews = function () {
    if (props.userInfo && props.userInfo.id) {
        axios({
            method: 'delete',
            url: `http://127.0.0.1:8000/api/v1/movies/reviews/${props.Rivew.id}/`,
            headers: {
                Authorization: `Token ${store.Token}`,
            },
        })
        .then(() => {
            console.log('삭제 성공');
            props.onDelete(props.Rivew.id); // 삭제 후 콜백 호출
        })
        .catch((error) => {
            console.error('삭제 실패', error);
        });
    } else {
        console.error('userInfo가 없거나 ID가 정의되지 않았습니다.');
    }
};
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
    border-bottom: 1px solid #323232;
}
.button {
    border: 1px solid #323232;
    background-color: #010C0E;
    color: white;
    padding: 0.4em;
    margin-left: 1em;
}
.score {
    display: flex;
    padding: 0.2em 0.8em;
    background-color: #282828;
    border-radius: 50px;
    width: 60px;
    height: 30px;
    align-items: center;
    justify-content: center;
    gap: 0.4em;
    margin-bottom: 1em;
}
.score img {
    width: 20px;
}
</style>
