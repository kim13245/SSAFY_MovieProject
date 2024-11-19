import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import persistedstate from 'pinia-plugin-persistedstate'


import App from './App.vue'
import router from './router'

const app = createApp(App)
const pinia = createPinia()

// persistedstate 플러그인 활성화
pinia.use(persistedstate)

app.use(pinia)
app.use(router)
app.mount('#app')
