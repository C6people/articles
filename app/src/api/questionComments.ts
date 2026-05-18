import api from './client';

export interface QuestionCommentResponse {
  id: string;
  question_id: string;
  user_id: string;
  parent_id: string | null;
  body: string;
  is_answer: boolean;
  is_best: boolean;
  created_at: string;
  user_name: string | null;
}

export interface QuestionCommentCreateRequest {
  parent_id?: string | null;
  body: string;
  is_answer?: boolean;
}

export const fetchQuestionComments = async (questionId: string): Promise<QuestionCommentResponse[]> => {
  const response = await api.get(`/questions/${questionId}/comments`);
  return response.data;
};

export const postQuestionComment = async (questionId: string, data: QuestionCommentCreateRequest): Promise<QuestionCommentResponse> => {
  const response = await api.post(`/questions/${questionId}/comments`, data);
  return response.data;
};

export const setBestAnswer = async (questionId: string, commentId: string): Promise<QuestionCommentResponse> => {
  const response = await api.patch(`/questions/${questionId}/comments/${commentId}/best`);
  return response.data;
};
