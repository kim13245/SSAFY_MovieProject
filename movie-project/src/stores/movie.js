import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

const END_POINT = 'https://api.themoviedb.org/3'
const API_KEY = '421615aa6350c166650b4d15fdd09550'
export const useMovieStore = defineStore('movie', () => {
  const Token = ref(null)
  const movieList = ref([])
  const countCheck = ref(0)
  const currentPage = ref(1)
  //top무비 리스트 들고 오는 부분
  //개봉 예정작을 먼저 들고온다.
  const apiMovie = async function() {
    try {
      while (movieList.value.length < 10) {
        const response = await axios.get(`${END_POINT}/movie/upcoming?api_key=${API_KEY}&language=ko-KR&page=${currentPage.value}`)
        const movies = response.data.results

        //필터링하여 현재 개봉 예정인 영화만 추가
        const filterMovies = movies.filter((movie) => {
          // if (new Date(movie.release_date) > new Date()) {
          //   return true
          // } else {
          //   return false
          // }
          const releaseDate = new Date(movie.release_date)
          const today = new Date()
          return releaseDate > today
        })

        // 영화 리스트에 추가하기 + 추가된 내용 만큼 카운트 올리기
        movieList.value.push(...filterMovies)
        countCheck.value += filterMovies.length
        currentPage.value ++

        // 20개가 되면 종료하기
        if (movieList.value.length >= 10) {
          if (movieList.value.length > 10) {
            movieList.value.splice(10) // 10번째 이후 항목을 모두 삭제
          }
          break
        }
      }

      if (movieList.value.length < 10) {
        console.warn('영화 20개 채우기 실패...')
      }
    } catch(err) {
      console.error('영화 정보 가져오기 실패', err)
    }
  }

  //이번주 영화 추천
  const movieBestList = ref([])
  const apimovieBest = async function() {
    try {
      const response = await axios.get(`${END_POINT}/movie/popular?api_key=${API_KEY}&language=ko-KR&page=1`)
      const movies = response.data.results
      movieBestList.value.push(...movies)
  
      if (movieBestList.value.length > 5) {
        movieBestList.value.splice(5)
      }
      console.log(movieBestList.value)
    } catch (error) {
      console.error('Error fetching best movies:', error)
    }
  }


  //유저 정보 저장
  const username = ref(null)
  const userId = ref(null)
  
  const getUserId = function() {
    axios({
      method:'get',
      url:'http://127.0.0.1:8000/api/v1/accounts/logout/',
      headers:{
        'Authorization': Token.value
      }
    }).then((res) => {
      console.log('성공')
      console.log(res)
    }).catch((err) => {
      console.log(err)
    })
  }


  // 감정 get
  const MindMoveList = ref(null)
  const getMind = async function(MindName) {
    try {
      const respons = await axios.get(`http://127.0.0.1:8000/api/v1/movies/emotion/${MindName}`)
      console.log(respons.data)
      MindMoveList.value = respons.data
      if (MindMoveList.value.length > 20) {
        MindMoveList.value = MindMoveList.value.splice(0,20)
      }
    } catch(err) {
      console.error('데이터 불러오기 실패 : ',err)
    }
}




// 장르검색 내용
const genres = [
    {
      "id": 28,
      "name": "액션"
    },
    {
      "id": 12,
      "name": "모험"
    },
    {
      "id": 16,
      "name": "애니메이션"
    },
    {
      "id": 35,
      "name": "코미디"
    },
    {
      "id": 80,
      "name": "범죄"
    },
    {
      "id": 99,
      "name": "다큐멘터리"
    },
    {
      "id": 18,
      "name": "드라마"
    },
    {
      "id": 10751,
      "name": "가족"
    },
    {
      "id": 14,
      "name": "판타지"
    },
    {
      "id": 36,
      "name": "역사"
    },
    {
      "id": 27,
      "name": "공포"
    },
    {
      "id": 10402,
      "name": "음악"
    },
    {
      "id": 9648,
      "name": "미스터리"
    },
    {
      "id": 10749,
      "name": "로맨스"
    },
    {
      "id": 878,
      "name": "SF"
    },
    {
      "id": 10770,
      "name": "TV 영화"
    },
    {
      "id": 53,
      "name": "스릴러"
    },
    {
      "id": 10752,
      "name": "전쟁"
    },
    {
      "id": 37,
      "name": "서부"
    }
  ]


  return {movieList, apiMovie, apimovieBest,movieBestList, Token, getUserId, username, userId, getMind, MindMoveList, genres}
}, {persist:true})
