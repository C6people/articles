# フロントエンド（Vue 3）開発ガイド

このプロジェクトのフロントエンド (`app/`) の構成と、ファイルの追加方法をまとめたドキュメントです。

---

## 📂 ディレクトリ構成

現在のフロントエンドのフォルダ構成と、**今後追加すべきフォルダ**は以下の通りです。
`★` マークが付いているものは今後新しく作るフォルダです。

```
app/src/
├── main.ts              ← アプリの起動ファイル（基本触らない）
├── App.vue              ← アプリ全体の大枠（ルーターの表示先を置く）
│
├── assets/              ← 画像・CSS などの静的ファイル
│   ├── base.css
│   ├── main.css
│   └── logo.svg
│
├── components/          ← 再利用できる小さな部品（ボタン、カードなど）
│   ├── HelloWorld.vue      ← サンプル（後で消してOK）
│   ├── TheWelcome.vue      ← サンプル（後で消してOK）
│   └── WelcomeItem.vue     ← サンプル（後で消してOK）
│
├── ★ views/             ← 各画面のページファイルを置く場所
│   ├── HomeView.vue         ← トップページ
│   ├── ArticleListView.vue  ← 記事一覧画面
│   ├── ArticleDetailView.vue← 記事詳細画面
│   ├── QuestionListView.vue ← 質問一覧画面
│   ├── QuestionDetailView.vue← 質問詳細画面
│   └── LoginView.vue        ← ログイン画面
│
├── ★ router/            ← ページ遷移（ルーティング）の設定
│   └── index.ts             ← URLとページの紐付けを定義する
│
├── ★ api/               ← バックエンド（FastAPI）との通信処理
│   └── client.ts            ← API呼び出し用の関数をまとめる
│
└── ★ types/             ← TypeScriptの型定義
    └── index.ts             ← Article, User などのデータの型を定義
```

---

## 🧩 各フォルダの役割と「何を書くか」

### 1. `views/` — 画面（ページ）
**「URL（アドレス）ごとに1つ作る」** のが基本です。

例えば、以下のような対応になります：
| URL | ファイル | 内容 |
|---|---|---|
| `/` | `HomeView.vue` | トップページ |
| `/articles` | `ArticleListView.vue` | 記事の一覧を表示 |
| `/articles/123` | `ArticleDetailView.vue` | 記事の詳細と本文を表示 |
| `/questions` | `QuestionListView.vue` | 質問の一覧を表示 |
| `/login` | `LoginView.vue` | ログインフォーム |

### 2. `components/` — 部品（パーツ）
**「複数の画面で繰り返し使う部品」** を置きます。

例：
- `ArticleCard.vue` — 記事一覧で表示する1つ分のカード
- `CommentForm.vue` — コメント入力フォーム（記事・質問の両方で使える）
- `LikeButton.vue` — いいねボタン
- `UserAvatar.vue` — ユーザーのアイコンと名前の表示

### 3. `router/index.ts` — ルーティング設定
**「このURLにアクセスしたら、このページ（view）を表示してね」** という設定を書きます。

```ts
// router/index.ts のイメージ
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import ArticleListView from '@/views/ArticleListView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/',          component: HomeView },
    { path: '/articles',  component: ArticleListView },
    // ... 他のページも同様に追加
  ],
})

export default router
```

> ⚠️ ルーターを使うには `vue-router` パッケージのインストールが必要です。
> ```bash
> cd app && npm install vue-router
> ```

### 4. `api/client.ts` — API通信
**「バックエンド（FastAPI）からデータを取ってくる処理」** をまとめます。

```ts
// api/client.ts のイメージ
const API_BASE = 'http://localhost:8000'

// 記事一覧を取得する関数
export async function getArticles() {
  const res = await fetch(`${API_BASE}/articles`)
  return await res.json()
}

// 記事を投稿する関数
export async function createArticle(title: string, body: string) {
  const res = await fetch(`${API_BASE}/articles`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, body }),
  })
  return await res.json()
}
```

### 5. `types/index.ts` — 型定義
**「APIから返ってくるデータの形（型）」** を定義します。
チーム内で「このデータにはどんな項目が入っているか」を共有するのに役立ちます。

```ts
// types/index.ts のイメージ
export interface User {
  id: number
  user_id: string
  name: string
  role: 'student' | 'teacher'
}

export interface Article {
  id: number
  user_id: number
  title: string
  body: string
  created_at: string
}
```

---

## 🚀 新しい画面を追加する手順（まとめ）

例えば「記事一覧画面」を追加したい場合の手順：

1. **`views/ArticleListView.vue`** を作成し、画面のHTML・ロジックを書く
2. **`components/ArticleCard.vue`** など、必要な部品を作成する
3. **`router/index.ts`** に `{ path: '/articles', component: ArticleListView }` を追加する
4. **`api/client.ts`** に `getArticles()` 関数を追加する
5. ブラウザで `http://localhost:5173/articles` にアクセスして確認！

---

## 💡 Tips

- **`@` は `src/` のショートカット**: `import Foo from '@/components/Foo.vue'` のように書くと、どのファイルからでも `src/` を起点にしたパスで import できます（`vite.config.ts` で設定済み）。
- **ファイル名のルール**: Vue のファイルは **PascalCase**（例: `ArticleCard.vue`）で命名するのが Vue の公式推奨です。
- **サンプルファイルの削除**: `components/` にある `HelloWorld.vue`, `TheWelcome.vue`, `WelcomeItem.vue` は Vite が自動生成したサンプルなので、開発を始めたら削除してOKです。
