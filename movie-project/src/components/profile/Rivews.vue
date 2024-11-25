<template>
    <div>
        <h1>리뷰</h1>

        <!-- 그래프 표시 -->
        <div class="chart">
            <canvas id="reviewChart" ref="reviewChart" v-if="Rivews.length > 0" style="max-width: 100%; height: 300px;"></canvas>
            <p style="font-size: 0.8em; color: #888; margin-top: 1em;">어떤 점수를 주었는지 확인하세요~!</p>
        </div>

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
import { onMounted, ref, nextTick } from 'vue';
import RivewItem from './ProfileList/RivewItem.vue';
import Chart from 'chart.js/auto'; // Chart.js 임포트

const store = useMovieStore();
const props = defineProps({
    userInfo: Object,
});

const reviewChart = ref(null); // Canvas 요소 참조
const Rivews = ref([]); // 리뷰 데이터
let chartInstance = null; // Chart.js 인스턴스

// 그래프 그리기 함수 (너무 길다...)
const drawChart = async () => {
    await nextTick();

    if (reviewChart.value) {
        // 기존 Chart.js 인스턴스 제거
        if (chartInstance) {
            chartInstance.destroy();
        }

        // 점수 분포 계산 (1점~5점 카운트)
        const ratings = [0, 0, 0, 0, 0];
        Rivews.value.forEach((review) => {
            if (review.rating >= 1 && review.rating <= 5) {
                ratings[review.rating - 1]++;
            }
        });

        // 새로운 Chart.js 인스턴스 생성
        const ctx = reviewChart.value.getContext('2d');
        chartInstance = new Chart(ctx, {
            type: 'bar', // 막대 그래프
            data: {
                labels: ['1점', '2점', '3점', '4점', '5점'],
                datasets: [{
                    label: '점수별 리뷰 수',
                    data: ratings, // 정수 데이터
                    backgroundColor: [
                    'rgba(97, 251, 255, 0.2)',  // 밝은 청록색
                    'rgba(97, 181, 255, 0.2)',  // 부드러운 파랑
                    'rgba(97, 138, 255, 0.2)',  // 짙은 파랑
                    'rgba(97, 97, 255, 0.2)',   // 딥 블루
                    'rgba(120, 97, 255, 0.2)',  // 보라색과 어울림
                    ],
                    borderColor: [
                    'rgba(97, 251, 255, 1)',  // 청록색
                    'rgba(97, 181, 255, 1)',  // 파랑
                    'rgba(97, 138, 255, 1)',  // 짙은 파랑
                    'rgba(97, 97, 255, 1)',   // 딥 블루
                    'rgba(120, 97, 255, 1)',  // 보라색
                    ],
                    hoverBackgroundColor: [
                        'rgba(0, 255, 255, 0.6)',
                        'rgba(0, 153, 255, 0.6)',
                        'rgba(0, 102, 255, 0.6)',
                        'rgba(0, 0, 255, 0.6)',
                        'rgba(153, 0, 255, 0.6)',
                    ],
                    hoverBorderColor: [
                        'rgba(0, 255, 255, 1)',
                        'rgba(0, 153, 255, 1)',
                        'rgba(0, 102, 255, 1)',
                        'rgba(0, 0, 255, 1)',
                        'rgba(153, 0, 255, 1)',
                    ],
                    borderWidth: 1,
                    borderRadius: 10
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true, // 비율 유지
                aspectRatio: 5,         // 비율 변경 (기본값: 2 → 세로를 더 줄임)
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            precision: 0
                        },
                        grid: {
                            borderColor: '#333', // y축 격자선 바깥쪽 경계선 색상
                            color: 'rgba(51, 51, 51, 0.2)', // y축 그리드 선 색상 (어두운 색)
                            tickColor: '#333', // y축 눈금선 색상
                        }
                    },
                    x: {
                        grid: {
                            borderColor: '#333', // x축 격자선 바깥쪽 경계선 색상
                            color: 'rgba(51, 51, 51, 0.2)', // x축 그리드 선 색상 (어두운 색)
                            tickColor: '#333', // x축 눈금선 색상
                        }
                    }
                }
            }

        });
    } else {
        console.warn('Canvas element is not available yet.');
    }
};


// 리뷰 가져오기
const getReivews = function () {
    return axios({
        method: 'get',
        url: `http://127.0.0.1:8000/api/v1/accounts/profile/${props.userInfo.id}/reviews`,
    }).then((res) => {
        Rivews.value = res.data;
        console.log(Rivews.value);

        // 데이터 로드 후 그래프 그리기
        drawChart();
    }).catch((err) => {
        console.error(err);
    });
};

// 삭제 처리 함수
const handleDelete = function (reviewId) {
    // Rivews 배열에서 삭제된 리뷰 제외
    Rivews.value = Rivews.value.filter((review) => review.id !== reviewId);

    // 삭제 후 그래프 다시 그리기
    drawChart();
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
.chart {
    border: 1px solid #333; 
    border-radius: 8px;
    padding: 1em;
    margin-bottom: 50px;
}
</style>
