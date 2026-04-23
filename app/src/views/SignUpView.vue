<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const userId = ref('')
const password = ref('')
const showPassword = ref(false)
const userIdError = ref(false)
const passwordError = ref(false)

const passwordType = () => (showPassword.value ? 'text' : 'password')
const passwordIcon = () => (showPassword.value ? '🔓' : '👁️')

const togglePassword = () => {
  showPassword.value = !showPassword.value
}

const validateAndSubmit = () => {
  userIdError.value = !userId.value.trim()
  passwordError.value = !password.value.trim()

  if (!userIdError.value && !passwordError.value) {
    // TODO: APIでユーザー登録処理を行う
    router.push('/')
  }
}

const goToLogin = () => {
  router.push('/login')
}
</script>

<template>
  <div class="page-wrapper">
    <section class="container" aria-labelledby="signup-heading">
      <div class="logo">
        <img src="../assets/logo.png" alt="KIC 神戸電子専門学校" />
      </div>
      <div class="site-title">プログラミング情報共有サイト</div>

      <h1 id="signup-heading">新規登録</h1>

      <div class="form-group">
        <label for="userId">ユーザID</label>
        <input
          id="userId"
          type="text"
          v-model="userId"
          placeholder="@kduser"
          :aria-invalid="userIdError"
          :aria-describedby="userIdError ? 'userId-error' : undefined"
        />
        <p v-if="userIdError" id="userId-error" class="error-msg">ユーザIDを入力してください</p>
      </div>

      <div class="form-group">
        <label for="password">パスワード</label>
        <div class="password-wrapper">
          <input
            id="password"
            :type="passwordType()"
            v-model="password"
            :aria-invalid="passwordError"
            :aria-describedby="passwordError ? 'password-error' : undefined"
          />
          <button type="button" class="toggle-password" @click="togglePassword" aria-label="パスワード表示切り替え">
            {{ passwordIcon() }}
          </button>
        </div>
        <p v-if="passwordError" id="password-error" class="error-msg">パスワードを入力してください</p>
      </div>

      <button type="button" class="submit-btn" @click="validateAndSubmit">新規登録</button>
      <button type="button" class="footer-link" @click="goToLogin">アカウントをお持ちですか？</button>
    </section>
  </div>
</template>

<style scoped>
.page-wrapper {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #ffffff;
  padding: 24px;
}

.container {
  width: 100%;
  max-width: 400px;
  padding: 20px;
  text-align: center;
  box-sizing: border-box;
}

.logo {
  margin-bottom: 10px;
}

.logo img {
  max-width: 150px;
  height: auto;
}

.site-title {
  font-size: 1.1rem;
  font-weight: bold;
  color: #555;
  margin-bottom: 50px;
}

h1 {
  font-size: 1.6rem;
  color: #444;
  margin-bottom: 30px;
}

.form-group {
  text-align: left;
  margin-bottom: 20px;
  position: relative;
}

label {
  display: block;
  font-size: 0.9rem;
  font-weight: bold;
  margin-bottom: 8px;
  color: #444;
}

input {
  width: 100%;
  padding: 15px;
  border: 1px solid #ccc;
  border-radius: 8px;
  box-sizing: border-box;
  font-size: 1rem;
}

.error-msg {
  color: #ff4d4d;
  font-size: 0.8rem;
  margin-top: 5px;
}

.password-wrapper {
  position: relative;
}

.toggle-password {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
  font-size: 1.2rem;
  user-select: none;
  border: none;
  background: none;
  padding: 0;
}

.submit-btn {
  width: 100%;
  padding: 16px;
  background-color: #2b96b6;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  margin-top: 20px;
}

.footer-link {
  margin-top: 25px;
  display: block;
  color: #2b96b6;
  text-decoration: none;
  font-size: 0.95rem;
  font-weight: bold;
  cursor: pointer;
  background: none;
  border: none;
  width: 100%;
}
</style>
