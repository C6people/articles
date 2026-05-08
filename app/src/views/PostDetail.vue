<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { fetchArticleById, type Article } from '@/api/articles';

const route = useRoute();
const router = useRouter();
const article = ref<Article | null>(null);
const loading = ref(true);
const searchQuery = ref("");

onMounted(async () => {
  const id = route.params.id as string;
  try {
    article.value = await fetchArticleById(id);
  } catch (e) {
    console.error("記事が見つかりませんでした");
  } finally {
    loading.value = false;
  }
});

const formatDate = (dateStr: string | Date | undefined) => {
  if (!dateStr) return "";
  const safeDateStr = typeof dateStr === 'string' && !dateStr.endsWith('Z') && !dateStr.includes('+') ? dateStr + 'Z' : dateStr;
  const d = new Date(safeDateStr);
  const yyyy = d.getFullYear();
  const mm = String(d.getMonth() + 1).padStart(2, '0');
  const dd = String(d.getDate()).padStart(2, '0');
  const hh = String(d.getHours()).padStart(2, '0');
  const min = String(d.getMinutes()).padStart(2, '0');
  return `${yyyy}-${mm}-${dd} ${hh}:${min}`;
};

const backToHome = () => {
  router.push("/");
};

const goToPost = () => {
  router.push("/post");
};
</script>

<template>
  <header class="main-header">
    <div class="header-inner">
      <h1 class="logo" @click="backToHome">
        プログラミング情報共有サイト
      </h1>
      <div class="search-bar">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="キーワードから知恵を探す..."
        />
        <button class="search-button">🔍 検索</button>
      </div>
      <button class="post-button" @click="goToPost">＋ 質問する</button>
    </div>
  </header>

  <div class="page">
    <div v-if="loading">読み込み中...</div>

    <div v-else-if="article" class="content-wrapper">
      <!-- 左カラム：メイン記事と戻るボタン -->
      <div class="left-column">
        <button class="back-button" @click="backToHome">
          記事一覧へ戻る
        </button>

        <div class="main-card">
          <h1 class="title">{{ article.title }}</h1>
          <div class="author-name">{{ article.user_id }}</div>
          <div class="category-badge">プログラミング</div>
          <div class="post-date">投稿日時 &nbsp;&nbsp;{{ formatDate(article.created_at) }}</div>

          <div class="body-content">
            {{ article.body }}
          </div>
        </div>
      </div>

      <!-- 右カラム：サイドバー -->
      <aside class="sidebar">
        <h2 class="sidebar-title">おすすめ記事一覧</h2>
        <ul class="recommended-list">
          <li>FastAPIでのDB接続エラー解決策</li>
          <li>ポートフォリオのデザイン案</li>
        </ul>
      </aside>
    </div>

    <div v-else class="content-wrapper">
      <div class="left-column">
        <button class="back-button" @click="backToHome">
          記事一覧へ戻る
        </button>
        <div class="main-card">
          <p>記事が見つかりませんでした。</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 全体の背景と配置 */
.page {
  background-color: #f0f2f5;
  min-height: 100vh;
  padding: 40px;
  display: flex;
  justify-content: center;
}

/* 2カラムレイアウト */
.content-wrapper {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 40px;
  width: 100%;
  max-width: 1100px;
}

/* 左カラム */
.left-column {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

/* 戻るボタン */
.back-button {
  display: inline-block;
  padding: 8px 24px;
  margin-bottom: 20px;
  background: transparent;
  border: 1px solid #2693B4;
  color: #2693B4;
  border-radius: 999px;
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
  transition: 0.2s;
}

.back-button:hover {
  background: #2693B4;
  color: white;
}

/* 記事カード */
.main-card {
  width: 100%;
  background: white;
  padding: 60px 50px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
  box-sizing: border-box;
}

.title {
  font-size: 28px;
  font-weight: bold;
  color: #333;
  margin: 0 0 15px 0;
  line-height: 1.4;
}

.author-name {
  font-size: 15px;
  color: #555;
  margin-bottom: 15px;
}

.category-badge {
  display: inline-block;
  background-color: #2693B4;
  color: white;
  padding: 6px 18px;
  border-radius: 999px;
  font-size: 13px;
  font-weight: bold;
  margin-bottom: 25px;
}

.post-date {
  font-size: 13px;
  color: #999;
  margin-bottom: 50px;
}

.body-content {
  white-space: pre-wrap;
  line-height: 2.0;
  color: #444;
  font-size: 16px;
}

/* サイドバー */
.sidebar {
  padding-top: 60px; /* 記事カードの上部と大体合わせる */
}

.sidebar-title {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  padding-bottom: 15px;
  border-bottom: 1px solid #999;
  margin: 0 0 10px 0;
}

.recommended-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.recommended-list li {
  padding: 20px 0;
  border-bottom: 1px solid #ccc;
  font-size: 14px;
  color: #555;
  cursor: pointer;
  line-height: 1.5;
}

.recommended-list li:hover {
  color: #2693B4;
}

/* ヘッダー装飾（既存そのまま） */
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
  cursor: pointer;
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
</style>
