<template>
  <div class="comment-thread">
    <form class="add-comment-form" @submit.prevent="addComment">
      <textarea v-model="newCommentText" placeholder="コメントを追加..." rows="2" />
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
import { ref, onMounted, watch } from 'vue';
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
