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
  return d.toLocaleString('ja-JP', {
    year: 'numeric',
    month: 'numeric',
    day: 'numeric',
    hour: 'numeric',
    minute: 'numeric'
  }); // YYYY/MM/DD HH:mm
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

    <div v-else-if="article" class="container">
      <!-- 戻るボタン（左上・横長） -->
      <button class="back-button" @click="backToHome">
        ← 記事一覧へ戻る
      </button>

      <!-- メイン -->
      <div class="main">
        <h1 class="title">{{ article.title }}</h1>

        <div class="meta">
          <span class="author">{{ article.user_id }}</span>
          <span class="genre">プログラミング</span>
          <span class="date">{{ formatDate(article.created_at) }}</span>
        </div>

        <div class="body">
          {{ article.body }}
        </div>
      </div>
    </div>

    <div v-else class="container">
      <button class="back-button" @click="backToHome">
        ← 記事一覧へ戻る
      </button>
      <div class="main">
        <p>記事が見つかりませんでした。</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page {
  display: flex;
  justify-content: center;
  padding: 40px;
  background: #f5f5f5;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
}

.back-button {
  display: inline-block;
  padding: 10px 24px;
  margin-bottom: 20px;
  background: white;
  border: 2px solid #2693B4;
  color: #2693B4;
  border-radius: 999px;
  font-size: 14px;
  cursor: pointer;
  transition: 0.2s;
}

.back-button:hover {
  background: #2693B4;
  color: white;
}

.main {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.title {
  font-size: 24px;
  margin-bottom: 16px;
}

.meta {
  display: flex;
  flex-direction: column;
  gap: 6px;
  color: #666;
  margin-bottom: 20px;
  font-size: 14px;
}

.meta span::before {
  font-weight: bold;
  color: #333;
  margin-right: 6px;
}

.author::before {
  content: "投稿者ID:";
}

.genre::before {
  content: "ジャンル:";
}

.date::before {
  content: "投稿日:";
}

.body {
  white-space: pre-wrap;
  line-height: 1.7;
}

/* ヘッダー装飾 */
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
