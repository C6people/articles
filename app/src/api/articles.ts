import api from './client';

export type Article = {
  id: string;
  user_id: string;
  title: string;
  body: string;
  content: string;
  author: string;
  category: string;
  likes: number;
  comments: number;
  created_at: string;
};

export async function fetchArticles(): Promise<Article[]> {
  const res = await api.get<Article[]>('/articles');
  return res.data;
}

export const fetchArticleById = async (id: string): Promise<Article> => {
  const response = await api.get<Article>(`/articles/${id}`);
  return response.data;
};