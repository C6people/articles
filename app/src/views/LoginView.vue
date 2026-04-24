<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

/**
 * 【TypeScriptのポイント】
 * Vueでは「ref」を使って、入力内容やエラー状態をリアルタイムに管理します。
 */
    const userid = ref<string>('')
    const password = ref<string>('')
    const errorMessage = ref<string>('')
    const isError = ref<boolean>(false)
    const isPasswordVisible = ref<boolean>(false)

    const router = useRouter()
/**
 * ログインボタンを押した時の処理
 */
    const handleLogin = async () => {
  // 以前のエラー状態をリセット
    isError.value = false
    errorMessage.value = ''

  // --- ⬇️ 将来のDB連携（Node.js / Python）用コード ⬇️ ---
/*
    const url = "http://localhost:8000/login"; 
    try {
    const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userid: userid.value, password: password.value })
    });
    const result = await response.json();
    if (result.success) {
      // 成功：トップ画面へ（Vue Router等を使用）
        return;
    }
    } catch (err) {
        console.error("通信エラー:", err);
    }
  */

  // --- ⬇️ 現時点のダミー判定 ⬇️ ---
    const dummyID = "1234567"
    const dummyPass = "password123"

    if (userid.value !== dummyID || password.value !== dummyPass) {
        // 失敗
        isError.value = true
        errorMessage.value = "ユーザーIDかパスワードが正しくありません"
    } else {
    // 成功
        alert("ログインに成功しました。ホームへ移動します。")
        router.replace('/')
    }
}

/**
 * パスワードの表示/非表示切り替え
 */
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
        <h1>ログイン</h1>
    
        <form @submit.prevent="handleLogin">
        
            <div class="input-group">
                <label for="userid">ユーザーID</label>
                <input 
                    type="text" 
                    id="userid" 
                    v-model="userid" 
                    :class="{ 'input-error': isError }"
                    required 
                    placeholder="7桁学籍番号"
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

            <button type="submit" class="login-button">ログイン</button>
        </form>
    
    <p class="register-link"><a href="#" @click.prevent="router.push('/signup')">アカウントを新規登録する</a></p>

    </div>
</div>
</template>

<style scoped>
/* Google Iconsの読み込み（CSSの冒頭に配置） */
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

/* 元のCSSをそのまま流用 */
.main-wrapper {
    /* 画面いっぱいに広げる */
    width: 100vw;
    height: 100vh;
    
    /* 背景を白（または画像のデザイン通り）にする */
    background-color: #ffffff; 
    
    /* 真ん中寄せの設定 */
    display: flex;
    justify-content: center;
    align-items: center;

    /* 💡 もし背景が真っ黒なままなら、これを追加 */
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

#userid, #password {
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
    height: 14px; /* 少し高さを調整 */
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
    margin-top: 30px;
}

.login-button:hover {
    background-color: #1e7a96;
}
</style>