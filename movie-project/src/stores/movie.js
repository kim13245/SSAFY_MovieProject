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


  return {movieList, apiMovie, apimovieBest,movieBestList, Token, getUserId, username, userId}
}, {persist:true})
