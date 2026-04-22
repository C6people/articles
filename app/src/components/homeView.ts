import { ref, computed } from 'vue'

// --- 型定義 ---
export type ContentType = 'question' | 'article' | 'project'
export type Category = 'programming' | 'design' | 'general' | 'other'

export interface Post {
  id: number
  type: ContentType
  title: string
  content: string
  author: string
  authorRole: 'student' | 'teacher'
  category: Category
  likes: number
  createdAt: string
}

export function useHome() {
  // --- 状態管理 ---
  const currentView = ref<'home' | 'detail' | 'new'>('home')
  const selectedPost = ref<Post | null>(null)
  const selectedCategory = ref<Category | 'all'>('all')
  const searchQuery = ref('')

  // --- ダミーデータ ---
  const posts = ref<Post[]>([
    {
      id: 1,
      type: 'question',
      title: 'ReactのuseEffectの依存配列について教えてください',
      content: 'useEffectの第二引数に空配列を渡した場合と、省略した場合の違いを教えてください。',
      author: '山田太郎',
      authorRole: 'student',
      category: 'programming',
      likes: 24,
      createdAt: '2026-04-20 13:00',
    },
    {
      id: 2,
      type: 'article',
      title: 'Vue3 + TypeScript の導入メリット',
      content: '型安全な開発が可能になり、大規模開発での保守性が向上します。',
      author: '田中次郎',
      authorRole: 'student',
      category: 'programming',
      likes: 15,
      createdAt: '2026-04-21 10:00',
    }
  ])

  const categories = [
    { id: 'programming', name: 'プログラミング' },
    { id: 'design', name: 'デザイン' },
    { id: 'general', name: '一般' },
    { id: 'other', name: 'その他' },
  ]

  // --- 新規投稿用 ---
  const newPostTitle = ref('')
  const newPostContent = ref('')

  // --- 検索・フィルタリングロジック ---
  const filteredPosts = computed(() => {
    return posts.value.filter((post) => {
      const matchesCategory = selectedCategory.value === 'all' || post.category === selectedCategory.value
      const matchesSearch = post.title.toLowerCase().includes(searchQuery.value.toLowerCase())
      return matchesCategory && matchesSearch
    })
  })

  // --- アクション ---
  const handleCreatePost = () => {
    if (!newPostTitle.value || !newPostContent.value) return

    const newPost: Post = {
      id: posts.value.length + 1,
      type: 'question',
      title: newPostTitle.value,
      content: newPostContent.value,
      author: 'ゲストユーザー',
      authorRole: 'student',
      category: 'programming',
      likes: 0,
      createdAt: new Date().toLocaleString(),
    }

    posts.value = [newPost, ...posts.value]
    newPostTitle.value = ''
    newPostContent.value = ''
    currentView.value = 'home'
  }

  const showDetail = (post: Post) => {
    selectedPost.value = post
    currentView.value = 'detail'
  }

  const goHome = () => {
    currentView.value = 'home'
    selectedPost.value = null
  }

  const goNewPost = () => {
    currentView.value = 'new'
  }

  return {
    currentView,
    selectedPost,
    selectedCategory,
    searchQuery,
    posts,
    categories,
    newPostTitle,
    newPostContent,
    filteredPosts,
    handleCreatePost,
    showDetail,
    goHome,
    goNewPost
  }
}
