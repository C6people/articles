import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../components/HomeView.vue'
import PostFormView from '../components/PostFormView.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },
  {
    path: '/post',
    name: 'Post',
    component: PostFormView
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router