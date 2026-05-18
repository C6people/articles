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
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import Comment from './Comment.vue';
import { fetchComments, postComment, type CommentResponse } from '@/api/comments';

interface ThreadComment extends CommentResponse {
  replies: ThreadComment[];
}

const route = useRoute();
const comments = ref<ThreadComment[]>([]);
const newCommentText = ref('');
const loading = ref(false);

const articleId = route.params.id as string;

const loadComments = async () => {
  if (!articleId) return;
  loading.value = true;
  try {
    const rawComments = await fetchComments(articleId);
    comments.value = buildTree(rawComments);
  } catch (error) {
    console.error('Failed to load comments:', error);
  } finally {
    loading.value = false;
  }
};

const buildTree = (flatComments: CommentResponse[]): ThreadComment[] => {
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

async function addComment() {
  if (!newCommentText.value.trim() || !articleId) return;
  try {
    await postComment(articleId, { body: newCommentText.value });
    newCommentText.value = '';
    await loadComments();
  } catch (error) {
    console.error('Failed to post comment:', error);
    alert('コメントの投稿に失敗しました。');
  }
}

async function handleReply(parentId: string, text: string) {
  if (!text.trim() || !articleId) return;
  try {
    await postComment(articleId, {
      parent_id: parentId,
      body: text
    });
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
