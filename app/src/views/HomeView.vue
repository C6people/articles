<script setup lang="ts">

import { ref, computed, onMounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { fetchArticles } from '@/api/articles';
import type { Article } from '@/api/articles';
import CommonHeader from '@/components/CommonHeader.vue';

const categories = ["すべて", "プログラミング", "質問", "コラム", "その他"];
// --- 1. データ管理（API接続） ---
const posts = ref<Article[]>([]);

onMounted(async () => {
  try {
    posts.value = await fetchArticles();
  } catch (e) {
    // エラー時は空配列のまま
    // 必要に応じてエラーメッセージ表示も可
  }
});

/* 2. 状態管理（検索・カテゴリー・ソート） */
const searchQuery = ref("");
const selectedCategory = ref("すべて");
const sortOrder = ref<"desc" | "asc">("desc"); // desc: 新着順, asc: 古い順
const router = useRouter();
const route = useRoute();

// ----------------------------------------------------
// 暫定的なロジック：しょうもないURLクエリパラメータ監視ロジック（後で消す）0507
// URLのクエリパラメータを監視して、searchQueryに反映させるロジック
// 【追加】URLの ?q=... を監視して、searchQuery に代入する
watch(
  () => route.query.q,
  (newVal) => {
    // query は string | string[] | undefined の可能性がある
    const q = Array.isArray(newVal) ? newVal[0] : newVal;
    searchQuery.value = (q as string) || "";
  },
  { immediate: true } // 画面が開いた瞬間も実行する
);
// ----------------------------------------------------

/*  3. 検索・絞り込み・ソートの統合ロジック */
const filteredAndSortedPosts = computed(() => {
  /* ① まずは検索ワードとカテゴリーで絞り込む */
  let result = posts.value.filter((post) => {
    const isCategoryMatch =
      selectedCategory.value === "すべて" ||
      post.category === selectedCategory.value;
    // 検索語や記事のフィールドが undefined でも安全に扱えるようにする
    const q = (searchQuery.value || "").toString().toLowerCase();
    const title = (post.title || "").toString().toLowerCase();
    const bodyOrContent = (post.content ?? post.body ?? "").toString().toLowerCase();
    const isSearchMatch = title.includes(q) || bodyOrContent.includes(q);
    return isCategoryMatch && isSearchMatch;
  });

  /* ② 次に日付で並び替える（元のデータを壊さないようコピーしてから実行） */
  return [...result].sort((a, b) => {
    // created_atが不正な場合は0とみなす
    const dateA = a.created_at ? new Date(a.created_at).getTime() : 0;
    const dateB = b.created_at ? new Date(b.created_at).getTime() : 0;
    return sortOrder.value === 'desc' 
      ? dateB - dateA  // 新着順（大きい順）
      : dateA - dateB; // 古い順（小さい順）
  });
});

// 記事詳細画面へ遷移
const goToPost = () => {
  router.push("/post");
};
const goToDetail = (id: string) => {
  router.push({ name: 'PostDetail', params: { id } });
};

// 日付をTwitter風の相対時間で表示するフォーマット関数
const formatDate = (dateStr: string | undefined) => {
  if (!dateStr) return '';
  // UTCとして解釈させるため、タイムゾーン表記がない場合は 'Z' を補完する
  const safeDateStr = dateStr.endsWith('Z') || dateStr.includes('+') ? dateStr : dateStr + 'Z';
  const date = new Date(safeDateStr);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffSec = Math.floor(diffMs / 1000);
  const diffMin = Math.floor(diffSec / 60);
  const diffHour = Math.floor(diffMin / 60);
  const diffDay = Math.floor(diffHour / 24);

  if (diffSec < 60) {
    // 0秒未満（未来）のズレがあった場合は数秒前とする
    return diffSec <= 0 ? '数秒前' : `${diffSec}秒前`;
  } else if (diffMin < 60) {
    return `${diffMin}分前`;
  } else if (diffHour < 24) {
    return `${diffHour}時間前`;
  } else if (diffDay < 7) {
    return `${diffDay}日前`;
  } else {
    // 1週間以上前なら日付のみ
    return date.toLocaleDateString('ja-JP'); 
  }
};
</script>

<template>
  <div class="full-screen-container">
    
    <CommonHeader />

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
            <button class="tab" :class="{ active: sortOrder === 'desc' }" @click="sortOrder = 'desc'">新着順</button>
            <button class="tab" :class="{ active: sortOrder === 'asc' }" @click="sortOrder = 'asc'">古い順</button>
          </div>
        </div>

        <div class="post-list">
          <article 
            v-for="post in filteredAndSortedPosts" 
            :key="post.id" 
            class="post-card"
            @click="goToDetail(post.id)"
          >
            <div class="post-header">
              <span class="category-badge">{{ post.category }}</span>
              <span class="post-date">{{ formatDate(post.created_at) }}</span>
            </div>
            <h3 class="post-title">{{ post.title }}</h3>
            <p class="post-summary">{{ post.content }}</p>
            <div class="post-footer">
              <span class="author-name">👤 ID: {{ post.user_id }}</span>
              <div class="post-stats">
                <span class="stat">💬 コメント {{ post.comments }}</span>
                <span class="stat">👍 高評価 {{ post.likes }}</span>
              </div>
            </div>
          </article>

          <div v-if="filteredAndSortedPosts.length === 0" class="no-results">
            「{{ searchQuery }}」に一致する記事は見つかりませんでした。
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
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.post-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
  cursor: pointer;
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
  hover {
    color: #007bff;
    cursor: pointer;
  }
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
