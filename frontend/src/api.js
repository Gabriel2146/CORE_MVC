import axios from 'axios';

const baseURL = import.meta.env.PROD
  ? 'https://core-mvc-2146.onrender.com/api'
  : 'http://localhost:8000/api';

const api = axios.create({
  baseURL,
});

// Opcional: agregar interceptor para agregar token de autorización si existe
api.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
