import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import PostFormView from '../views/PostFormView.vue'
import LoginView from '../views/LoginView.vue'
import SignUpView from '../views/SignUpView.vue'
import PostDetail from '../views/PostDetail.vue'
import UserProfileView from '@/views/UserProfileView.vue'
import PasswordChangeView from '../views/PasswordChangeView.vue'

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
    path: '/password',
    name: 'PasswordChange',
    component: PasswordChangeView
  },
  {
    path: '/detail/:id',
    name: 'Detail',
    component: PostDetail
  },
  {
    path: '/profile',
    name: 'MyProfile',
    component: UserProfileView
  },
  {
    path: '/users/:userId',
    name: 'UserProfile',
    component: UserProfileView
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
});

// ナビゲーションガード：ログインチェック
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  
  // ログインや新規登録など、誰でも見れるページ
  const publicPages = ['/login', '/signup'];
  const authRequired = !publicPages.includes(to.path);

  // トークンがなく、かつログイン・新規登録画面以外へアクセスしようとした場合
  if (authRequired && !token) {
    return next('/login');
  }

  next();
});

export default router;