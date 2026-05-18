import api from './client';

export interface CommentResponse {
  id: string;
  article_id: string;
  user_id: string;
  parent_id: string | null;
  body: string;
  created_at: string;
  user_name: string | null;
}

export interface CommentCreateRequest {
  parent_id?: string | null;
  body: string;
}

export const fetchComments = async (articleId: string): Promise<CommentResponse[]> => {
  const response = await api.get(`/articles/${articleId}/comments`);
  return response.data;
};

export const postComment = async (articleId: string, data: CommentCreateRequest): Promise<CommentResponse> => {
  const response = await api.post(`/articles/${articleId}/comments`, data);
  return response.data;
};
