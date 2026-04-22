<script setup lang="ts">
import { useHome } from './homeView'
import '../assets/home.css'

const {
  currentView,
  selectedPost,
  selectedCategory,
  searchQuery,
  categories,
  newPostTitle,
  newPostContent,
  filteredPosts,
  handleCreatePost,
  showDetail,
  goHome,
  goNewPost
} = useHome()
</script>

<template>
  <div class="app-container">
    <!-- ヘッダー -->
    <header class="header">
      <div class="header-content">
        <h1 class="logo" @click="goHome">プログラミング情報共有サイト（仮）</h1>

        <div class="search-container">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="キーワードで検索..."
            class="search-input"
          />
        </div>

        <button @click="goNewPost" class="post-btn">
          <span>投稿する</span>
        </button>
      </div>
    </header>

    <div class="main-layout">
      <!-- サイドバー -->
      <aside class="sidebar">
        <div class="sidebar-card">
          <h2 class="sidebar-title">カテゴリー</h2>
          <nav class="category-nav">
            <button
              @click="selectedCategory = 'all'"
              :class="['category-item', { active: selectedCategory === 'all' }]"
            >
              すべて
            </button>
            <button
              v-for="cat in categories"
              :key="cat.id"
              @click="selectedCategory = cat.id as any"
              :class="['category-item', { active: selectedCategory === cat.id }]"
            >
              {{ cat.name }}
            </button>
          </nav>
        </div>
      </aside>

      <!-- メインコンテンツ -->
      <main class="content">
        <!-- ホーム画面（投稿一覧） -->
        <div v-if="currentView === 'home'" class="post-list">
          <div
            v-for="post in filteredPosts"
            :key="post.id"
            class="post-card"
            @click="showDetail(post)"
          >
            <h3 class="post-title">{{ post.title }}</h3>
            <p class="post-summary">{{ post.content }}</p>
            <div class="post-footer">
              <span class="post-author">{{ post.author }}</span>
              <span class="post-date">{{ post.createdAt }}</span>
              <span class="post-likes">👍 {{ post.likes }}</span>
            </div>
          </div>
        </div>

        <!-- 新規投稿画面 -->
        <div v-if="currentView === 'new'" class="form-card">
          <h2 class="form-title">新規投稿作成</h2>
          <form @submit.prevent="handleCreatePost" class="post-form">
            <input
              v-model="newPostTitle"
              class="form-input"
              placeholder="タイトル"
              required
            />
            <textarea
              v-model="newPostContent"
              class="form-textarea"
              placeholder="プログラミングに関する質問や知見を書いてください"
              required
            ></textarea>
            <div class="form-actions">
              <button type="submit" class="submit-btn">投稿</button>
              <button type="button" @click="goHome" class="cancel-btn">キャンセル</button>
            </div>
          </form>
        </div>

        <!-- 詳細画面 -->
        <div v-if="currentView === 'detail' && selectedPost" class="detail-card">
          <button @click="goHome" class="back-link">← 戻る</button>
          <h2 class="detail-title">{{ selectedPost.title }}</h2>
          <p class="detail-content">{{ selectedPost.content }}</p>
        </div>
      </main>
    </div>
  </div>
</template>

<style scoped>
.app-container {
  min-height: 100vh;
  background-color: #f9fafb;
  color: #111827;
  font-family: sans-serif;
}

.header {
  background-color: white;
  border-bottom: 1px solid #e5e7eb;
  position: sticky;
  top: 0;
  z-index: 50;
  padding: 0.75rem 0;
}

.header-content {
  max-width: 80rem;
  margin: 0 auto;
  padding: 0 1rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
  color: #2563eb;
  cursor: pointer;
}

.search-container {
  flex: 1;
  max-width: 36rem;
}

.search-input {
  width: 100%;
  padding: 0.5rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
  outline: none;
}

.search-input:focus {
  ring: 2px solid #3b82f6;
}

.post-btn {
  background-color: #2563eb;
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  border: none;
  cursor: pointer;
  font-weight: 500;
}

.post-btn:hover {
  background-color: #1d4ed8;
}

.main-layout {
  max-width: 80rem;
  margin: 0 auto;
  padding: 1.5rem 1rem;
  display: flex;
  gap: 1.5rem;
}

.sidebar {
  width: 16rem;
  display: none;
}

@media (min-width: 1024px) {
  .sidebar {
    display: block;
  }
}

.sidebar-card {
  background-color: white;
  border-radius: 0.5rem;
  border: 1px solid #e5e7eb;
  padding: 1rem;
}

.sidebar-title {
  font-weight: bold;
  margin-bottom: 1rem;
}

.category-nav {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.category-item {
  text-align: left;
  padding: 0.5rem 0.75rem;
  border-radius: 0.375rem;
  border: none;
  background: transparent;
  cursor: pointer;
}

.category-item:hover {
  background-color: #f3f4f6;
}

.category-item.active {
  background-color: #eff6ff;
  color: #1d4ed8;
}

.content {
  flex: 1;
}

.post-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.post-card {
  background-color: white;
  padding: 1.5rem;
  border-radius: 0.5rem;
  border: 1px solid #e5e7eb;
  cursor: pointer;
}

.post-card:hover {
  box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
}

.post-title {
  font-size: 1.25rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.post-summary {
  color: #4b5563;
  margin-bottom: 1rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.post-footer {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 0.875rem;
  color: #6b7280;
}

.post-author {
  background-color: #f3f4f6;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
}

.form-card, .detail-card {
  background-color: white;
  padding: 2rem;
  border-radius: 0.5rem;
  border: 1px solid #e5e7eb;
}

.form-title, .detail-title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 1.5rem;
}

.post-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-input, .form-textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 0.5rem;
}

.form-textarea {
  height: 10rem;
}

.form-actions {
  display: flex;
  gap: 0.5rem;
}

.submit-btn {
  background-color: #2563eb;
  color: white;
  padding: 0.5rem 1.5rem;
  border-radius: 0.5rem;
  border: none;
  cursor: pointer;
}

.cancel-btn {
  background-color: #e5e7eb;
  padding: 0.5rem 1.5rem;
  border-radius: 0.5rem;
  border: none;
  cursor: pointer;
}

.back-link {
  color: #2563eb;
  background: none;
  border: none;
  cursor: pointer;
  margin-bottom: 1rem;
  padding: 0;
}

.detail-content {
  color: #1f2937;
  white-space: pre-wrap;
  line-height: 1.6;
}
</style>
