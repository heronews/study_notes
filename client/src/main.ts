import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { createMemoryHistory, createRouter, type RouteRecordRaw } from 'vue-router'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

import { createPinia } from 'pinia'

import LoginView from './components/LoginView.vue'
import MainView from './components/MainView.vue'
import HomeView from './components/HomeView.vue'
import VideoView from './components/VideoView.vue'


const routes: RouteRecordRaw[] = [
    { path: '/', redirect: "/login" },
    { path: '/login', component: LoginView },
    {
        path: '/main', component: MainView, children: [
            { path: 'home', component: HomeView },
            { path: 'video', component: VideoView },
        ]
    },
]

const router = createRouter({
    history: createMemoryHistory(),
    routes,
})

const pinia = createPinia()

const app = createApp(App)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component("IEl" + key, component)
}

app.use(router)
    .use(ElementPlus, { locale: zhCn })
    .use(pinia)
    .mount('#app')
