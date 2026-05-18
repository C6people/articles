<template>
  <div :class="['comment', `level-${level}`]">
    <div class="comment-connector" v-if="level > 0">
      <div class="vertical-line"></div>
    </div>
    <div class="comment-main">
      <div class="comment-header">
        <span class="comment-user">{{ comment.user_id }}</span>
        <span class="comment-date">{{ comment.created_at }}</span>
      </div>
      <div class="comment-body">{{ comment.body }}</div>
      <div class="comment-actions">
        <button class="reply-btn" @click="toggleReply">返信</button>
        <button v-if="comment.replies.length" class="toggle-btn" @click="toggleCollapse">
          {{ collapsed ? '返信を表示' : '返信を隠す' }} ({{ comment.replies.length }})
        </button>
      </div>
    </div>
    <div v-if="showReplyBox" class="reply-box">
      <textarea v-model="replyText" placeholder="返信を入力..." rows="2"></textarea>
      <button class="send-btn" @click="sendReply">送信</button>
      <button class="cancel-btn" @click="toggleReply">キャンセル</button>
    </div>
    <transition name="fade">
      <div class="replies" v-show="!collapsed">
        <Comment
          v-for="reply in comment.replies"
          :key="reply.id"
          :comment="reply"
          :level="level + 1"
          @reply="(parentId: string, text: string) => $emit('reply', parentId, text)"
        />
      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">

import { ref } from 'vue';

// ThreadCommentの構造に合わせた型定義
export interface CommentType {
  id: string;
  article_id: string;
  user_id: string;
  parent_id: string | null;
  body: string;
  created_at: string;
  user_name?: string;
  replies: CommentType[];
}

// 2. props（親から受け取るデータ）に型を設定
// これにより、テンプレートの comment.user が「確実に存在する」と認識されます
const props = withDefaults(defineProps<{
  comment: CommentType;
  level?: number;
}>(), {
  level: 0  // もし指定がなければ 0 を代入する
});

const emit = defineEmits(['reply']);
const showReplyBox = ref(false);
const replyText = ref('');
const collapsed = ref(true);

function toggleReply() {
  showReplyBox.value = !showReplyBox.value;
  if (!showReplyBox.value) replyText.value = '';
}

function sendReply() {
  // props.comment.id と書いたときにエラーが出なくなります
  if (replyText.value.trim() && props.comment) {
    emit('reply', props.comment.id, replyText.value);
    replyText.value = '';
    showReplyBox.value = false;
    collapsed.value = false;
  }
}

function toggleCollapse() {
  collapsed.value = !collapsed.value;
}
</script>

<style scoped>
/* 階層インデント */
.comment {
  margin-top: 24px;
  position: relative;
  padding-left: 0;
}
.level-1 {
  padding-left: 32px;
}
.level-2 {
  padding-left: 64px;
}
.level-3 {
  padding-left: 96px;
}
.comment-connector {
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 24px;
  display: flex;
  align-items: flex-start;
  z-index: 0;
}
.vertical-line {
  width: 2px;
  background: #d0d7de;
  height: 100%;
  margin-left: 12px;
  border-radius: 2px;
}
.comment-main {
  background: #fff;
  border-radius: 6px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.5);
  padding: 16px 20px 10px 20px;
  margin-bottom: 4px;
  position: relative;
  z-index: 1;
}
.comment-header {
  font-size: 13px;
  color: #888;
  margin-bottom: 6px;
}
.comment-user {
  font-weight: bold;
  color: #2693B4;
  margin-right: 10px;
}
.comment-date {
  color: #aaa;
}
.comment-body {
  font-size: 15px;
  color: #333;
  margin-bottom: 8px;
}
.comment-actions {
  display: flex;
  gap: 10px;
  margin-top: 2px;
}
.reply-btn {
  font-size: 13px;
  color: #2693B4;
  background: none;
  border: none;
  cursor: pointer;
  margin-left: -8px;
  margin-bottom: 2px;
}
.reply-btn:hover {
  text-decoration: underline;
}
.toggle-btn {
  font-size: 13px;
  color: #888;
  background: none;
  border: none;
  cursor: pointer;
  text-decoration: underline;
}
.reply-box {
  margin: 10px 0 0 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.reply-box textarea {
  width: 100%;
  border-radius: 4px;
  border: 1px solid #ccc;
  padding: 6px;
  font-size: 14px;
  resize: vertical;
}
.send-btn {
  background: #2693B4;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 4px 16px;
  font-size: 13px;
  cursor: pointer;
  margin-right: 8px;
}
.cancel-btn {
  background: none;
  color: #888;
  border: none;
  font-size: 13px;
  cursor: pointer;
}
.replies {
  margin-top: 0;
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
