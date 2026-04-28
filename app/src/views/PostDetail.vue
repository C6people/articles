<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";

const route = useRoute();
const article = ref(null);
const loading = ref(true);
const router = useRouter();

onMounted(() => {
  // ダミーデータ
  article.value = {
    id: route.params.id,
    title: "ReactとVue.jsの違いについて",
    body: `1. はじめに

普段はNode.jsやPythonでAPIを叩いているサーバーサイド寄りですが、フロントエンドの基礎を固めるために、モダンな2大フレームワークである「React」と「Vue.js」を比較してみました。

2. Vue.js：直感的でHTMLの延長に近い
Vueは構文がシンプルで、学習コストが低いです。

3. React：すべてがJavaScriptの世界
ReactはJS中心で設計されており、柔軟性が高いです。

4. まとめ
用途によって使い分けるのがベストだと感じました。`,
    created_at: "2026-04-22T18:00:00",
    genre: "プログラミング",
    user: {
      name: "Mahiro"
    }
  };

  loading.value = false;
});

const formatDate = (date) => {
  return new Date(date).toLocaleString();
};

const backToHome = () => {
  router.push("/");
};
</script>

<template>
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
          <span class="author">{{ article.user?.name }}</span>
          <span class="genre">{{ article.genre }}</span>
          <span class="date">{{ formatDate(article.created_at) }}</span>
        </div>

        <div class="body">
          {{ article.body }}
        </div>
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
  width: 800px;
}

/* 横長ボタン（変更なし） */
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

/* ★ 影追加 */
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

/* ★ 縦並びに変更 */
.meta {
  display: flex;
  flex-direction: column;
  gap: 6px;
  color: #666;
  margin-bottom: 20px;
  font-size: 14px;
}

/* 見やすくする */
.meta span::before {
  font-weight: bold;
  color: #333;
  margin-right: 6px;
}

.author::before {
  content: "投稿者:";
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
</style>