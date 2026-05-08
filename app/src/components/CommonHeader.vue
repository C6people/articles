<script setup lang="ts">
import { useRouter } from 'vue-router';

const router = useRouter();

// -------------------------------------------------------
// 投稿ボタンがクリックされたときの処理0507
const handlePostClick = () => {
    router.push('/post'); // 投稿画面のパスを指定
};

// 検索入力用の関数を追加（eventが暗黙的にanyみたいなエラーを消すためのもの）0507
// event の型を明示的に指定
const handleSearch = (event: Event) => {
    const target = event.target as HTMLInputElement;
    const keyword = target.value;
    console.log('入力されました:', target.value);
    if (!keyword) return; // 空っぽなら何もしない
    // URLを /?q=キーワード に書き換えて移動する
    router.push({ path: '/', query: { q: target.value } });
};
// -------------------------------------------------------

// ----- プロフィール編集とログアウトの関数を追加0508 --------
const goToEdit = () => {
    console.log("編集画面へ移動");
    router.push('/profile/edit');
};

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
                        <span class="material-symbols-outlined">search</span>
                        <input 
                            type="text" 
                            placeholder="キーワードから知恵を探す"
                            @keydown.enter="handleSearch"
                        >
                    </div>
                    <button class="post-button" @click="handlePostClick">+ 投稿する</button>

                    <!-- ログアウトボタン0508暫定的---------------- -->
                    <div class="user-menu-container">
                        <div class="profile-icon">
                            <div class="color-avatar">
                                <span>U</span> 
                            </div>
                        </div>

                        <div class="dropdown-menu">
                            <button @click="goToEdit">プロフィール編集</button>
                            <!-- <hr /> -->
                            <button @click="handleLogout" class="logout-btn">ログアウト</button>
                        </div>
                    </div>
                    <!-- ↑0508プロフィール用---------------------------- -->
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
    display: flex;
    align-items: center;
    border: 1.5px solid #2693B4;
    border-radius: 4px;
    padding: 4px 10px;
    width: 100%;
    max-width: 500px;
}

.search-bar input {
    border: none;
    outline: none;
    width: 100%;
    padding: 5px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
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

/* メニューの初期状態：隠しておく */
.dropdown-menu {
    position: absolute;
    right: 0;
    top: 100%;
    background: white;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    border-radius: 8px;
    min-width: 160px;
    z-index: 100;
    /* アニメーション系 */
    opacity: 0;
    visibility: hidden;
    transform: translateY(-10px);
    transition: all 0.3s ease;
}

/* ホバーした時の状態 */
.user-menu-container:hover .dropdown-menu {
    opacity: 1;
    visibility: visible;
    transform: translateY(0);
}

.dropdown-menu button {
    display: block;
    width: 100%;
    padding: 12px;
    text-align: left;
    border: none;
    background: none;
    cursor: pointer;
    transition: all 0.3s ease;
}

.dropdown-menu button:hover {
    background-color: #f5f5f5;
}

.logout-btn {
    color: red;
    font-weight: bold;
}
/* -------------------------------------------------------- */
</style>
