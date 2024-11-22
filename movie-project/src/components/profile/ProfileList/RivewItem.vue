<template>
    <div>
        <p>{{ props.Rivew.content }}</p>
        <p>{{ props.Rivew.id }}</p>
        <RouterLink :to="{name:'review',params:{review_id:props.Rivew.id}}">상세히 보기</RouterLink>
        <button @click="DeleteRivews()">삭제</button>
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
</style>
