# フロントエンド（Vue 3）開発ガイド

このプロジェクトのフロントエンド (`app/`) の構成と開発方法をまとめたドキュメントです。

---

## 技術スタック

| カテゴリ | 技術 |
|---------|------|
| フレームワーク | Vue 3 (Composition API + `<script setup>`) |
| 言語 | TypeScript |
| ルーティング | vue-router |
| HTTP通信 | axios |
| ビルドツール | Vite |
| 型チェック | vue-tsc |

---

## 主要パッケージ

### dependencies (本番で必要)
| パッケージ | 用途 |
|-----------|------|
| `vue` | UIフレームワーク |
| `vue-router` | ページ遷移（ルーティング） |
| `axios` | API通信（JWTトークンの自動付与付き） |

### devDependencies (開発時のみ)
| パッケージ | 用途 |
|-----------|------|
| `vite` | 開発サーバー・ビルドツール |
| `@vitejs/plugin-vue` | Vite用Vueプラグイン |
| `typescript` | TypeScript コンパイラ |
| `vue-tsc` | Vue + TypeScript の型チェック |
| `vite-plugin-vue-devtools` | Vue DevTools連携 |
| `npm-run-all2` | npm スクリプトの並列実行 |

---

## 📂 ディレクトリ構成

```
app/src/
├── main.ts              ← アプリの起動ファイル（基本触らない）
├── App.vue              ← アプリ全体の大枠（ルーターの表示先を置く）
│
├── assets/              ← 画像・CSS などの静的ファイル
│   ├── base.css
│   ├── main.css
│   ├── logo.png            ← サイトロゴ画像
│   └── logo.svg
│
├── components/          ← 再利用できる小さな部品
│   └── CommonHeader.vue    ← 全画面共通のヘッダー（検索バー・投稿ボタン・ユーザーメニュー）
│
├── views/               ← 各画面のページファイル
│   ├── HomeView.vue        ← トップページ（記事・質問の一覧表示）
│   ├── PostFormView.vue    ← 新規投稿画面
│   ├── PostDetail.vue      ← 記事・質問の詳細画面
│   ├── LoginView.vue       ← ログイン画面
│   └── SignUpView.vue      ← 新規登録画面
│
├── router/              ← ページ遷移（ルーティング）の設定
│   └── index.ts            ← URLとページの紐付け＋認証ガード
│
└── api/                 ← バックエンド（FastAPI）との通信処理
    ├── client.ts           ← axiosインスタンス（トークン自動付与・401ハンドリング）
    ├── articles.ts         ← 記事APIの型定義と取得関数
    └── questions.ts        ← 質問APIの型定義と取得関数
```

---

## 🧩 各フォルダの役割

### 1. `views/` — 画面（ページ）
**「URL（アドレス）ごとに1つ作る」** のが基本です。

| URL | ファイル | 内容 |
|---|---|---|
| `/` | `HomeView.vue` | トップページ（記事＋質問の一覧） |
| `/post` | `PostFormView.vue` | 新規投稿画面 |
| `/post/:id` | `PostDetail.vue` | 記事・質問の詳細表示 |
| `/login` | `LoginView.vue` | ログインフォーム |
| `/signup` | `SignUpView.vue` | 新規登録フォーム |

### 2. `components/` — 部品（パーツ）
**「複数の画面で繰り返し使う部品」** を置きます。

- `CommonHeader.vue` — 全画面共通のヘッダー（ロゴ・検索バー・投稿ボタン・ユーザーメニュー）

### 3. `router/index.ts` — ルーティング設定 + 認証ガード
- URLとページの対応関係を定義
- `beforeEach` ガードにより、ログイン/新規登録以外のページはトークンが無いとアクセスできない

### 4. `api/` — API通信
- `client.ts` — axiosインスタンスの設定
  - **リクエストインターセプター**: `localStorage` のトークンを自動で `Authorization` ヘッダーに付与
  - **レスポンスインターセプター**: 401エラー時にトークン削除＋ログイン画面へリダイレクト
- `articles.ts` — 記事の取得関数（一覧・個別）と `Article` 型定義
- `questions.ts` — 質問の取得関数（一覧・個別）と `Question` 型定義

---

## 💡 Tips

- **`@` は `src/` のショートカット**: `import Foo from '@/components/Foo.vue'` のように書くと、どのファイルからでも `src/` を起点にしたパスで import できます（`vite.config.ts` で設定済み）。
- **ファイル名のルール**: Vue のファイルは **PascalCase**（例: `CommonHeader.vue`）で命名するのが Vue の公式推奨です。
- **Node.jsバージョン**: `v20.19` 以上 または `v22.12` 以上が必要です（`package.json` の `engines` で指定）。
