<template>
  <div class="comment-wrapper">
    <div class="comment" :style="{ marginLeft: level > 0 ? '24px' : '0' }">
      
      <div v-if="level > 0" class="comment-connector">
        <div class="vertical-line"></div>
      </div>

      <div class="comment-main">
        <div class="comment-header">
          <span class="comment-user">{{ comment.user_name ?? '名無しさん' }}</span>
          <span class="comment-date">{{ formattedDate }}</span>
        </div>
        <div class="comment-body">{{ comment.body }}</div>
        <div class="comment-actions">
          <button class="reply-btn" @click="toggleReply">返信</button>
          <button v-if="comment.replies?.length" class="toggle-btn" @click="toggleCollapse">
            {{ collapsed ? '返信を表示' : '返信を隠す' }} ({{ comment.replies.length }})
          </button>
        </div>
      </div>

      <div v-if="showReplyBox" class="reply-box">
        <textarea 
          ref="replyTextarea"
          v-model="replyText" 
          placeholder="返信を入力..." 
          rows="1" 
          @input="autoResize"
        />
        <div class="reply-box-actions">
          <button class="send-btn" @click="sendReply">送信</button>
          <button class="cancel-btn" @click="toggleReply">キャンセル</button>
        </div>
      </div>

      <transition name="fade">
        <div class="replies" v-show="!collapsed">
          <Comment
            v-for="reply in comment.replies"
            :key="reply.id"
            :comment="reply"
            :level="level + 1"
            @reply="(parentId, text) => $emit('reply', parentId, text)"
          />
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, nextTick } from 'vue';

// --- 型定義 (Types) ---
export interface CommentType {
  id: string;
  article_id: string;
  user_id: string;
  user_name: string | null;
  parent_id: string | null;
  body: string;
  created_at: string;
  replies: CommentType[];
}

// --- Props & Emits ---
const props = withDefaults(defineProps<{
  comment: CommentType;
  level?: number;
}>(), {
  level: 0
});

const emit = defineEmits<{
  (e: 'reply', parentId: string, text: string): void;
}>();

// --- 状態定義 (Refs) ---
const showReplyBox = ref(false);
const replyText = ref('');
const collapsed = ref(true);
const replyTextarea = ref<HTMLTextAreaElement | null>(null);

// --- 計算プロパティ (Computed) ---
const formattedDate = computed(() => {
  if (!props.comment.created_at) return '';
  const date = new Date(props.comment.created_at);
  
  // 既存のタイムゾーン計算をきれいに整理
  const jst = new Date(date.getTime() + 9 * 60 * 60 * 1000);
  const yyyy = jst.getFullYear();
  const mm = String(jst.getMonth() + 1).padStart(2, '0');
  const dd = String(jst.getDate()).padStart(2, '0');
  const hh = String(jst.getHours()).padStart(2, '0');
  const min = String(jst.getMinutes()).padStart(2, '0');
  
  return `${yyyy}-${mm}-${dd} ${hh}:${min}`;
});

// --- ロジック関数 (Functions) ---
function autoResize() {
  nextTick(() => {
    const textarea = replyTextarea.value;
    if (textarea) {
      textarea.style.height = 'auto';
      // ⭐ CSSの max-height (120px) を超えないように最小値をとる
      const nextHeight = Math.min(textarea.scrollHeight, 120);
      textarea.style.height = `${nextHeight}px`;
    }
  });
}

function toggleReply() {
  showReplyBox.value = !showReplyBox.value;
  if (!showReplyBox.value) {
    replyText.value = '';
  }
  nextTick(() => {
    if (showReplyBox.value && replyTextarea.value) {
      replyTextarea.value.style.height = 'auto';
      replyTextarea.value.focus(); // 開いたときに自動フォーカス
    }
  });
}

function sendReply() {
  if (!replyText.value.trim()) return;
  
  emit('reply', props.comment.id, replyText.value);
  replyText.value = '';
  showReplyBox.value = false;
  collapsed.value = false;
  
  nextTick(() => {
    if (replyTextarea.value) replyTextarea.value.style.height = 'auto';
  });
}

function toggleCollapse() {
  collapsed.value = !collapsed.value;
}
</script>

<style scoped>
.comment-wrapper {
  position: relative;
}

.comment {
  margin-top: 12px;
  position: relative;
  transition: margin 0.2s ease;
}

.comment-connector {
  position: absolute;
  left: -12px;
  top: -12px; 
  bottom: 0;
  width: 2px;
  z-index: 0;
}

.vertical-line {
  width: 2px;
  background: #d0d7de;
  height: 100%;
}

.comment-main {
  background: #fff;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.35); 
  padding: 12px 16px 10px 16px;
  margin-bottom: 4px;
  position: relative;
  z-index: 1;
}

.comment-header {
  font-size: 13px;
  color: #888;
  margin-bottom: 4px;
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
  white-space: pre-wrap;
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
  padding: 0;
}

.reply-btn:hover, .toggle-btn:hover {
  text-decoration: underline;
}

.toggle-btn {
  font-size: 13px;
  color: #888;
  background: none;
  border: none;
  cursor: pointer;
}

.reply-box {
  margin: 8px 0 0 0;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.reply-box-actions {
  display: flex;
  gap: 8px;
}

.reply-box textarea {
  width: 100%;
  border-radius: 4px;
  border: 1px solid #ccc;
  padding: 8px;
  font-size: 14px;
  resize: none;
  max-height: 120px;
  overflow-y: auto;
  line-height: 1.4;
}

.send-btn {
  background: #2693B4;
  color: #fff;
  border: none;
  border-radius: 4px;
  padding: 6px 16px;
  font-size: 13px;
  cursor: pointer;
}

.cancel-btn {
  background: #ffffff;
  color: #666666;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 6px 16px;
  font-size: 13px;
  cursor: pointer;
}

.replies {
  margin-top: 4px;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>