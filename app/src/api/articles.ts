import api from './client';

export type Article = {
  id: string;
  title: string;
  content: string;
  author: string;
  category: string;
  likes: number;
  comments: number;
  createdAt: string;
};

export async function fetchArticles(): Promise<Article[]> {
  const res = await api.get<Article[]>('/articles');
  return res.data;
}
