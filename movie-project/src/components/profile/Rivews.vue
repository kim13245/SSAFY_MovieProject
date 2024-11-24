<template>
    <div>
        <h1>리뷰</h1>
        <div class="list" v-if="props.userInfo">
            <!-- userInfo를 이용해 리뷰 데이터를 표시 -->
            <RivewItem
                v-for="Rivew in Rivews"
                :key="Rivew.id"
                :Rivew="Rivew"
                :userInfo="props.userInfo"
                :onDelete="handleDelete" 
                class="list-item"
            />
        </div>
    </div>
</template>

<script setup>
import { useMovieStore } from '@/stores/movie';
import axios from 'axios';
import { onMounted, ref } from 'vue';
import RivewItem from './ProfileList/RivewItem.vue';



const store = useMovieStore();
const props = defineProps({
    userInfo: Object,
});

const Rivews = ref([]);

// 리뷰 가져오기
const getReivews = function () {
    return axios({
        method: 'get',
        url: `http://127.0.0.1:8000/api/v1/accounts/profile/${props.userInfo.id}/reviews`,
        // headers: {
        //     Authorization: `Token ${store.Token}`,
        // },
    }).then((res) => {
        Rivews.value = res.data;
        console.log(res);
    }).catch((err) => {
        console.error(err);
    });
};

// 삭제 처리 함수
const handleDelete = function (reviewId) {
    // Rivews 배열에서 삭제된 리뷰 제외
    Rivews.value = Rivews.value.filter((review) => review.id !== reviewId);
};

onMounted(async () => {
    try {
        console.log(props.userInfo);
        await getReivews();
    } catch (err) {
        console.log(err);
    }
});
</script>

<style scoped>
.list {
    display: flex;
    flex-wrap: wrap;
    width: 100%;
    gap: 1em;
    padding: 0;
}
.list-item {
    width: calc((100% - 2em) / 3);
}
</style>
