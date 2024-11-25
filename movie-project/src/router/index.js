import Comunity from '@/views/Comunity.vue'
import Login from '@/views/Login.vue'
import Main from '@/views/Main.vue'
import Mind from '@/views/Mind.vue'
import MindCollection from '@/views/MindCollection.vue'
import MovieDetail from '@/views/MovieDetail.vue'
import MovieSearch from '@/views/MovieSearch.vue'
import OtherProfile from '@/views/otherProfile.vue'
import Profile from '@/views/Profile.vue'
import RivewDetail from '@/views/RivewDetail.vue'
import SignUp from '@/views/SignUp.vue'


import { createRouter, createWebHistory } from 'vue-router'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path:'/',
      name:'home',
      component:Main
    },
    {
      path:'/MindCollection',
      name:'mind',
      component:MindCollection
    },
    {
      path:'/MovieSearch',
      name:'moviesearch',
      component:MovieSearch
    },
    {
      path:'/Detail/:movie_id',
      name:'detail',
      component:MovieDetail
    },
    {
      path:'/Profile/:user_id',
      name:'profile',
      component:Profile
    },
    {
      path:'/Comunity',
      name:'comunity',
      component:Comunity
    },
    {
      path:'/Login',
      name:'login',
      component:Login,
    },
    {
      path:'/signUp',
      name:'signup',
      component:SignUp,
    },
    {
      path:'/review/:review_id',
      name:'review',
      component:RivewDetail,
    },
    {
      path:'/profile/other/:user_id',
      name:'otherprofile',
      component:OtherProfile
    },
    {
      path:'/mindAi',
      name:'mindai',
      component: Mind
    }
  ],
})


export default router
