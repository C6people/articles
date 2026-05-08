import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import PostFormView from '../views/PostFormView.vue'
import LoginView from '../views/LoginView.vue'
import SignUpView from '../views/SignUpView.vue'
import PostDetail from '../views/PostDetail.vue'

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
    path: '/post/:id',
    name: 'PostDetail',
    component: PostDetail
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
  },
  {
    path: '/detail/:id',
    name: 'Detail',
    component: PostDetail
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router