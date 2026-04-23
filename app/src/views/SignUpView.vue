<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const userId = ref<string>('')
const password = ref<string>('')
const errorMessage = ref<string>('')
const isError = ref<boolean>(false)
const isPasswordVisible = ref<boolean>(false)

const handleSignUp = async () => {
  isError.value = false
  errorMessage.value = ''

  if (!userId.value.trim() || !password.value.trim()) {
    isError.value = true
    errorMessage.value = 'ユーザーIDとパスワードを入力してください'
    return
  }

  // TODO: APIでユーザー登録処理を行う
  alert('登録に成功しました。ホームへ移動します。')
  router.push('/')
}

const togglePasswordVisibility = () => {
  isPasswordVisible.value = !isPasswordVisible.value
}
</script>

<template>
  <div class="main-wrapper">
    <div class="login-box">

      <div class="logo">
        <img class="school-logo" src="@/assets/logo.png" alt="School Logo">
      </div>
      <p class="site-sub-title">プログラミング情報共有サイト</p>
      <h1>新規登録</h1>

      <form @submit.prevent="handleSignUp">

        <div class="input-group">
          <label for="userId">ユーザーID</label>
          <input
            type="text"
            id="userId"
            v-model="userId"
            :class="{ 'input-error': isError }"
            required
            placeholder="@kduser"
          >
          <div class="error-message">{{ errorMessage }}</div>
        </div>

        <div class="input-group">
          <label for="password">パスワード</label>
          <div class="password-wrapper">
            <input
              :type="isPasswordVisible ? 'text' : 'password'"
              id="password"
              v-model="password"
              :class="{ 'input-error': isError }"
              required
              placeholder="8文字以上の英数字"
            >
            <span
              class="material-symbols-outlined"
              id="togglePassword"
              @click="togglePasswordVisibility"
            >
              {{ isPasswordVisible ? 'visibility_off' : 'visibility' }}
            </span>
          </div>
        </div>

        <button type="submit" class="login-button">新規登録</button>
      </form>

      <p class="register-link"><a href="#" @click.prevent="$router.push('/login')">アカウントをお持ちですか？</a></p>

    </div>
  </div>
</template>

<style scoped>
/* Google Iconsの読み込み */
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

.main-wrapper {
    width: 100vw;
    height: 100vh;
    background-color: #ffffff;
    display: flex;
    justify-content: center;
    align-items: center;
    position: fixed;
    top: 0;
    left: 0;
}

.login-box {
    background: #ffffff;
    width: 360px;
    padding: 40px;
    box-shadow: 0 5px 20px rgba(0,0,0,0.1);
    text-align: center;
}

.logo img {
    max-width: 150px;
    height: auto;
}

.site-sub-title {
    font-size: 13px;
    color: #888;
    margin: 0 0 10px 0;
    font-weight: bold;
}

h1 {
    font-size: 24px;
    margin: 30px 0 20px 0;
    color: #4b4b4b;
    font-weight: 700;
    font-family: "Segoe UI", sans-serif;
}

form {
    display: flex;
    flex-direction: column;
    gap: 20px;
    text-align: left;
}

.input-group label {
    display: block;
    font-size: 13px;
    color: #666;
    margin-bottom: 8px;
    font-weight: bold;
}

#userId, #password {
    width: 100%;
    padding: 12px;
    font-size: 14px;
    border: 1px solid #ddd;
    border-radius: 6px;
    box-sizing: border-box;
    transition: border-color 0.2s;
}

input:focus {
    outline: none;
    border-color: #2693B4;
}

.password-wrapper {
    position: relative;
    display: flex;
    align-items: center;
}

.password-wrapper input {
    padding-right: 45px;
}

#togglePassword {
    position: absolute;
    right: 12px;
    cursor: pointer;
    user-select: none;
    color: #aaa;
    font-size: 20px;
    width: 24px;
    text-align: center;
}

.error-message {
    color: #ff4d4d;
    font-size: 12px;
    margin-top: 5px;
    height: 14px;
}

.input-error {
    border-color: #ff4d4d !important;
    background-color: #fffafa;
}

.register-link {
    font-size: 12px;
    font-weight: bold;
    margin-top: 10px;
}

.register-link a {
    color: #2693B4;
    text-decoration: none;
    font-weight: bold;
}

.register-link a:hover {
    text-decoration: underline;
}

.login-button {
    width: 100%;
    padding: 12px;
    background-color: #2693B4;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 15px;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.2s;
}

.login-button:hover {
    background-color: #1e7a96;
}
</style>
