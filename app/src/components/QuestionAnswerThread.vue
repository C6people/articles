<template>
  <div class="qa-thread">
    <!-- 回答投稿フォーム -->
    <form class="answer-form" @submit.prevent="submitAnswer">
      <h3 class="form-title">回答する</h3>
      <textarea
        v-model="newAnswerText"
        placeholder="この質問に対する回答を入力..."
        rows="4"
      />
      <button type="submit" :disabled="!newAnswerText.trim()">回答を投稿</button>
    </form>

    <!-- 回答件数 -->
    <h3 class="answer-count">{{ answers.length }} 件の回答</h3>

    <!-- 回答一覧（ベストアンサーを先頭に表示） -->
    <div v-for="answer in sortedAnswers" :key="answer.id" class="answer-card" :class="{ 'is-best': answer.is_best }">
      <!-- ベストアンサーバッジ -->
      <div v-if="answer.is_best" class="best-badge">⭐ ベストアンサー</div>

      <div class="answer-header">
        <span class="answer-user">{{ answer.user_id.slice(0, 8) }}</span>
        <span class="answer-date">{{ formatDate(answer.created_at) }}</span>
      </div>
      <div class="answer-body">{{ answer.body }}</div>

      <div class="answer-actions">
        <!-- ベストアンサー選択ボタン（質問者のみ） -->
        <button
          v-if="isQuestionOwner && !answer.is_best"
          class="best-btn"
          @click="markBest(answer.id)"
        >
          ベストアンサーに選ぶ
        </button>

        <!-- コメント表示/非表示トグル -->
        <button class="toggle-comments-btn" @click="toggleComments(answer.id)">
          💬 コメント ({{ getSubComments(answer.id).length }})
        </button>
      </div>

      <!-- コメント一覧（フラット・1階層） -->
      <div v-if="expandedAnswers.has(answer.id)" class="sub-comments">
        <div v-for="comment in getSubComments(answer.id)" :key="comment.id" class="sub-comment">
          <div class="sub-comment-header">
            <span class="sub-comment-user">{{ comment.user_id.slice(0, 8) }}</span>
            <span class="sub-comment-date">{{ formatDate(comment.created_at) }}</span>
          </div>
          <div class="sub-comment-body">{{ comment.body }}</div>
        </div>

        <!-- コメント入力 -->
        <form class="sub-comment-form" @submit.prevent="submitSubComment(answer.id)">
          <input
            v-model="subCommentTexts[answer.id]"
            type="text"
            placeholder="コメントを追加..."
          />
          <button type="submit" :disabled="!subCommentTexts[answer.id]?.trim()">送信</button>
        </form>
      </div>
    </div>

    <!-- 回答がない場合 -->
    <div v-if="answers.length === 0" class="no-answers">
      まだ回答がありません。最初の回答を投稿しましょう！
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, reactive } from 'vue';
import {
  fetchQuestionComments,
  postQuestionComment,
  setBestAnswer,
  type QuestionCommentResponse,
} from '@/api/questionComments';

const props = defineProps<{
  questionId: string;
  questionUserId: string; // 質問の投稿者ID（ベストアンサー権限判定用）
}>();

const allComments = ref<QuestionCommentResponse[]>([]);
const newAnswerText = ref('');
const expandedAnswers = ref(new Set<string>());
const subCommentTexts = reactive<Record<string, string>>({});

// 現在のユーザーID（トークンから取得）
const currentUserId = computed(() => {
  const token = localStorage.getItem('token');
  if (!token) return '';
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    return payload.user_id || '';
  } catch {
    return '';
  }
});

// 質問の投稿者かどうか
const isQuestionOwner = computed(() => currentUserId.value === props.questionUserId);

// 回答一覧（is_answer: true かつ parent_id: null）
const answers = computed(() =>
  allComments.value.filter(c => c.is_answer && !c.parent_id)
);

// ベストアンサーを先頭にソート
const sortedAnswers = computed(() =>
  [...answers.value].sort((a, b) => {
    if (a.is_best && !b.is_best) return -1;
    if (!a.is_best && b.is_best) return 1;
    return new Date(a.created_at).getTime() - new Date(b.created_at).getTime();
  })
);

// 回答に対するコメント一覧
const getSubComments = (answerId: string) =>
  allComments.value.filter(c => c.parent_id === answerId);

const loadComments = async () => {
  try {
    allComments.value = await fetchQuestionComments(props.questionId);
  } catch (error) {
    console.error('Failed to load comments:', error);
  }
};

onMounted(loadComments);

async function submitAnswer() {
  if (!newAnswerText.value.trim()) return;
  try {
    await postQuestionComment(props.questionId, {
      body: newAnswerText.value,
      is_answer: true,
    });
    newAnswerText.value = '';
    await loadComments();
  } catch (error) {
    console.error('Failed to post answer:', error);
    alert('回答の投稿に失敗しました。');
  }
}

async function submitSubComment(answerId: string) {
  const text = subCommentTexts[answerId];
  if (!text?.trim()) return;
  try {
    await postQuestionComment(props.questionId, {
      body: text,
      parent_id: answerId,
      is_answer: false,
    });
    subCommentTexts[answerId] = '';
    await loadComments();
  } catch (error) {
    console.error('Failed to post comment:', error);
    alert('コメントの投稿に失敗しました。');
  }
}

async function markBest(commentId: string) {
  try {
    await setBestAnswer(props.questionId, commentId);
    await loadComments();
  } catch (error: any) {
    const msg = error?.response?.data?.detail || 'ベストアンサーの設定に失敗しました。';
    alert(msg);
  }
}

function toggleComments(answerId: string) {
  if (expandedAnswers.value.has(answerId)) {
    expandedAnswers.value.delete(answerId);
  } else {
    expandedAnswers.value.add(answerId);
  }
}

const formatDate = (dateStr: string) => {
  const safeDateStr = !dateStr.endsWith('Z') && !dateStr.includes('+') ? dateStr + 'Z' : dateStr;
  const d = new Date(safeDateStr);
  const yyyy = d.getFullYear();
  const mm = String(d.getMonth() + 1).padStart(2, '0');
  const dd = String(d.getDate()).padStart(2, '0');
  const hh = String(d.getHours()).padStart(2, '0');
  const min = String(d.getMinutes()).padStart(2, '0');
  return `${yyyy}-${mm}-${dd} ${hh}:${min}`;
};
</script>

<style scoped>
.qa-thread {
  margin-top: 0;
  padding: 0 0 40px 0;
}

/* 回答フォーム */
.answer-form {
  margin-bottom: 32px;
}
.form-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 10px;
  color: #333;
}
.answer-form textarea {
  width: 100%;
  border-radius: 8px;
  border: 1px solid #ccc;
  padding: 12px;
  font-size: 15px;
  resize: vertical;
  box-sizing: border-box;
  transition: border 0.2s;
}
.answer-form textarea:focus {
  border-color: #2693B4;
  outline: none;
}
.answer-form button {
  margin-top: 10px;
  background: #2693B4;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 10px 24px;
  font-size: 15px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.2s;
}
.answer-form button:hover {
  background: #1e7d9a;
}
.answer-form button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

/* 回答件数 */
.answer-count {
  font-size: 16px;
  color: #555;
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 1px solid #e0e0e0;
}

/* 回答カード */
.answer-card {
  background: white;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  padding: 20px 24px;
  margin-bottom: 16px;
  transition: box-shadow 0.2s;
}
.answer-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}
.answer-card.is-best {
  border: 2px solid #28a745;
  background: #f6fff8;
}

/* ベストアンサーバッジ */
.best-badge {
  display: inline-block;
  background: #28a745;
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: bold;
  margin-bottom: 10px;
}

.answer-header {
  font-size: 13px;
  color: #888;
  margin-bottom: 8px;
}
.answer-user {
  font-weight: bold;
  color: #2693B4;
  margin-right: 10px;
}
.answer-date {
  color: #aaa;
}
.answer-body {
  font-size: 15px;
  line-height: 1.7;
  color: #333;
  white-space: pre-wrap;
  margin-bottom: 12px;
}

/* 回答アクション */
.answer-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}
.best-btn {
  background: none;
  border: 1px solid #28a745;
  color: #28a745;
  padding: 4px 14px;
  border-radius: 20px;
  font-size: 13px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.2s;
}
.best-btn:hover {
  background: #28a745;
  color: white;
}
.toggle-comments-btn {
  background: none;
  border: none;
  color: #888;
  font-size: 13px;
  cursor: pointer;
}
.toggle-comments-btn:hover {
  color: #2693B4;
}

/* サブコメント */
.sub-comments {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #eee;
}
.sub-comment {
  padding: 8px 0;
  border-bottom: 1px solid #f5f5f5;
}
.sub-comment-header {
  font-size: 12px;
  color: #aaa;
  margin-bottom: 4px;
}
.sub-comment-user {
  font-weight: bold;
  color: #2693B4;
  margin-right: 8px;
}
.sub-comment-date {
  color: #ccc;
}
.sub-comment-body {
  font-size: 14px;
  color: #555;
}

/* コメント入力 */
.sub-comment-form {
  display: flex;
  gap: 8px;
  margin-top: 10px;
}
.sub-comment-form input {
  flex: 1;
  border: 1px solid #ddd;
  border-radius: 6px;
  padding: 6px 10px;
  font-size: 13px;
  outline: none;
}
.sub-comment-form input:focus {
  border-color: #2693B4;
}
.sub-comment-form button {
  background: #2693B4;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 6px 14px;
  font-size: 13px;
  cursor: pointer;
}
.sub-comment-form button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

/* 回答なし */
.no-answers {
  text-align: center;
  color: #999;
  padding: 40px;
  font-size: 14px;
}
</style>
