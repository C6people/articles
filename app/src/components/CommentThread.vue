<template>
  <div class="comment-thread">
    <form class="add-comment-form" @submit.prevent="addComment">
      <textarea v-model="newCommentText" placeholder="記事にコメントを追加..." rows="2" />
      <button type="submit" :disabled="!newCommentText.trim()">コメント</button>
    </form>
    <div class="comment-list">
      <div v-if="comments.length === 0" class="no-comments">まだコメントがありません。</div>

      <Comment
        v-else
        v-for="comment in comments"
        :key="comment.id"
        :comment="comment"
        :level="0"
        @reply="handleReply"
        @delete="handleDelete"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import Comment from './Comment.vue';

interface CommentType {
  id: number;
  user: string;
  text: string;
  created_at: string;
  replies: CommentType[];
}

const props = defineProps<{ articleId: string }>();

const comments = ref<CommentType[]>([]);
const newCommentText = ref('');
let nextId = Date.now();

const getStorageKey = () => `article_comments_${props.articleId}`;

const saveComments = () => {
  try {
    localStorage.setItem(getStorageKey(), JSON.stringify(comments.value));
  } catch (err) {
    console.error('コメント保存エラー:', err);
  }
};

const loadComments = () => {
  if (!props.articleId) {
    comments.value = [];
    return;
  }

  const stored = localStorage.getItem(getStorageKey());
  if (stored) {
    try {
      const parsed = JSON.parse(stored);
      comments.value = Array.isArray(parsed) ? parsed : [];
    } catch (err) {
      console.error('コメント読み込みエラー:', err);
      comments.value = [];
    }
  } else {
    comments.value = [];
  }

  const findMaxId = (list: CommentType[]): number =>
    list.reduce((max, item) => Math.max(max, item.id, findMaxId(item.replies)), 0);

  const maxId = findMaxId(comments.value);
  nextId = Math.max(nextId, maxId + 1);
};

onMounted(loadComments);

function addComment() {
  if (!newCommentText.value.trim()) return;

  comments.value.push({
    id: nextId++,
    user: 'ゲスト',
    text: newCommentText.value.trim(),
    created_at: new Date().toLocaleString('ja-JP', { hour12: false }),
    replies: []
  });
  newCommentText.value = '';
  saveComments();
}

function handleReply(parentId: number, text: string) {
  function addReply(list: CommentType[]): boolean {
    for (const c of list) {
      if (c.id === parentId) {
        c.replies.push({
          id: nextId++,
          user: 'ゲスト',
          text: text.trim(),
          created_at: new Date().toLocaleString('ja-JP', { hour12: false }),
          replies: []
        });
        return true;
      }
      if (addReply(c.replies)) return true;
    }
    return false;
  }

  if (addReply(comments.value)) {
    saveComments();
  }
}

function handleDelete(commentId: number) {
  function deleteComment(list: CommentType[]): boolean {
    const index = list.findIndex((item) => item.id === commentId);
    if (index !== -1) {
      list.splice(index, 1);
      return true;
    }
    for (const item of list) {
      if (deleteComment(item.replies)) {
        return true;
      }
    }
    return false;
  }

  if (deleteComment(comments.value)) {
    saveComments();
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
  margin-bottom: 24px;
  align-items: flex-start;
}
.add-comment-form textarea {
  flex: 1;
  border-radius: 6px;
  border: 1px solid #ccc;
  padding: 8px;
  font-size: 15px;
  resize: vertical;
}
.add-comment-form button {
  background: #2693B4;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 8px 18px;
  font-size: 15px;
  cursor: pointer;
  min-width: 80px;
  transition: 0.2s;
}
.add-comment-form button:disabled {
  background: #ccc;
  cursor: not-allowed;
}
.comment-list {
  margin-top: 0;
}
</style>
