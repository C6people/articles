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
        @reply="handleReply"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, nextTick } from 'vue';
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
const textareaRef = ref<HTMLTextAreaElement | null>(null);

const articleId = route.params.id as string;

// 高さを自動調節するロジック（CSSの max-height を超えると自動的に頭打ちになります）
const adjustHeight = () => {
  const textarea = textareaRef.value;
  if (!textarea) return;
  
  textarea.style.height = 'auto';
  textarea.style.height = `${textarea.scrollHeight}px`;
};

watch(newCommentText, (newVal) => {
  if (newVal === '') {
    nextTick(() => {
      if (textareaRef.value) textareaRef.value.style.height = 'auto';
    });
  }
});

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
  margin-bottom: 20px;
  align-items: flex-start; 
}
.add-comment-form textarea {
  flex: 1;
  border-radius: 6px;
  border: 1px solid #ccc;
  padding: 10px;
  font-size: 15px;
  resize: none; 
  min-height: 40px; 
  max-height: 120px; 
  overflow-y: auto; 
  line-height: 1.4;
  box-sizing: border-box;
}
.add-comment-form button {
  background: #2693B4;
  color: #fff;
  border: none;
  border-radius: 6px;
  padding: 10px 18px; 
  font-size: 15px;
  cursor: pointer;
  min-width: 90px; 
  height: 40px; /* 1行目の高さにジャストフィット */
  transition: 0.2s;
}
.add-comment-form button:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.comment-list :deep(.comment) {
  margin-bottom: 8px !important; 
}

.comment-list :deep(.send-btn),
.comment-list :deep(.cancel-btn),
.comment-list :deep(.reply-box button) {
  min-width: 90px !important;    
  text-align: center;
  padding: 6px 12px !important;   
  box-sizing: border-box;
}
</style>