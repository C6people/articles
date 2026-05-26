<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';
import { useRouter, useRoute } from 'vue-router';
import CommonHeader from '@/components/CommonHeader.vue';

const API_URL = 'http://localhost:8000';

// ルーターのインスタンスを取得
const router = useRouter();
const route = useRoute();

const handleLogout = () => {
	console.log("ログアウト処理実行");
	localStorage.removeItem('token');
	alert("ログアウトしました");
	router.push('/login'); // ログイン画面へ飛ばす
};
const goToPasswordChange = () => {
	// 遷移を実行
	router.push('/password')
}
// --------------------------
//  自己紹介用
const user = ref({
	id: '',
	name: '',
	bio: ''
	// 空データ確認用↓
	// bio: ''
});

// ========== アクティビティ関連 ==========
// 使用技術タグ（ダミーデータ）
const skills = ref([
	'Vue.js',
	'TypeScript',
	'Python',
	'FastAPI',
	'Docker',
	'AWS',
	'PostgreSQL',
	'Git'
]);

// 全利用可能な技術一覧（a～z順）
const allAvailableSkills = ref([
	'AWS',
	'Azure',
	'Bootstrap',
	'C++',
	'C#',
	'CSS',
	'Docker',
	'Electron',
	'Express',
	'FastAPI',
	'Firebase',
	'Flutter',
	'Git',
	'GitHub',
	'GitLab',
	'Go',
	'GraphQL',
	'HTML',
	'Java',
	'JavaScript',
	'Jest',
	'Kubernetes',
	'Laravel',
	'Linux',
	'MongoDB',
	'MySQL',
	'Next.js',
	'Node.js',
	'PostgreSQL',
	'Python',
	'React',
	'Redis',
	'REST API',
	'Ruby',
	'Rust',
	'Sass',
	'Spring Boot',
	'SQL',
	'SQLite',
	'Tailwind CSS',
	'TypeScript',
	'Vue.js',
	'Webpack',
	'Windows',
	'Xcode'
]);

// スキル選択モーダル関連
const isEditingSkills = ref(false);
const selectedSkillsForEdit = ref<string[]>([]);

// ========== 既存のデータ ==========
const isMyProfile = ref(true); 
const userNotFound = ref(false);

// --- モーダル（bio編集関連） ---
// モーダルはマスクみたいな感じです

// 変数
const isEditing = ref(false); // モーダルが開いているか
const tempBio = ref('');      // 編集中の文字を一時保存する場所

// プロフィールを編集ボタン
const startEditing = () => {
	tempBio.value = user.value.bio; // 今の自己紹介をコピー
	isEditing.value = true;         // モーダルを表示
};

// 保存ボタン
const saveBio = async () => {
	try {
		const token = localStorage.getItem('token');

		const response = await axios.put(
			`${API_URL}/users/me`,
			{
				bio: tempBio.value
			},
			{
				headers: {
					Authorization: `Bearer ${token}`
				}
			}
		);

		// 画面更新
		user.value = response.data;

		// モーダル閉じる
		isEditing.value = false;

		console.log("保存成功");

	} catch (error) {
		console.error("保存失敗", error);
		alert("保存に失敗しました");
	}
};
// --------------------------
// タブ切り替え用の初期値設定
const currentTab = ref('記事');

// タブ用記事管理データ
interface ContentItem {
	id: string;
	title: string;
	type?: 'article' | 'question';
}

// 各タブ用のデータ。[] の中にデータがあれば表示、なければ「XXはありません」が出ます。
// データがない場合を確認したいときは{}の中身を空にしてください。
// 記事用
const articles = ref<ContentItem[]>([]);
// 質問用
const questions = ref<ContentItem[]>([]);
// いいね用ダミーデータ
const likes = ref<ContentItem[]>([]);
// --------------------------

const fetchMyProfile = async () => {
	try {
		const token = localStorage.getItem('token');

		const response = await axios.get(
			`${API_URL}/users/me`,
			{
				headers: {
					Authorization: `Bearer ${token}`
				}
			}
		);

		user.value = response.data;

	} catch (error) {
		console.error('プロフィール取得失敗', error);
	}
};

const fetchUserProfile = async (
	userId: string
) => {
	try {

		userNotFound.value =
			false;

		const response =
			await axios.get(
				`${API_URL}/users/${userId}`
			);

		const fetchedUser =
			response.data;

		// ユーザーが存在しない
		if (
			!fetchedUser ||
			!fetchedUser.id
		) {
			userNotFound.value =
				true;
			return;
		}

		user.value =
			fetchedUser;

	} catch (error: any) {

		const status =
			error.response?.status;

		// 404: ユーザー不存在
		// 422: 不正なUUID
		if (
			status === 404 ||
			status === 422
		) {
			userNotFound.value =
				true;
			return;
		}

		console.error(
			'他ユーザプロフィール取得失敗',
			error
		);
	}
};

const fetchUserArticles = async () => {
	try {
		const response = await axios.get(
			`${API_URL}/users/${user.value.id}/articles`
		);

		articles.value = response.data;

	} catch (error) {
		console.error('記事取得失敗', error);
	}
};

const fetchUserQuestions = async () => {
	try {
		const response = await axios.get(
			`${API_URL}/users/${user.value.id}/questions`
		);

		questions.value = response.data;

	} catch (error) {
		console.error('質問取得失敗', error);
	}
};

const fetchUserLikes = async () => {
	try {

		const response = await axios.get(
			`${API_URL}/users/${user.value.id}/likes`
		);

		const likedArticles =
			response.data.articles.map(
				(article: any) => ({
					id: article.id,
					title: article.title,
					type: 'article'
				})
			);

		const likedQuestions =
			response.data.questions.map(
				(question: any) => ({
					id: question.id,
					title: question.title,
					type: 'question'
				})
			);

		// 記事＋質問を結合
		likes.value = [
			...likedArticles,
			...likedQuestions
		];

	} catch (error) {
		console.error(
			'いいね取得失敗',
			error
		);
	}
};

onMounted(async () => {
	const routeUserId =
		route.params.userId as
		string | undefined;

	// URLにuserIdがある
	if (routeUserId) {

		isMyProfile.value =
			false;

		await fetchUserProfile(
			routeUserId
		);

		// ユーザー不存在なら終了
		if (
			userNotFound.value
		) {
			return;
		}
	}
	// 自分のプロフィール
	else {

		isMyProfile.value =
			true;

		await fetchMyProfile();
	}

	// user.id が確定後に取得
	await fetchUserArticles();
	await fetchUserQuestions();
	await fetchUserLikes();
});

// スキル編集開始
const startEditingSkills = () => {
	selectedSkillsForEdit.value = [...skills.value]; // 現在の選択をコピー
	isEditingSkills.value = true;
};

// スキルトグル（選択/非選択）
const toggleSkill = (skill: string) => {
	const index = selectedSkillsForEdit.value.indexOf(skill);
	if (index > -1) {
		// 既に選択されている場合は削除
		selectedSkillsForEdit.value.splice(index, 1);
	} else {
		// 選択されていない場合は追加（ただし10個まで）
		if (selectedSkillsForEdit.value.length < 10) {
			selectedSkillsForEdit.value.push(skill);
		}
	}
};

// スキル選択を確認
const saveSkills = async () => {
	try {
		const token = localStorage.getItem('token');

		// API呼び出し準備（将来実装用）
		// await axios.put(
		// 	`${API_URL}/users/me`,
		// 	{ skills: selectedSkillsForEdit.value },
		// 	{ headers: { Authorization: `Bearer ${token}` } }
		// );

		// 一旦ローカル更新
		skills.value = [...selectedSkillsForEdit.value];
		isEditingSkills.value = false;

		console.log('スキル保存成功', selectedSkillsForEdit.value);
	} catch (error) {
		console.error('スキル保存失敗', error);
		alert('スキルの保存に失敗しました');
	}
};

// スキル選択キャンセル
const cancelEditingSkills = () => {
	isEditingSkills.value = false;
	selectedSkillsForEdit.value = [];
};

// スキル一括選択解除
const clearAllSkills = () => {
	selectedSkillsForEdit.value = [];
};

// 記事編集
const editArticle = (articleId: string) => {
	console.log('記事編集クリック:', articleId);
	router.push(`/detail/${articleId}`);
};

// 質問編集
const editQuestion = (questionId: string) => {
	console.log('質問編集クリック:', questionId);
	router.push(`/detail/${questionId}`);
};

</script>

<template>
	<CommonHeader />
	<div class="profile-page-wrapper">
		<main v-if="!userNotFound" class="profile-container">
    
			<div class="main-content">
				<div class="profile-wrapper">
					<router-link to="/" class="back-link">
						←ホームに戻る
					</router-link>
				</div>
				<div class="user-header">
					<h1><strong>{{ user.name }}</strong> さんのプロフィール</h1>
					<!--   編集モーダルを開くためのボタン。クリックするとisEditingがtrueになり、モーダルが表示される仕組みです。 -->
					<button v-if="isMyProfile" class="btn-edit-profile" @click="startEditing">自己紹介を編集</button>
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
                            </li>
                        </ul>
                        <p v-else class="empty-message">投稿した記事はありません。</p>
                    </div>

                    <div v-else-if="currentTab === '質問'">
                        <ul v-if="questions.length > 0" class="article-list">
                            <li v-for="item in questions" :key="item.id" class="article-item">
                                <span class="article-title">{{ item.title }}</span>
                            </li>
                        </ul>
                        <p v-else class="empty-message">質問はまだありません。</p>
                    </div>

					<div v-else-if="currentTab === 'いいね'">
						<ul v-if="likes.length > 0" class="article-list">
						<li v-for="item in likes" :key="item.id" class="article-item">
						<span class="article-title">
							<span v-if="item.type === 'article'">📝 記事：</span>
							<span v-else>❓ 質問：</span>
							{{ item.title }}
						</span>
					</li>
				</ul>

				<p v-else class="empty-message">
					いいねした投稿はありません。
				</p>
			</div>
		</div>
	</div>

	<!-- サイドバー -->
	<aside class="sidebar">
		<div class="sticky-container">
			<!-- 使用技術タグ -->
			<div class="card skills-card">
				<div class="skills-header">
					<h3 class="card-title">🛠️ 使用技術</h3>
					<button v-if="isMyProfile" class="btn-change-skills" @click="startEditingSkills">
						変更
					</button>
				</div>
				<div class="skills-container">
					<span v-for="skill in skills" :key="skill" class="skill-tag">
						{{ skill }}
					</span>
				</div>
			</div>

			<!-- セキュリティ（自分のプロフィールの場合のみ表示） -->
			<div v-if="isMyProfile" class="card action-card">
				<span>アカウントセキュリティ</span>
				<p class="action-description">パスワードを変更して、アカウントをより安全に保ちましょう。</p>
				<button @click="goToPasswordChange" class="btn-action-red">パスワードを変更</button>
			</div>
		</div>
	</aside>
        
	</main>
	<div
	v-else
	class="not-found-container"
	>
		<h1>
			ユーザーが見つかりません
		</h1>

		<p>
			指定されたユーザーは
			存在しないか、
			削除された可能性があります。
		</p>

		<button
			class="back-button"
			@click="router.push('/')"   
			>
			ホームへ戻る
		</button>
	</div>

	<!-- 編集モーダル -->
	<!-- isEditingがtrueの時に表示なのでmodal-container以外（背景半透明）に触れると閉じるようになっています -->
	<div v-if="isMyProfile && isEditing" class="modal-mask" @click.self="isEditing = false">
		<div class="modal-container">
			<h3>自己紹介を編集</h3>
			<textarea 
				v-model="tempBio" 
					class="edit-bio-area" 
					placeholder="自己紹介を入力してください"
				></textarea>
				<div class="modal-buttons">
					<button class="btn-save" @click="saveBio">保存</button>
					<button class="btn-cancel" @click="isEditing = false">キャンセル</button>
				</div>
			</div>
		</div>
		<!-- ------------------------ -->

	<!-- スキル選択モーダル -->
	<div v-if="isEditingSkills" class="modal-mask" @click.self="cancelEditingSkills">
		<div class="modal-container skills-modal-container">
			<div class="skills-modal-header">
				<div class="skills-modal-title-row">
					<h3>使用技術を選択</h3>
					<button v-if="selectedSkillsForEdit.length > 0" class="btn-clear-all" @click="clearAllSkills">
						クリア
					</button>
				</div>
				<p class="skills-modal-subtitle">最大10個まで選択できます（選択中: {{ selectedSkillsForEdit.length }} / 10）</p>
			</div>

			<div class="skills-selection-grid">
				<label v-for="skill in allAvailableSkills" :key="skill" class="skill-checkbox-label">
					<input
						type="checkbox"
						:value="skill"
						:checked="selectedSkillsForEdit.includes(skill)"
						:disabled="!selectedSkillsForEdit.includes(skill) && selectedSkillsForEdit.length >= 10"
						@change="toggleSkill(skill)"
						class="skill-checkbox"
					/>
					<span class="skill-checkbox-text">{{ skill }}</span>
				</label>
			</div>

			<div class="modal-buttons">
				<button class="btn-save" @click="saveSkills">保存</button>
				<button class="btn-cancel" @click="cancelEditingSkills">キャンセル</button>
			</div>
		</div>
	</div>
	<!-- ======================== -->
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
/* --- ホームに戻るボタン --- */
/* 親要素 */
.profile-wrapper {
	margin-bottom: 40px;
}

/* ホームに戻るリンク */
.back-link {
	background: #f0f2f5;
	border: 3px solid #2693B4;
	border-radius: 20px;
	padding: 6px 24px;
	color: #2693B4;
	cursor: pointer;
	margin-bottom: 30px;
	margin-top: 10px;
	font-weight: bold;
	font-size: 0.875rem;
	text-decoration: none;
	transition: ease-out 0.3s;
}

.back-link:hover {
	background-color: #2693B4;
	color: #fff;
}
/* --- ↑ホームに戻るボタン --- */

/* ---  メインレイアウト --- */
.profile-container {
	display: grid;
	grid-template-columns: 1fr 320px;
	justify-items: start;
	align-items: start;
	max-width: 1200px;
	margin: 0 auto;
	padding: 30px 50px;
	gap: 40px;
}

.main-content {
	min-width: 0;
	width: 100%;
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
	color: #fff;
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
/* --- 自己紹介見出し --- */
.bio-label { 
	font-weight: bold;
	margin-bottom: 8px;
	font-size: 14px;
}
/* --- 自己紹介本文 --- */
.bio-text { 
	font-size: 14px;
	line-height: 1.6;
	color: #555; 
}

/* --- タブ部分（記事、質問、いいね） --- */
/* タブ全体のコンテナ */
.profile-tabs {
	display: flex;
	justify-content: center; /* 真ん中のほうが何となくいいのでタブを中央に配置しました */
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
	color: #fff !important;
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
	color: #fff;
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
	margin-top: 0;
}

/* スティッキーコンテナ */
.sticky-container {
	position: sticky;
	top: 100px;
	display: flex;
	flex-direction: column;
	gap: 20px;
}

/* ========== カード共通スタイル拡張 ========== */
.card-title {
	font-size: 16px;
	font-weight: bold;
	color: #333;
	margin: 0 0 16px 0;
	display: flex;
	align-items: center;
	gap: 6px;
}

/* ========== 使用技術タグ ========== */
.skills-card {
	background: #fff;
	border-radius: 12px;
	box-shadow: 0 2px 8px rgba(0,0,0,0.06);
	padding: 20px;
}

.skills-header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	margin-bottom: 16px;
}

.skills-header .card-title {
	margin: 0;
}

.btn-change-skills {
	background: none;
	border: 1px solid #2693B4;
	color: #2693B4;
	padding: 4px 12px;
	border-radius: 12px;
	font-size: 12px;
	font-weight: bold;
	cursor: pointer;
	transition: all 0.3s ease;
}

.btn-change-skills:hover {
	background-color: #2693B4;
	color: #fff;
}

.skills-container {
	display: flex;
	flex-wrap: wrap;
	gap: 8px;
}

.skill-tag {
	display: inline-block;
	background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
	color: #fff;
	padding: 6px 12px;
	border-radius: 20px;
	font-size: 12px;
	font-weight: 500;
	transition: all 0.3s ease;
	cursor: default;
	white-space: nowrap;
}

.skill-tag:hover {
	transform: translateY(-2px);
	box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.action-card {
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	gap: 10px;
	background: #fff;
	border-radius: 12px;
	box-shadow: 0 2px 8px rgba(0,0,0,0.06);
	padding: 20px;
}
.action-card span {
	font-size: 16px;
	font-weight: bold;
	color: #333;
}
.action-description {
	font-size: 13px;
	color: #666;
	text-align: center;
	margin: 0;
	line-height: 1.4;
}
.btn-action-red {
	width: 100%;
	border: none;
	background-color: #b42626;
	color: #fff;
	border-radius: 8px;
	padding: 12px 24px;
	cursor: pointer;
	font-weight: bold;
	font-size: 15px;
	transition: all 0.3s ease;
}
.btn-action-red:hover {
	background-color: #8b1d1d;
	transform: translateY(-2px);
	box-shadow: 0 4px 12px rgba(180, 38, 38, 0.3);
}

/* --- モーダル関連 --- */
.modal-mask {
	position: fixed;
	z-index: 9999;
	top: 0;
	left: 0;
	width: 100vw;
	height: 100vh;
	background-color: rgba(0,0,0,0.5);
	display: flex;
	justify-content: center;
	align-items: center;
}

/* モーダル中央の白い箱 */
.modal-container {
	background: #f0f2f5;
	padding: 24px;
	border-radius: 15px;
	width: 90%;
	max-width: 500px;
	box-shadow: 0 4px 20px rgba(0,0,0,0.2);
	color: #3c3c3c;
}
.modal-container h3 {
	margin-top: 0;
	font-size: 20px;
	font-weight: bold;
}
/* 入力エリア */
.edit-bio-area {
	background-color: #fff; /* 入力欄は真っ白 */
	box-shadow: inset 0 1px 3px rgba(0,0,0,0.02); /* ほんの少しの立体感 */
	font-family: sans-serif;
	width: 100%;
	height: 150px;
	margin: 15px 0;
	padding: 15px;
	border: 1px solid #e8e8e8; /* 線は極薄 */
	border-radius: 15px;
	resize: none; /* ユーザがサイズ変更できないようにしました 縦方向のサイズ変更はnoneをverticalに変更してください*/
	transition: ease-out 0.3s;
}
.edit-bio-area:focus {
	border: 1px solid #c3c3c3;
	outline: none;
}
/* ボタンの並び */
.modal-buttons {
	display: flex;
	justify-content: flex-end;
	gap: 10px;
}

.btn-save {
	background-color: #2693B4;
	color: #f0f2f5;
	border: none;
	padding: 8px 16px;
	border: 3px solid #2693B4;
	border-radius: 70px;
	cursor: pointer;
	font-weight: bold;
	transition: ease-out 0.3s;
}
.btn-save:hover {
	background-color: #1a6d85; 
	border-color: #1a6d85;
}

.btn-cancel {
	background-color: #f0f2f5;
	color: #f44336;
	border: none;
	padding: 8px 16px;
	border: 3px solid #f44336;
	border-radius: 70px;
	cursor: pointer;
	font-weight: bold;
	transition: ease-out 0.3s;
}
.btn-cancel:hover {
	background-color: #f44336;
	color: #f0f2f5;
	border: 3px solid #f44336;
}
/* --- ↑モーダル --- */

/* ========== スキル選択モーダル ========== */
.skills-modal-container {
	width: 90%;
	max-width: 600px;
	max-height: 80vh;
	overflow-y: auto;
}

.skills-modal-header {
	margin-bottom: 24px;
}

.skills-modal-title-row {
	display: flex;
	justify-content: space-between;
	align-items: center;
	gap: 12px;
}

.skills-modal-header h3 {
	margin: 0;
	font-size: 20px;
	font-weight: bold;
}

.btn-clear-all {
	background: none;
	border: 1px solid #ff6b6b;
	color: #ff6b6b;
	padding: 2px 8px;
	border-radius: 4px;
	font-size: 11px;
	font-weight: 600;
	cursor: pointer;
	transition: all 0.2s ease;
	white-space: nowrap;
}

.btn-clear-all:hover {
	background-color: #ff6b6b;
	color: #fff;
}

.skills-modal-subtitle {
	margin: 0;
	font-size: 13px;
	color: #666;
}

.skills-selection-grid {
	display: grid;
	grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
	gap: 12px;
	margin-bottom: 24px;
	padding: 16px;
	background: #f8f9fa;
	border-radius: 8px;
	max-height: 400px;
	overflow-y: auto;
}

.skill-checkbox-label {
	display: flex;
	align-items: center;
	gap: 8px;
	padding: 8px 12px;
	cursor: pointer;
	border-radius: 6px;
	transition: all 0.2s ease;
	user-select: none;
}

.skill-checkbox-label:hover {
	background: #e8eef7;
}

.skill-checkbox {
	cursor: pointer;
	width: 18px;
	height: 18px;
	accent-color: #2693B4;
}

.skill-checkbox:disabled {
	cursor: not-allowed;
	opacity: 0.5;
}

.skill-checkbox-text {
	font-size: 13px;
	color: #333;
	flex: 1;
	overflow: hidden;
	text-overflow: ellipsis;
	white-space: nowrap;
}

.skill-checkbox-label:has(.skill-checkbox:checked) {
	background: #d4e8f0;
	font-weight: 500;
}
/* ======================== */

/* 画面幅が 768px 以下（タブレットやスマホ）になったら適用 */
@media (max-width: 768px) {
	.profile-wrapper {
	padding-top: 20px;
	}
	
	.profile-container {
		grid-template-columns: 1fr;
		padding: 20px 20px;
		gap: 20px;
	}

	.main-content {
		width: 100%;
	}

	/* サイドバーも全幅 */
	.sidebar {
		width: 100%;
	}

	.sticky-container {
		position: static;
		flex-direction: column;
		gap: 20px;
	}

	/* スマホではタグを2行に */
	.skills-container {
		justify-content: space-between;
	}

	.skill-tag {
		flex: 0 0 calc(50% - 4px);
		text-align: center;
	}

	/* スマホのモーダルサイズ調整 */
	.skills-modal-container {
		width: 95%;
		max-height: 90vh;
	}

	.skills-selection-grid {
		grid-template-columns: repeat(auto-fill, minmax(100px, 1fr));
		max-height: 300px;
	}
}

.not-found-container {
	min-height: 70vh;
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	text-align: center;
	gap: 16px;
}

.not-found-container h1 {
	font-size: 32px;
	color: #333;
}

.not-found-container p {
	color: #666;
	font-size: 16px;
}

.back-button {
	background: none;
	border: 1px solid #2693B4;
	color: #2693B4;
	padding: 8px 20px;
	border-radius: 20px;
	cursor: pointer;
}
</style>
