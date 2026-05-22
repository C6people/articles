<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import CommonHeader from '@/components/CommonHeader.vue';
import { fetchArticleById, type Article } from '@/api/articles';
import { fetchQuestionById } from '@/api/questions';
import { likeArticle, likeQuestion, unlikeArticle, unlikeQuestion } from '@/api/likes';
import CommentThread from '@/components/CommentThread.vue';
import QuestionAnswerThread from '@/components/QuestionAnswerThread.vue';

const route = useRoute();
const router = useRouter();
const article = ref<Article | null>(null);
const loading = ref(true);
const contentId = ref('');
const contentType = ref<'article' | 'question'>('article');

const handleLike = async () => {
  if (!article.value) return;
  const isLiked = article.value.is_liked;
  try {
    let res;
    if (isLiked) {
      if (contentType.value === 'question') {
        res = await unlikeQuestion(contentId.value);
      } else {
        res = await unlikeArticle(contentId.value);
      }
    } else {
      if (contentType.value === 'question') {
        res = await likeQuestion(contentId.value);
      } else {
        res = await likeArticle(contentId.value);
      }
    }
    article.value.likes_count = res.likes_count;
    article.value.is_liked = !isLiked;
  } catch (error: any) {
    const msg = error?.response?.data?.detail || '処理に失敗しました。';
    alert(msg);
  }
};

const getUserIdFromToken =
(): string => {

    const token =
        localStorage.getItem('token');

    if (!token) return '';

    const tokenParts =
        token.split('.');

    if (tokenParts.length < 2) {
        return '';
    }

    const payload =
        JSON.parse(
            atob(tokenParts[1] ?? '')
        );

    return String(
        payload.user_id ?? ''
    );
};

onMounted(async () => {
  const id = route.params.id as string;
  const type = route.query.type as string; // 'question' or 'article'
  contentId.value = id;
  contentType.value = type === 'question' ? 'question' : 'article';

  try {
    if (type === 'question') {
      const q = await fetchQuestionById(id);
      article.value = {
        id: q.id,
        user_id: q.user_id,
        user_name: q.user_name,
        title: q.title,
        body: q.body,
        content: q.body,
        author: q.user_name || '',
        category: '質問',
        likes_count: q.likes_count,
        is_liked: q.is_liked,
        comments: 0,
        created_at: q.created_at,
      };
    } else {
      article.value = await fetchArticleById(id);
    }
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

const backToHome = () => router.push("/");
const goToPost = () => router.push("/post");
const goToUserProfile = (
    userId?: string | number
) => {

    if (!userId) return;

    const myUserId =
        getUserIdFromToken();

    const clickedUserId =
        String(userId);

    console.log(
        'clicked:',
        clickedUserId
    );

    console.log(
        'me:',
        myUserId
    );

    if (
        clickedUserId ===
        String(myUserId)
    ) {
        router.push('/profile');
    } else {
        router.push(
            `/users/${clickedUserId}`
        );
    }
};
</script>

<template>
  <div class="full-screen-container">
    <CommonHeader />

    <div class="content-wrapper">
      <aside class="sidebar">
        <h2 class="sidebar-title">おすすめ記事一覧</h2>
        <ul class="recommended-list">
          <li>FastAPIでのDB接続エラー解決策</li>
          <li>ポートフォリオのデザイン案</li>
        </ul>
      </aside>

      <main class="main-content">
        <div v-if="loading" class="loading-text">読み込み中...</div>

        <template v-else-if="article">
          <button class="back-button" @click="backToHome">
            ← 記事一覧へ戻る
          </button>

          <section class="main-card article-section">
            <h1 class="title">{{ article.title }}</h1>
            <div class="author-name clickable-user" @click.stop="goToUserProfile(article.user_id)">
              👤 {{ article.user_name || '不明' }}
            </div>
            <div class="category-badge">{{ article.category }}</div>
            <div class="post-date">投稿日時 &nbsp;&nbsp;{{ formatDate(article.created_at) }}</div>
            
            <div class="article-actions">
              <button class="like-button" :class="{ 'is-active': article.is_liked }" @click="handleLike">
                <span class="like-icon">👍</span> いいね <span class="like-count">{{ article.likes_count }}</span>
              </button>
            </div>

            <div class="body-content">
              {{ article.body }}
            </div>
          </section>

          <!-- 質問の場合：Q&A特化UI -->
          <section v-if="contentType === 'question'" class="main-card comment-section">
            <h2 class="comment-count">回答</h2>
            <QuestionAnswerThread
              :questionId="contentId"
              :questionUserId="article.user_id"
            />
          </section>

          <!-- 記事の場合：通常コメント -->
          <section v-else class="main-card comment-section">
            <h2 class="comment-count">コメント</h2>
            <CommentThread :contentId="contentId" :contentType="contentType" />
          </section>
        </template>

        <template v-else>
          <button class="back-button" @click="backToHome">← 記事一覧へ戻る</button>
          <div class="main-card">
            <p>記事が見つかりませんでした。</p>
          </div>
        </template>
      </main>
    </div>
  </div>
</template>

<style scoped>
/* レイアウト */
.full-screen-container {
  width: 100%;
  min-height: 100vh;
  background-color: #f0f2f5;
  font-family: sans-serif;
}

.content-wrapper {
  display: grid;
  grid-template-columns: 250px 1fr;
  max-width: 1200px;
  margin: 0 auto;
  padding: 30px 20px;
  gap: 30px;
}

/* 共通カードスタイル */
.main-card {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
  margin-bottom: 20px;
}

/* 記事詳細 */
.title {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 15px;
}

.category-badge {
  display: inline-block;
  background-color: #2693B4;
  color: white;
  padding: 4px 14px;
  border-radius: 20px;
  font-size: 13px;
  margin: 20px 0 20px 0;
}

.article-actions {
  margin: 15px 0;
}

.like-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background-color: #fff;
  border: 1px solid #ddd;
  padding: 8px 16px;
  border-radius: 20px;
  cursor: pointer;
  font-size: 14px;
  color: #555;
  transition: all 0.2s ease;
  font-weight: bold;
}

.like-button:hover {
  background-color: #f0f8ff;
  border-color: #2693B4;
  color: #2693B4;
  transform: scale(1.03);
}

.like-button:active {
  transform: scale(0.97);
}

.like-button.is-active {
  background-color: #e7f3ff;
  border-color: #007bff;
  color: #007bff;
}

.like-button.is-active:hover {
  background-color: #d0e7ff;
  border-color: #0056b3;
  color: #0056b3;
}

.body-content {
  white-space: pre-wrap;
  line-height: 1.8;
  color: #333;
  font-size: 16px;
}

/* コメント欄 */
.comment-section {
  padding-top: 30px;
}

.comment-count {
  font-size: 18px;
  margin-bottom: 20px;
}

.new-comment-input {
  display: flex;
  gap: 15px;
  margin-bottom: 30px;
}

.user-avatar {
  font-size: 32px;
}

.input-container {
  flex: 1;
}

.input-container input {
  width: 100%;
  border: none;
  border-bottom: 1px solid #ccc;
  padding: 8px 0;
  outline: none;
}

.input-container input:focus {
  border-bottom: 2px solid #2693B4;
}

.input-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 10px;
}

.submit-btn {
  background: #2693B4;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 20px;
  cursor: pointer;
}

/* その他パーツ */
.back-button {
  background: none;
  border: 3px solid #2693B4;
  color: #2693B4;
  padding: 8px 20px;
  border-radius: 20px;
  cursor: pointer;
  margin-bottom: 20px;
  font-weight: bold;
  transition: ease 0.3s;
}

.back-button:hover {
  background: #2693B4;
  color: white;
}

.sidebar-title {
  margin-top: 70px;
  font-size: 16px;
  border-bottom: 1px solid #ddd;
  padding-bottom: 10px;
}

.recommended-list {
  list-style: none;
  padding: 0;
}

.recommended-list li {
  padding: 15px 0;
  border-bottom: 1px solid #eee;
  font-size: 14px;
  cursor: pointer;
}

.clickable-user {
  cursor: pointer;
  transition: color 0.2s;
}

.clickable-user:hover {
  color: #2693B4;
  text-decoration: underline;
}
</style>