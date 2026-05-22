import api from './client';

export interface LikeResponse {
  message: string;
  likes_count: number;
}

export const likeArticle = async (articleId: string): Promise<LikeResponse> => {
  const response = await api.post<LikeResponse>(`/articles/${articleId}/likes`);
  return response.data;
};

export const likeQuestion = async (questionId: string): Promise<LikeResponse> => {
  const response = await api.post<LikeResponse>(`/questions/${questionId}/likes`);
  return response.data;
};

export const likeArticleComment = async (commentId: string): Promise<LikeResponse> => {
  const response = await api.post<LikeResponse>(`/article-comments/${commentId}/likes`);
  return response.data;
};

export const likeQuestionComment = async (commentId: string): Promise<LikeResponse> => {
  const response = await api.post<LikeResponse>(`/question-comments/${commentId}/likes`);
  return response.data;
};

export const unlikeArticle = async (articleId: string): Promise<LikeResponse> => {
  const response = await api.delete<LikeResponse>(`/articles/${articleId}/likes`);
  return response.data;
};

export const unlikeQuestion = async (questionId: string): Promise<LikeResponse> => {
  const response = await api.delete<LikeResponse>(`/questions/${questionId}/likes`);
  return response.data;
};

export const unlikeArticleComment = async (commentId: string): Promise<LikeResponse> => {
  const response = await api.delete<LikeResponse>(`/article-comments/${commentId}/likes`);
  return response.data;
};

export const unlikeQuestionComment = async (commentId: string): Promise<LikeResponse> => {
  const response = await api.delete<LikeResponse>(`/question-comments/${commentId}/likes`);
  return response.data;
};
