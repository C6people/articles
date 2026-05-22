<template>
  <div class="comment-thread">
    <form class="add-comment-form" @submit.prevent="addComment">
      <textarea 
        ref="textareaRef"
        v-model="newCommentText" 
        placeholder="記事にコメントを追加..." 
        rows="1"
        @input="adjustHeight"
      />
      <button type="submit" :disabled="!newCommentText.trim()">コメント</button>
    </form>
    <div class="comment-list">
      <Comment
        v-for="comment in comments"
        :key="comment.id"
        :comment="comment"
        :level="0"
        :contentType="contentType"
        @reply="handleReply"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, nextTick } from 'vue';
import Comment from './Comment.vue';
import { fetchComments, postComment, type CommentResponse } from '@/api/comments';
import { fetchQuestionComments, postQuestionComment, type QuestionCommentResponse } from '@/api/questionComments';

// 共通のコメント型
interface ThreadComment {
  id: string;
  user_id: string;
  parent_id: string | null;
  body: string;
  created_at: string;
  user_name?: string | null;
  replies: ThreadComment[];
}

const props = withDefaults(defineProps<{
  contentId: string;
  contentType?: 'article' | 'question';
}>(), {
  contentType: 'article',
});

const comments = ref<ThreadComment[]>([]);
const newCommentText = ref('');
const loading = ref(false);
const textareaRef = ref<HTMLTextAreaElement | null>(null);

// ⭐ テキストエリアの高さを文字量・改行に合わせて自動調節するロジック
const adjustHeight = () => {
  const textarea = textareaRef.value;
  if (!textarea) return;
  
  // 一度高さをリセットして正しい scrollHeight を取得できるようにする
  textarea.style.height = 'auto';
  // 内包するコンテンツの高さに合わせて拡張 (上下のpadding分などを考慮)
  textarea.style.height = `${textarea.scrollHeight}px`;
};

// コメント送信後にテキストエリアが綺麗に1行に戻るように watch
watch(newCommentText, (newVal) => {
  if (newVal === '') {
    nextTick(() => {
      if (textareaRef.value) textareaRef.value.style.height = 'auto';
    });
  }
});

const loadComments = async () => {
  if (!props.contentId) return;
  loading.value = true;
  try {
    let rawComments: (CommentResponse | QuestionCommentResponse)[];
    if (props.contentType === 'question') {
      rawComments = await fetchQuestionComments(props.contentId);
    } else {
      rawComments = await fetchComments(props.contentId);
    }
    comments.value = buildTree(rawComments);
  } catch (error) {
    console.error('Failed to load comments:', error);
  } finally {
    loading.value = false;
  }
};

const buildTree = (flatComments: any[]): ThreadComment[] => {
  const map = new Map<string, ThreadComment>();
  const roots: ThreadComment[] = [];

  flatComments.forEach(c => {
    map.set(c.id, { ...c, replies: [] });
  });

  map.forEach(c => {
    if (c.parent_id && map.has(c.parent_id)) {
      map.get(c.parent_id)!.replies.push(c);
    } else {
      roots.push(c);
    }
  });

  return roots;
};

onMounted(loadComments);

// contentId が変わったら再読み込み
watch(() => props.contentId, loadComments);

async function addComment() {
  if (!newCommentText.value.trim() || !props.contentId) return;
  try {
    if (props.contentType === 'question') {
      await postQuestionComment(props.contentId, { body: newCommentText.value });
    } else {
      await postComment(props.contentId, { body: newCommentText.value });
    }
    newCommentText.value = '';
    await loadComments();
  } catch (error) {
    console.error('Failed to post comment:', error);
    alert('コメントの投稿に失敗しました。');
  }
}

async function handleReply(parentId: string, text: string) {
  if (!text.trim() || !props.contentId) return;
  try {
    if (props.contentType === 'question') {
      await postQuestionComment(props.contentId, { parent_id: parentId, body: text });
    } else {
      await postComment(props.contentId, { parent_id: parentId, body: text });
    }
    await loadComments();
  } catch (error) {
    console.error('Failed to post reply:', error);
    alert('返信の投稿に失敗しました。');
  }
}
</script>

<style scoped>
.comment-thread {
  margin-top: 0;
  padding: 0 0 40px 0;
}
.add-comment-form {
  display: flex;
  gap: 10px;
  margin-bottom: 20px; /* 少し縮小 */
  align-items: flex-end; /* 下揃えにすることでテキストが伸びてもボタンが下に綺麗に配置されます */
}
.add-comment-form textarea {
  flex: 1;
  border-radius: 6px;
  border: 1px solid #ccc;
  padding: 10px;
  font-size: 15px;
  resize: none; /* ⭐ 手動可変を完全に禁止 */
  min-height: 40px; /* 初期状態の1行分の高さ */
  line-height: 1.4;
  box-sizing: border-box;
}
.add-comment-form button {
  background: #2693B4;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 10px 18px; /* 高さを少し調整 */
  font-size: 15px;
  cursor: pointer;
  min-width: 90px; /* ⭐ コメント送信ボタンの幅を確保 */
  height: 40px; /* 1行目の高さに揃える */
  transition: 0.2s;
}
.add-comment-form button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

/* ⭐ コメントとコメントの間の隙間を制御するスタイル */
.comment-list :deep(.comment) {
  margin-bottom: 8px !important; /* コメント同士の間隔を少し狭く設定 */
}

/* ⭐ 子の Comment.vue 側にある「返信ボタン」「キャンセルボタン」の横幅を完全一致させるためのディープセレクタ設定 */
.comment-list :deep(.send-btn),
.comment-list :deep(.cancel-btn),
.comment-list :deep(.reply-box button) {
  min-width: 90px !important;    /* 完全に幅を統一 */
  text-align: center;
  padding: 6px 12px !important;   /* 内側の余白を統一 */
  box-sizing: border-box;
}
</style>