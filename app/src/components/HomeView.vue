<script setup lang="ts">
import { ref, computed } from 'vue';

// --- 1. データ管理（ダミーデータ：後にAPI接続） ---
const posts = ref([
  { 
    id: 1, 
    title: "ReactとVue.jsの違いについて", 
    content: "サーバーサイド専攻ですが、フロントエンドの基礎を固めるために比較しました。どちらも一長一短ありますね。", 
    author: "Mahiro", 
    category: "プログラミング", 
    likes: 15, 
    comments: 4, 
    createdAt: "2026-04-22 18:00" 
  },
  { 
    id: 2, 
    title: "FastAPIでのDB接続エラー解決策", 
    content: "PostgreSQLとの連携でバリデーションエラーが出た際の対処法です。Pydanticモデルの定義を見直しましょう。", 
    author: "サーバー担当A", 
    category: "サーバーサイド", 
    likes: 10, 
    comments: 2, 
    createdAt: "2026-04-23 10:00" 
  },
  { 
    id: 3, 
    title: "ポートフォリオのデザイン案", 
    content: "見やすいWebサイトを作るための配色の基本をまとめました。余白の使い方が重要です。", 
    author: "佐藤", 
    category: "デザイン", 
    likes: 20, 
    comments: 5, 
    createdAt: "2026-04-21 12:00" 
  }
]);

const categories = ["すべて", "プログラミング", "サーバーサイド", "デザイン", "その他"];

// --- 2. 状態管理（検索・カテゴリー・ソート） ---
const searchQuery = ref("");
const selectedCategory = ref("すべて");
const sortOrder = ref<'desc' | 'asc'>('desc'); // desc: 新着順, asc: 古い順

// --- 3. 検索・絞り込み・ソートの統合ロジック ---
const filteredAndSortedPosts = computed(() => {
  // ① まずは検索ワードとカテゴリーで絞り込む
  let result = posts.value.filter(post => {
    const isCategoryMatch = selectedCategory.value === "すべて" || post.category === selectedCategory.value;
    const isSearchMatch = post.title.includes(searchQuery.value) || post.content.includes(searchQuery.value);
    return isCategoryMatch && isSearchMatch;
  });

  // ② 次に日付で並び替える（元のデータを壊さないようコピーしてから実行）
  return [...result].sort((a, b) => {
    const dateA = new Date(a.createdAt).getTime();
    const dateB = new Date(b.createdAt).getTime();
    
    return sortOrder.value === 'desc' 
      ? dateB - dateA  // 新着順（大きい順）
      : dateA - dateB; // 古い順（小さい順）
  });
});
</script>

<template>
  <div class="full-screen-container">
    
    <header class="main-header">
      <div class="header-inner">
        <h1 class="logo">プログラミング情報共有サイト</h1>
        <div class="search-bar">
          <input 
            v-model="searchQuery" 
            type="text" 
            placeholder="キーワードから知恵を探す..." 
          />
          <button class="search-button">🔍 検索</button>
        </div>
        <button class="post-button">＋ 質問する</button>
      </div>
    </header>

    <div class="content-wrapper">
      
      <aside class="sidebar">
        <h2 class="section-title">カテゴリー</h2>
        <ul class="category-list">
          <li 
            v-for="cat in categories" 
            :key="cat" 
            class="category-item"
            :class="{ 'active-cat': selectedCategory === cat }"
            @click="selectedCategory = cat"
          >
            {{ cat }}
            <span class="arrow">▶</span>
          </li>
        </ul>
      </aside>

      <main class="main-content">
        <div class="list-header">
          <h2 class="section-title">
            {{ selectedCategory }}の質問 ({{ filteredAndSortedPosts.length }}件)
          </h2>
          
          <div class="sort-tabs">
            <button 
              class="tab" 
              :class="{ active: sortOrder === 'desc' }" 
              @click="sortOrder = 'desc'"
            >
              新着順
            </button>
            <button 
              class="tab" 
              :class="{ active: sortOrder === 'asc' }" 
              @click="sortOrder = 'asc'"
            >
              古い順
            </button>
          </div>
        </div>

        <div class="post-list">
          <article v-for="post in filteredAndSortedPosts" :key="post.id" class="post-card">
            <div class="post-header">
              <span class="category-badge">{{ post.category }}</span>
              <span class="post-date">{{ post.createdAt }}</span>
            </div>
            
            <h3 class="post-title">{{ post.title }}</h3>
            <p class="post-summary">{{ post.content }}</p>
            
            <div class="post-footer">
              <span class="author-name">👤 {{ post.author }}</span>
              <div class="post-stats">
                <span class="stat">💬 {{ post.comments }}</span>
                <span class="stat">👍 {{ post.likes }}</span>
              </div>
            </div>
          </article>

          <div v-if="filteredAndSortedPosts.length === 0" class="no-results">
            「{{ searchQuery }}」に一致する質問は見つかりませんでした。
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<style scoped>
/* 全画面対応と基本レイアウト */
.full-screen-container {
  width: 100%;
  min-height: 100vh;
  background-color: #f0f2f5;
  font-family: sans-serif;
  margin: 0;
  padding: 0;
}

.main-header {
  width: 100%;
  background-color: #fff;
  border-bottom: 1px solid #ddd;
  padding: 15px 0;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-inner {
  width: 100%;
  padding: 0 40px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-sizing: border-box;
}

.logo {
  font-size: 24px;
  color: #007bff;
  margin: 0;
}

.search-bar {
  flex: 1;
  max-width: 600px;
  margin: 0 30px;
  display: flex;
  border: 2px solid #007bff;
  border-radius: 4px;
}

.search-bar input {
  flex: 1;
  border: none;
  padding: 10px;
  outline: none;
}

.search-button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 0 20px;
  cursor: pointer;
}

.post-button {
  background-color: #ff5a5f;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
}

/* 2カラムレイアウト設定 */
.content-wrapper {
  display: grid;
  grid-template-columns: 250px 1fr;
  width: 100%;
  padding: 30px 40px;
  box-sizing: border-box;
  gap: 30px;
}

.sidebar {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  height: fit-content;
}

.section-title {
  font-size: 18px;
  margin-bottom: 15px;
  border-bottom: 2px solid #007bff;
  padding-bottom: 5px;
}

/* カテゴリー項目の装飾 */
.category-list {
  list-style: none;
  padding: 0;
}

.category-item {
  padding: 12px 10px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.active-cat {
  color: #007bff;
  font-weight: bold;
  background-color: #e7f3ff;
  border-radius: 4px;
}

.category-item:hover {
  background-color: #f8f9fa;
  color: #007bff;
}

/* ソートボタン設定 */
.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.sort-tabs {
  display: flex;
  gap: 10px;
}

.tab {
  background-color: #fff;
  border: 1px solid #ddd;
  padding: 8px 16px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 13px;
}

.tab.active {
  background-color: #007bff;
  color: white;
  border-color: #007bff;
}

/* 記事カード装飾 */
.post-card {
  background-color: #fff;
  padding: 25px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.post-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  font-size: 12px;
  color: #888;
}

.category-badge {
  background-color: #e7f3ff;
  color: #007bff;
  padding: 4px 8px;
  border-radius: 4px;
}

.post-title {
  font-size: 20px;
  margin: 0 0 10px 0;
  color: #333;
}

.post-summary {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 15px;
}

.post-footer {
  display: flex;
  justify-content: space-between;
  padding-top: 15px;
  border-top: 1px solid #eee;
  font-size: 13px;
  color: #555;
}

.post-stats {
  display: flex;
  gap: 15px;
}

.no-results {
  text-align: center;
  padding: 100px 0;
  color: #999;
}
</style>