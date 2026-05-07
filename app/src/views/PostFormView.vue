<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// フォームデータ
const title = ref('')
const genre = ref('')
const content = ref('')
const tags = ref('')

// エラーメッセージ
const errors = ref({
  title: '',
  genre: '',
  content: ''
})

// バリデーション対象フィールド
const fields = [
  { id: 'title', name: 'タイトル', value: title },
  { id: 'genre', name: 'ジャンル', value: genre },
  { id: 'content', name: '内容', value: content }
]

// エラークリア
const clearErrors = () => {
  Object.keys(errors.value).forEach(key => {
    errors.value[key as keyof typeof errors.value] = ''
  })
}

// エラー表示
const showError = (fieldId: string, message: string) => {
  errors.value[fieldId as keyof typeof errors.value] = message
}

// フォーム送信処理
const handleSubmit = async (event: Event) => {
  event.preventDefault()
  clearErrors()

  let hasError = false

  fields.forEach(field => {
    const value = field.value.value.trim()
    if (!value) {
      showError(field.id, field.name + 'を入力してください')
      hasError = true
    }
  })

  if (hasError) return

  try {
    // API振り分け
    const isQuestion = genre.value === "question"
    const url = isQuestion
      ? "http://localhost:8000/questions"
      : "http://localhost:8000/articles"

    // 送信データ（バックのschemaに合わせる）
    const body = isQuestion
      ? {
          title: title.value,
          body: content.value,
          // ↓テスト時はuserのハッシュ値を直接入れておいてください
          user_id: "94d81f82-2082-421d-bf9d-94aced3e0fbe" // 後で消す
        }
      : {
          title: title.value,
          body: content.value,
          genre: genre.value,
          user_id: "94d81f82-2082-421d-bf9d-94aced3e0fbe"
        }

    const res = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(body)
    })

    if (!res.ok) {
      throw new Error("投稿に失敗")
    }

    alert("投稿成功")
    router.push("/")

  } catch (e) {
    console.error(e)
    alert("投稿に失敗しました")
  }
}

// キャンセル処理
const handleCancel = () => {
  router.push('/')
}

// エラーメッセージをクリア
const clearFieldError = (fieldId: string) => {
  const el = document.getElementById(fieldId)
  if (el) {
    const value = el instanceof HTMLSelectElement ? el.value : (el as HTMLInputElement | HTMLTextAreaElement).value.trim()
    if (value) {
      errors.value[fieldId as keyof typeof errors.value] = ''
    }
  }
}

// ジャンル選択の初期化
onMounted(() => {
  genre.value = ''
})
</script>

<template>
  <div class="post-container">
    <h1>新規投稿</h1>
    <form @submit="handleSubmit" id="postForm">
      <div class="form-group">
        <label for="title">タイトル</label>
        <div class="field">
          <input
            type="text"
            id="title"
            v-model="title"
            placeholder="タイトルを入力"
            :class="{ invalid: errors.title }"
            @input="clearFieldError('title')"
            @blur="clearFieldError('title')"
          />
          <div class="error-msg" v-if="errors.title">{{ errors.title }}</div>
        </div>
      </div>

      <div class="form-group">
        <label for="genre">ジャンル</label>
        <div class="field">
          <select
            id="genre"
            v-model="genre"
            :class="{ invalid: errors.genre }"
            @change="clearFieldError('genre')"
            @blur="clearFieldError('genre')"
          >
            <option value="">選択してください</option>
            <option value="question">質問</option>
            <option value="project">制作物</option>
            <option value="column">コラム</option>
            <option value="other">その他</option>
          </select>
          <div class="error-msg" v-if="errors.genre">{{ errors.genre }}</div>
        </div>
      </div>

      <div class="form-group">
        <label for="content">内容</label>
        <div class="field">
          <textarea
            id="content"
            v-model="content"
            placeholder="内容を入力してください..."
            :class="{ invalid: errors.content }"
            @input="clearFieldError('content')"
            @blur="clearFieldError('content')"
          ></textarea>
          <div class="error-msg" v-if="errors.content">{{ errors.content }}</div>
        </div>
      </div>

      <div class="form-group">
        <label for="tags">タグ</label>
        <div class="field">
          <input
            type="text"
            id="tags"
            v-model="tags"
            placeholder="タグを追加（例：JavaScript, Python）"
          />
          <div class="error-msg"></div>
        </div>
      </div>

      <div class="button-container">
        <button type="button" class="cancel-btn" @click="handleCancel">キャンセル</button>
        <input type="submit" value="投稿する">
      </div>
    </form>
  </div>
</template>

<style scoped>
/* 基本設定 */
.post-container {
  font-family: "Helvetica Neue", Arial, "Hiragino Kaku Gothic ProN", "Hiragino Sans", Meiryo, sans-serif;
  background-color: #fff;
  color: #333;
  line-height: 1.6;
  margin: 0;
  padding: 40px;
}

/* コンテナ全体の幅制限 */
#postForm {
  max-width: 800px;
  margin: 0 auto;
}

/* 見出し：新規投稿 */
h1 {
  text-align: center;
  font-size: 24px;
  border-bottom: 1px solid #eee;
  padding-bottom: 20px;
  margin-bottom: 30px;
}

/* 入力行のレイアウト */
.form-group {
  display: flex;
  align-items: flex-start;
  margin-bottom: 25px;
}

/* 各入力とエラーメッセージを縦に並べるラッパー */
.form-group .field {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.form-group .field > input[type="text"],
.form-group .field > select,
.form-group .field > textarea {
  width: 100%;
  box-sizing: border-box;
  flex: none;
}

/* 項目間の区切り */
.form-group:not(.button-container) {
  border-bottom: 1px solid #eee;
  padding-bottom: 18px;
  margin-bottom: 18px;
}

/* ラベルのスタイル */
label {
  width: 120px;
  font-weight: bold;
  padding-top: 10px;
  flex-shrink: 0;
}

/* 入力要素の共通スタイル */
input[type="text"],
select,
textarea {
  flex: 1;
  padding: 12px 15px;
  border: 1px solid #d1d9e0;
  border-radius: 6px;
  font-size: 16px;
  color: #333;
  background-color: #fafbfc;
  transition: border-color 0.2s;
}

/* フォーカス時の色 */
input[type="text"]:focus,
select:focus,
textarea:focus {
  outline: none;
  border-color: #0084d1;
  background-color: #fff;
}

/* 内容（textarea）の高さ */
textarea {
  min-height: 200px;
  resize: vertical;
}

/* ボタンエリアのレイアウト */
.button-container {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

/* ボタンのスタイル */
.cancel-btn,
input[type="submit"] {
  padding: 12px 24px;
  border-radius: 6px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.cancel-btn {
  background-color: #f6f8fa;
  border: 1px solid #d1d9e0;
  color: #333;
}

.cancel-btn:hover {
  background-color: #f3f4f6;
}

input[type="submit"] {
  background-color: #0084d1;
  border: none;
  color: white;
}

input[type="submit"]:hover {
  background-color: #0066a3;
}

/* エラースタイル */
.invalid {
  border-color: #d73a49 !important;
  background-color: #fff !important;
}

.error-msg {
  color: #d73a49;
  font-size: 14px;
  margin-top: 5px;
  min-height: 18px;
}
</style>