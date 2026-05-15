<template>
  <div class="comment-thread">
    <form class="add-comment-form" @submit.prevent="addComment">
      <textarea v-model="newCommentText" placeholder="記事にコメントを追加..." rows="2" />
      <button type="submit" :disabled="!newCommentText.trim()">コメント</button>
    </form>
    <div class="comment-list">
      <Comment
        v-for="comment in comments"
        :key="comment.id"
        :comment="comment"
        :level="0"
        @reply="handleReply"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import Comment from './Comment.vue';

// モックデータ
const comments = ref([
  {
    id: 1,
    user: '田中太郎',
    text: 'とても参考になりました！',
    created_at: '2026-05-10 12:00',
    replies: [
      {
        id: 2,
        user: '管理人',
        text: 'コメントありがとうございます！',
        created_at: '2026-05-10 12:10',
        replies: [
          {
            id: 3,
            user: '田中太郎',
            text: 'また質問させてください！',
            created_at: '2026-05-10 12:15',
            replies: []
          }
        ]
      }
    ]
  },
  {
    id: 4,
    user: '山田花子',
    text: '記事の内容が分かりやすかったです。',
    created_at: '2026-05-11 09:30',
    replies: []
  }
]);

const newCommentText = ref('');
let nextId = 100;

function addComment() {
  if (!newCommentText.value.trim()) return;
  comments.value.push({
    id: nextId++,
    user: 'ゲスト',
    text: newCommentText.value,
    created_at: new Date().toLocaleString('ja-JP', { hour12: false }),
    replies: []
  });
  newCommentText.value = '';
}

function handleReply(parentId: number, text: string) {
  // 再帰的に親IDを探してrepliesにpush
  function addReply(list: any[]) {
    for (const c of list) {
      if (c.id === parentId) {
        c.replies.push({
          id: nextId++,
          user: 'ゲスト',
          text,
          created_at: new Date().toLocaleString('ja-JP', { hour12: false }),
          replies: []
        });
        return true;
      }
      if (addReply(c.replies)) return true;
    }
    return false;
  }
  addReply(comments.value);
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
  padding: 13px 18px;
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
