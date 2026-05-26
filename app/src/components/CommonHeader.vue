<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

// -------------------------------------------------------
// 投稿ボタンがクリックされたときの処理0507
const handlePostClick = () => {
    router.push('/post'); // 投稿画面のパスを指定
};

const searchQuery = ref('');

// 検索実行ロジック
const executeSearch = () => {
    const keyword = searchQuery.value.trim();
    if (!keyword) {
        // 空欄で検索した場合はクエリをクリアしてHomeへ遷移（全記事表示）
        router.push({ name: 'Home' });
        return;
    }
    // URLを /?q=キーワード に書き換えて移動する
    router.push({ name: 'Home', query: { q: keyword } });
};
// -------------------------------------------------------

// ----- プロフィール編集とログアウトの関数を追加0508 --------
// const goToEdit = () => {
//     console.log("編集画面へ移動");
//     router.push('/profile/edit');
// };

// プロフィール編集からプロフィールを表示に変更0515
// --- プロフィールを表示0515 ---
const goToProfile = () => {
    console.log("プロフィール画面へ強制移動（リロード）");
    window.location.href = '/profile'; // ブラウザの機能でページを読み込み直す0522
};
// ----------------------------------------------------
const handleLogout = () => {
    console.log("ログアウト処理実行");
    localStorage.removeItem('token');
    alert("ログアウトしました");
    router.push('/login'); // ログイン画面へ飛ばす
};
// ----------------------------------------------------

</script>
<template>
    <div class="article-header-wrapper">
        <header class="site-header">
            <div class="header-container">
                
                <router-link to="/" class="header-logo-group">
                <!-- <a href="/" class="header-logo-group"> -->
                    <img src="@/assets/logo.png" alt="学校ロゴ" class="header-logo">
                    <p class="site-sub-title">プログラミング情報共有サイト</p>
                <!-- </a> -->
                </router-link>

                <div class="header-right-group">
                    <div class="search-bar">
                        <input 
                            v-model="searchQuery"
                            type="text" 
                            placeholder="キーワードから記事を探す..."
                            @keydown.enter="executeSearch"
                        >
                        <button class="search-button" @click="executeSearch">検索</button>
                    </div>
                    <button class="post-button" @click="handlePostClick">+ 投稿する</button>

                    <!-- プロフィール表示ボタン -->
                    <button class="profile-button" @click="goToProfile">
                        <div class="color-avatar">
                            <span>👤</span>
                        </div>
                        <span class="button-text">プロフィール</span>
                    </button>
                    <!-- ログアウトボタン -->
                    <button class="logout-button" @click="handleLogout">
                        ログアウト
                    </button>
                </div>

            </div>
        </header>
    </div>
</template>

<script>

</script>

<style scoped>
.article-header-wrapper {
    width: 100%;
    position: sticky;
    top: 0;
    z-index: 100;
    border-bottom: 1px solid #ddd;
}

.site-header {
    background-color: #fff;
}

.header-container {
    display: flex;
    align-items: center;
    padding: 10px 30px;
    background-color: #fff;
}

/* ロゴとテキストの縦並び・中央揃え */
.header-logo-group {
    display: flex;
    flex-direction: column;
    align-items: center;
    flex-shrink: 0;
    text-decoration: none;
    color: inherit;
    cursor: pointer;
}

.header-logo {
    height: 40px;
    width: auto;
    margin-bottom: 2px;
}

.site-sub-title {
    margin: 0;
    font-size: 10px;
    color: #333;
    transform: scale(0.8);
}

/* 右側グループを右に押し出す */
.header-right-group {
    display: flex;
    align-items: center;
    gap: 20px;
    margin-left: auto;
    flex-grow: 0.6;
    justify-content: flex-end;
}

.search-bar {
    flex: 1;
    max-width: 600px;
    margin: 0 30px;
    display: flex;
    border: 2px solid #2693B4;
    border-radius: 4px;
    overflow: hidden;
}

.search-bar input {
    flex: 1;
    border: none;
    padding: 10px;
    outline: none;
    font-size: 14px;
}

.search-button {
    background-color: #2693B4;
    color: white;
    border: none;
    padding: 0 30px 0 30px;
    cursor: pointer;
    font-size: 14px;
    font-weight: bold;
    display: flex;
    align-items: center;
    gap: 4px;
    transition: ease 0.3s;
}
.search-button:hover {
    background-color: #1b6a8c;
}

.post-button {
    background-color: #ff6b6b;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 6px;
    font-weight: bold;
    white-space: nowrap;
    cursor: pointer;
    transition: background-color 0.3s;
}

.post-button:hover {
    background-color: #2693B4;
}

/* --------------ログアウトなどのユーザメニュー 0508（イメージなし）----------------*/
.user-menu-container {
    position: relative; /* メニューの基準点にする */
    cursor: pointer;
    padding: 10px;
}

/* アイコンを包む枠の設定（サイズを固定する） */
.profile-icon {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    overflow: hidden; /* はみ出た部分を隠す（正円） */
    display: flex;
    align-items: center;
    justify-content: center;
    /* border: 2px solid #fff; */
}

/* 画像が有効になった時の設定 */
.profile-icon img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

/* 今使っている色付きの丸（イメージなし）デモ用 */
.color-avatar {
    width: 100%;
    height: 100%;
    background-color: #2693B4; /* 色付きアイコン */
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 18px;
    user-select: none; /* 文字を選択不可にする */
}

/* プロフィール表示ボタン */
.profile-button {
    display: flex;
    align-items: center;
    gap: 8px;
    background-color: #2693B4;
    color: white;
    border: none;
    padding: 8px 12px;
    border-radius: 20px;
    cursor: pointer;
    font-weight: bold;
    font-size: 14px;
    transition: all 0.3s ease;
}

.profile-button:hover {
    background-color: #1b6a8c;
    transform: translateY(-2px);
}

.profile-button .color-avatar {
    width: 28px;
    height: 28px;
    background-color: rgba(255,255,255,0.3);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
}

.profile-button .button-text {
    font-size: 14px;
}

/* ログアウトボタン */
.logout-button {
    background-color: #f44336;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 20px;
    cursor: pointer;
    font-weight: bold;
    font-size: 14px;
    transition: all 0.3s ease;
}

.logout-button:hover {
    background-color: #da190b;
    transform: translateY(-2px);
}
/* -------------------------------------------------------- */
/* レスポンシブ緊急（すべてimportantついてます） */
 /* スプリット画面を想定した幅 */
@media (max-width: 1024px) {
    .search-bar {
        flex: 1 !important;     /* 1を指定すると、余っている余白をすべて吸い取って伸びる */
        max-width: 600px !important;
        margin-right: 20px !important; 
    }

    .header-container {
        justify-content: space-between !important; /* 両端に広げる */
    }
}
@media (max-width: 768px) {
    * {
        max-width: 100vw !important;
        box-sizing: border-box !important;
        /* overflow: hidden !important; */
    }
    .header-container {
        height: 80px !important; /* ヘッダーの高さを固定して小さくする */
        padding: 0 15px !important; /* 左右に余白をつけました */
        gap: 4px !important; /* 要素間の隙間をほぼゼロに */
    }

    .header-logo-group {
        width: 10% !important; /* ロゴグループ全体も小さく */
    }
    .site-sub-title {
        display: none !important; /* サブタイトルはスマホでは非表示にする */
    }
    .header-logo {
        width: 100% !important; /* ロゴをアイコンサイズまで小さく */
    }

    .search-button {
        /* 元の「検索」という文字を透明にして見えなくする */
        color: transparent !important;

        width: 40px !important;
        min-width: 40px !important;
        height: 40px !important;
        padding: 0 !important;
        
        /* 虫眼鏡アイコンを背景として表示する */
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='white'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z'/%3E%3C/svg%3E") !important;
        background-repeat: no-repeat !important;
        background-position: center !important;
        background-size: 15px !important; /* アイコンの大きさ */
        background-color: #2693B4 !important; 
    }
    /* バー本体 */
    .search-bar {
        flex: 1 !important;
        min-width: 0 !important;
        margin-right: 5px !important;
        margin-left: 10px !important;
    }
    .search-bar input {
        padding: 6px !important; /* 中の余白も削る */
        font-size: 14px !important;
    }
    .header-right-group {
        display: flex !important;
        align-items: center !important;
        gap: 12px !important;
        margin-left: 0 !important;
    }
    .post-button {
        min-width: 40px !important;
        padding: 8px !important;
    }

    /* プロフィールボタン：レスポンシブ対応 */
    .profile-button {
        padding: 6px 10px !important;
        font-size: 12px !important;
        gap: 4px !important;
    }

    .profile-button .button-text {
        display: none !important;
    }

    .logout-button {
        padding: 6px 10px !important;
        font-size: 12px !important;
    }

}
</style>
