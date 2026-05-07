<script setup lang="ts">
import { useRouter } from 'vue-router';

const router = useRouter();

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
</style>
