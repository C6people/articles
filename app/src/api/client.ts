import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 10000,
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // 401 Unauthorized (トークンが無効、期限切れなど) の場合
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token');
      alert("セッションが切れました。再度ログインしてください。");
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
