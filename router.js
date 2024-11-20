// src/router.js
import { createRouter, createWebHistory } from 'vue-router'
import Home from './components/Home.vue'
import About from './components/About.vue'
import Login from './components/Login.vue'
import Data from './components/Data.vue'
import DetailsTechniques from './components/DetailsTechniques.vue'
import UserGuide from './components/UserGuide.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/a-propos',
    name: 'About',
    component: About
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/donnees-capteurs',
    name: 'Data',
    component: Data
  },
  {
    path: '/details-techniques',
    name: 'DetailsTechniques',
    component: DetailsTechniques
  },
  {
    path: '/user-guide',
    name: 'UserGuide',
    component: UserGuide
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router