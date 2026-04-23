import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../components/HomeView.vue'
import PostFormView from '../components/PostFormView.vue'
import LoginView from '../components/Login.vue'
import SignUpView from '../components/SignUp.vue'

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
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView
  },
  {
    path: '/signup',
    name: 'SignUp',
    component: SignUpView
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router