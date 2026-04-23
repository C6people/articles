<script setup lang="ts">
import { ref } from 'vue';
// アイコンは標準的なHTML文字を使用し、ライブラリ依存をなくしてエラーを防ぎます

// --- ダミーデータ（後でAPI接続） ---
const posts = ref([
  {
    id: 1,
    title: "ReactとVue.js、どちらを先に学ぶべきですか？",
    content: "現在IT系の専門学校に通っています。サーバーサイド専攻ですが、フロントエンドの基礎も固めたいです。アドバイスをお願いします。",
    author: "Mahiro",
    category: "プログラミング",
    likes: 15,
    comments: 4,
    createdAt: "2026-04-22 18:00"
  },
  {
    id: 2,
    title: "FastAPIのバリデーションエラーの解決策について",
    content: "Pydanticモデルで定義した型と、送られてくるJSONが一致しない際のエラーハンドリングについて具体的な実装例を知りたいです。",
    author: "サーバー担当A",
    category: "サーバーサイド",
    likes: 10,
    comments: 2,
    createdAt: "2026-04-22 15:30"
  }
]);

const categories = ["すべて", "プログラミング", "サーバーサイド", "デザイン", "その他"];
</script>

<template>
  <div class="full-screen-container">
    
    <header class="main-header">
      <div class="header-inner">
        <h1 class="logo">プログラミング情報共有サイト（仮）</h1>
        <div class="search-bar">
          <input type="text" placeholder="キーワードから知恵を探す" />
          <button class="search-button">🔍 検索</button>
        </div>
        <button class="post-button">＋ 質問する</button>
      </div>
    </header>

    <div class="content-wrapper">
      
      <aside class="sidebar">
        <h2 class="section-title">カテゴリー</h2>
        <ul class="category-list">
          <li v-for="cat in categories" :key="cat" class="category-item">
            {{ cat }}
            <span class="arrow">▶</span>
          </li>
        </ul>
      </aside>

      <main class="main-content">
        <div class="list-header">
          <h2 class="section-title">新着の質問</h2>
          <div class="sort-tabs">
            <button class="tab active">新着順</button>
            <button class="tab">回答数順</button>
          </div>
        </div>

        <div class="post-list">
          <article v-for="post in posts" :key="post.id" class="post-card">
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
        </div>
      </main>
    </div>
  </div>
</template>

<style scoped>
/* --- 全画面対応の肝となるスタイル --- */
.full-screen-container {
  width: 100%; /* 画面横幅いっぱい */
  min-height: 100vh; /* 画面高さいっぱい */
  background-color: #f0f2f5; /* 薄いグレーの背景 */
  font-family: sans-serif;
  margin: 0;
  padding: 0;
}

/* ヘッダー：横幅100%で上部に固定 */
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
  max-width: 100%; /* ここでも幅制限をしない */
  padding: 0 40px; /* 両端に少し余白を取る */
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-sizing: border-box;
}

.logo {
  font-size: 24px;
  color: #007bff; /* 知恵袋カラーの青 */
  margin: 0;
}

.search-bar {
  flex: 1; /* 残りの幅をすべて使用 */
  max-width: 600px; /* 検索窓が広がりすぎないよう上限だけ設定 */
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
  background-color: #ff5a5f; /* 目立つ赤色 */
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 4px;
  font-weight: bold;
  cursor: pointer;
}

/* コンテンツエリア：Gridで全画面幅を分割 */
.content-wrapper {
  display: grid;
  grid-template-columns: 250px 1fr; /* サイドバー固定、メインは残り全部 */
  width: 100%;
  padding: 30px 40px; /* 周囲の余白 */
  box-sizing: border-box;
  gap: 30px; /* サイドバーとメインの間隔 */
}

/* サイドバー */
.sidebar {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  height: fit-content; /* コンテンツに応じた高さ */
}

.section-title {
  font-size: 18px;
  margin-bottom: 15px;
  border-bottom: 2px solid #007bff;
  padding-bottom: 5px;
}

.category-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.category-item {
  padding: 12px 0;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  cursor: pointer;
  font-size: 14px;
}

.category-item:hover {
  color: #007bff;
}

/* メインコンテンツ */
.main-content {
  /* 親の Grid により、残りの幅を自動的に使用 */
}

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
  background: none;
  border: 1px solid #ddd;
  padding: 8px 16px;
  border-radius: 20px;
  cursor: pointer;
  background-color: #fff;
}

.tab.active {
  background-color: #007bff;
  color: white;
  border-color: #007bff;
}

/* 記事カード */
.post-card {
  background-color: #fff;
  padding: 25px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  transition: box-shadow 0.2s;
}

.post-card:hover {
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
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
  color: #333;
  margin: 0 0 10px 0;
}

.post-summary {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 15px;
  /* 3行以上は省略する設定 */
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.post-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 15px;
  border-top: 1px solid #eee;
  font-size: 13px;
  color: #555;
}

.post-stats {
  display: flex;
  gap: 15px;
  color: #888;
}
</style>