<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import CommonHeader from '@/components/CommonHeader.vue';

// script setup 内に追加
const currentTab = ref('記事'); // 最初は「記事」を選択状態にする

const user = ref({
    name: '1350132',
    bio: '佐藤先生のクラスでネットワークを学んでいます。コンテナ技術を用いた環境の構築をしています。テストとか資格の対策の記事を書いていきます。'
    // bio: '' // 自己紹介が未登録の状態を試すときは、ここを空文字にしてください。
});

// データの形（型）を定義
interface ContentItem {
    id: number;
    title: string;
}

// --------------------------
// 各タブ用のデータ。[] の中にデータがあれば表示、なければ「なし」が出ます。
const articles = ref<ContentItem[]>([
    { id: 1, title: 'ESP32でLEDを光らせてみる。2年後期と3年前期向け。ESP32キットを持っている学生向け' },
    { id: 2, title: 'ゾンビ化したKubernetesを殺す' },
    { id: 3, title: '【2024年版】これだけやっとけ！基本情報技術者試験対策' },
    { id: 4, title: '【2024年版】これだけやっとけ！応用情報技術者試験対策' },
    { id: 5, title: '【2024年版】これだけやっとけ！AWS認定ソリューションアーキテクト試験対策' },
]);

// const questions = ref<ContentItem[]>([
//     { id: 1, title: 'Vue.jsのタブ切り替えがうまくいきません' } 
// ]);

const likes = ref<ContentItem[]>([
    { id: 1, title: '2年生Linuxのテスト過去問こんな感じ' }
]);

// データが入っていない状態を試すときは、上のように[]にしてみてください。
// const articles = ref<any[]>([]);
    const questions = ref<any[]>([]);
// const likes = ref<any[]>([]);
// --------------------------
</script>

<template>
    <CommonHeader />
    <div class="profile-page-wrapper">
        <main class="profile-container">
    
            <div class="main-content">
                <div class="user-header">
                    <h1><strong>{{ user.name }}</strong> さんのプロフィール</h1>
                    <button class="btn-edit-profile">プロフィールを編集</button>
                </div>

                <div class="card bio-card">
                    <p class="bio-label">自己紹介</p>
                    <p class="bio-text">{{ user.bio ? user.bio : '自己紹介はまだ登録されていません。' }}</p>
                </div>

                <nav class="profile-tabs"> 
                    <button 
                        class="tab-item" 
                        :class="{ active: currentTab === '記事' }" 
                        @click="currentTab = '記事'"
                    >
                    記事
                    </button>
                    <button 
                        class="tab-item" 
                        :class="{ active: currentTab === '質問' }" 
                        @click="currentTab = '質問'"
                    >
                    質問
                    </button>
                    <button 
                        class="tab-item" 
                        :class="{ active: currentTab === 'いいね' }" 
                        @click="currentTab = 'いいね'"
                    >
                    いいね
                    </button>
                </nav>

                <div class="tab-content">
                    <div v-if="currentTab === '記事'">
                        <ul v-if="articles.length > 0" class="article-list">
                            <li v-for="item in articles" :key="item.id" class="article-item">
                                <span class="article-title">{{ item.title }}</span>
                                <button class="btn-article-edit">編集</button>
                            </li>
                        </ul>
                        <p v-else class="empty-message">投稿した記事はありません。</p>
                    </div>

                    <div v-else-if="currentTab === '質問'">
                        <ul v-if="questions.length > 0" class="article-list">
                            <li v-for="item in questions" :key="item.id" class="article-item">
                                <span class="article-title">{{ item.title }}</span>
                                <button class="btn-article-edit">編集</button> </li>
                            </ul>
                        <p v-else class="empty-message">質問はまだありません。</p>
                    </div>

                    <div v-else-if="currentTab === 'いいね'">
                        <ul v-if="likes.length > 0" class="article-list">
                            <li v-for="item in likes" :key="item.id" class="article-item">
                                <span class="article-title">{{ item.title }}</span>
                            </li>
                        </ul>
                        <p v-else class="empty-message">いいねした記事はありません。</p>
                    </div>
                </div>
            </div>
        
            <!-- サイドバーPW変更等 -->
            <aside class="sidebar">
                <div class="sticky-container">
                <div class="card action-card">
                    <span>パスワード変更</span>
                    <button class="btn-action-red">変更</button>
                </div>

                <div class="card action-card">
                    <span>退会する</span>
                    <button class="btn-action-red">退会する</button>
                </div>
                </div>
            </aside>

        </main>
    </div>
</template>

<style scoped>
/* --- プロフィールページ全体 --- */
.profile-page-wrapper {
    background-color: #f0f2f5;
    min-height: 100vh;
    font-family: sans-serif;
    color: #333;
}
/* ---  メインレイアウト --- */
.profile-container {
    display: flex;
    justify-content: center;
    max-width: 1200px;
    margin: 0 auto;
    gap: 50px;
    padding: 40px 100px;
    align-items: flex-start;
    gap: 100px; /* メイン（記事）とサイド（パスワード）の間のスペース */
}
.main-content {
    min-width: 0; /* Flexの子要素がはみ出さないようにするための魔法の1行 */
    flex: 1;
    display: flex;
    flex-direction: column; 
}

/* --- ヘッダー --- */
/* ユーザネームさんのプロフィール */
.user-header h1 {
    font-size: 26px;
    margin-bottom: 12px;
}
.user-header h1 strong {
    color: #3c3c3c;
    font-weight: bold;
}
/* --- プロフィール編集ボタン --- */
.btn-edit-profile {
    font-weight: bold;
    background: #f0f2f5;
    border: 3px solid #2693B4;
    border-radius: 20px;
    padding: 6px 24px;
    color: #2693B4;
    cursor: pointer;
    margin-bottom: 30px;
    margin-top: 10px;
    transition: ease-out 0.3s;
}
.btn-edit-profile:hover {
    background-color: #2693B4;
    color: white;
}

/* --- カード共通 --- */
.card {
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.06); /* Figma風の柔らかい影 */
    padding: 24px;
    margin-bottom: 24px;
}

/* --- 自己紹介 --- */
/* .bio-card {
  max-width: 500px; /* 自己紹介カードの横幅 */
.bio-label { 
    font-weight: bold;
    margin-bottom: 8px;
    font-size: 14px;
}
.bio-text { 
    font-size: 14px;
    line-height: 1.6;
    color: #555; 
}

/* --- タブ部分（記事、質問、いいね） --- */
/* タブ全体のコンテナ */
.profile-tabs {
    display: flex;
    gap: 0; /* ボタン同士をくっつける */
    margin: 30px 0 0; /* 下線とくっつけるために下マージンは0 */
    border-bottom: 2px solid #2693B4;
}
/* --- タブのボタン自体の見た目 --- */
.tab-item {
    background: none;
    border: none;
    padding: 10px 30px;
    font-size: 16px;
    color: #666;
    cursor: pointer;
    outline: none;
    margin-bottom: -2px; 
}
/* --- 選択された時の見た目 --- */
.tab-item.active {
    background-color: #2693B4; /* Figmaの青 */
    color: white !important;
    border-radius: 10px 10px 0 0; /* 上だけ丸く */
}

/* ---  記事リスト --- */
.tab-content {
    width: 100%;
}

.article-list {
    list-style: none;
    padding: 0;
    margin: 0;
}

.article-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 18px 20px;
    border-bottom: 1px solid #eee;
    width: 100%;
    box-sizing: border-box; 
    gap: 15px; /* タイトルと編集ボタンの間のスペース */
}
.article-title {
  /* 固定（70%）ではなく、最大（70%）にする */
    flex: 1; /* 余っているスペースを埋める */
    max-width: 70%; 
    
    /* 三点リーダー設定はそのまま */
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    
    /* 左揃えを確実にする */
    text-align: left;
}
/* 記事編集ボタン */
.btn-article-edit {
    /* ボタンが潰れないように、幅を固定 */
    flex: 0 0 80px; 
    text-align: center;
    border: 3px solid #2693B4;
    background: #f0f2f5;
    color: #2693B4;
    border-radius: 20px;
    padding: 5px 20px;
    cursor: pointer;
    font-weight: bold;
    transition: ease-out 0.3s;
}
.btn-article-edit:hover {
    background-color: #2693B4;
    color: white;
}
/* ----------------------- */
/* --- データなし表示 --- */
.empty-message {
    padding: 60px;
    text-align: center;
    color: #999;
    margin-top: 20px;
}

/* 右のサイドバー */
.sidebar {
    width: 320px;
    margin-top: 130px; /* 微調整の集大成 さわるな */
}
/* パスワード変更・退会 */
.sticky-container {
    top: 200px; 
    display: flex;
    flex-direction: column;
    gap: 20px; /* カード同士の隙間 */
}

.action-card {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.btn-action-red {
    border: 3px solid #b42626;
    background: white;
    color: #b42626;
    border-radius: 20px;
    padding: 6px 30px;
    cursor: pointer;
    font-weight: bold;
    transition: ease-out 0.3s;
}
.btn-action-red:hover {
    background-color: #b42626;
    color: white;
}
/* 画面幅が 768px 以下（タブレットやスマホ）になったら適用 */
@media (max-width: 768px) {
    .profile-container {
        flex-direction: column; /* 「左と右」を「上と下」に並び替える */
        align-items: stretch;   /* 横幅いっぱいまで広げる */
        padding: 20px 50px; 
    }

    .main-content {
        width: 100%; /* メインエリアを全幅にする */
    }

    /* パスワード変更などのサイドバーも全幅にして下に並べる */
    .sidebar {
        width: 100%;
        display: flex;
        flex-direction: column;
        gap: 20px;
        margin: 0; /* 上のマージンは消す */
    }
}
</style>