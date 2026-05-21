<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 入力データ
const currentPassword = ref('')
const newPassword = ref('')
const confirmPassword = ref('')

// 目のアイコン用
const isVisibleCurrent = ref(false)
const isVisibleNew = ref(false)
const isVisibleConfirm = ref(false)

// バリデーション
const isShort = computed(() => {
    return newPassword.value.length > 0 && newPassword.value.length < 8
})

// 更新処理
const handleSubmit = () => {
    if (isShort.value) {
        alert('パスワードは8文字以上にしてください')
        return
    }
    if (newPassword.value !== confirmPassword.value) {
        alert('新しいパスワードが一致しません')
        return
    }
    // ログアウト処理（トークン削除）
    localStorage.removeItem('token')
    alert('更新しました。再ログインしてください')
    router.replace('/login')
}

// キャンセル処理
const handleCancel = () => {
    router.push('/profile')
}
</script>

<template>
<div class="password-change-page">
    <div class="form-card">
        <div class="logo-container">
            <div class="logo">
                <img class="school-logo" src="@/assets/logo.png" alt="School Logo">
            </div>
            <p class="site-sub-title">プログラミング情報共有サイト</p>
            <h1>パスワード変更</h1>
        </div>
        <form @submit.prevent="handleSubmit">
            <div class="input-group">
                <label>現在のパスワード</label>
                <div class="password-wrapper">
                    <input
                        :type="isVisibleCurrent ? 'text' : 'password'"
                        v-model="currentPassword"
                        class="password-input"
                        required
                    >
                    <button
                        type="button"
                        @click="isVisibleCurrent = !isVisibleCurrent"
                        class="eye-btn"
                    >
                        <span class="material-symbols-outlined">
                            {{ isVisibleCurrent ? 'visibility_off' : 'visibility' }}
                        </span>
                    </button>
                </div>
            </div>

            <div class="input-group">
                <label>新しいパスワード</label>
                <div class="password-wrapper">
                    <input
                        :type="isVisibleNew ? 'text' : 'password'"
                        v-model="newPassword"
                        class="password-input"
                        required
                    >
                <button
                    type="button"
                    @click="isVisibleNew = !isVisibleNew"
                    class="eye-btn"
                >
                <span class="material-symbols-outlined">
                    {{ isVisibleNew ? 'visibility_off' : 'visibility' }}
                </span>
                </button>
            </div>
            <p v-if="isShort" class="error-msg">8文字以上で入力してください</p>
            </div>

            <div class="input-group">
                <label>新しいパスワード（確認）</label>
                <div class="password-wrapper">
                    <input
                        :type="isVisibleConfirm ? 'text' : 'password'"
                        v-model="confirmPassword"
                        class="password-input"
                        required
                    >
                    <button
                        type="button"
                        @click="isVisibleConfirm = !isVisibleConfirm"
                        class="eye-btn"
                    >
                    <span class="material-symbols-outlined">
                        {{ isVisibleConfirm ? 'visibility_off' : 'visibility' }}
                    </span>
                    </button>
                </div>
            </div>

            <div class="button-group">
                <button
                    type="submit"
                    class="btn-action-blue"
                >
                変更
                </button>
                <button
                    type="button"
                    @click="handleCancel"
                    class="btn-cancel"
                >
                キャンセル
                </button>
            </div>
        </form>
    </div>
</div>
</template>


<style scoped>
/* Google Iconsの読み込み（CSSの冒頭に配置） */
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200');

.password-change-page {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background-color: #f5f5f5;
    padding: 20px; 
    box-sizing: border-box;
}

.form-card {
    width: 100%;
    max-width: 400px;
    background: white;
    padding: 30px 40px 35px 40px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}
.logo-container {
    text-align: center;
}
.logo img {
    max-width: 130px;
    height: auto;
}

.site-sub-title {
    font-size: 10px;
    color: #888;
    font-weight: bold;
}

h1 {
    font-size: 24px;
    margin-bottom: 10px;
    color: #4b4b4b;
    font-weight: 700;
    font-family: "Segoe UI", sans-serif;
}

.password-wrapper {
    position: relative;
    width: 100%;
    display: flex;
    align-items: center;
}

.password-input {
    width: 100%;
    padding: 10px;
    padding-right: 45px;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-sizing: border-box;
}

.eye-btn {
    position: absolute;
    right: 5px;
    background: none;
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #666;
    padding: 8px;
}

/* アイコン自体のサイズ調整 */
.material-symbols-outlined {
    font-size: 20px;
}

.error-msg {
    color: #ff4d4d;
    font-size: 0.8rem;
    margin-top: 5px;
    text-align: left;
}

.input-group {
    margin-bottom: 20px;
}

.input-group label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
}

.input-group input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
    box-sizing: border-box;
}

.button-group {
    display: flex;
    flex-direction: column; /* ボタンを縦に並べるスタイル */
    gap: 15px;
    margin-top: 30px;
}

.btn-action-blue {
    background-color: #2693B4;
    color: white;
    border: none;
    padding: 12px;
    border-radius: 5px;
    cursor: pointer;
    font-weight: bold;
    transition: ease 0.3s;
}
.btn-action-blue:hover {
    background-color: #1b6a8c;
}

.btn-cancel {
    background-color: transparent;
    color: #666;
    border: 1px solid #ccc;
    padding: 12px;
    border-radius: 5px;
    cursor: pointer;
    transition: ease 0.3s;
}
.btn-cancel:hover {
    background-color: #f0f0f0;
}
</style>