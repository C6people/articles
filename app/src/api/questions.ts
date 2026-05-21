import api from './client';

export type Question = {
  id: string;
  user_id: string;
  user_name: string | null;
  title: string;
  body: string;
  likes_count: number;
  created_at: string;
};

export async function fetchQuestions(): Promise<Question[]> {
  const res = await api.get<Question[]>('/questions');
  return res.data;
}

export const fetchQuestionById = async (id: string): Promise<Question> => {
  const response = await api.get<Question>(`/questions/${id}`);
  return response.data;
};
