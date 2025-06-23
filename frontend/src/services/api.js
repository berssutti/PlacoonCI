import axios from 'axios';
import { useAuthStore } from '@/stores/auth';

const api = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL,
});

api.interceptors.response.use(
  (response) => response, // Retorna a resposta se for bem-sucedida
  async (error) => {
    const originalRequest = error.config;
    const authStore = useAuthStore();

    // Verifica se o erro é 401 (Não Autorizado) e se não é uma tentativa de refresh
    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true; // Marca para evitar loop infinito

      if (authStore.refreshToken) {
        try {
          // Tenta renovar o token
          const response = await axios.post(`${api.defaults.baseURL}auth/jwt/refresh/`, {
            refresh: authStore.refreshToken,
          });
          
          // Atualiza o token de acesso na store e no localStorage
          authStore.accessToken = response.data.access;
          localStorage.setItem('accessToken', response.data.access);
          
          // Atualiza o cabeçalho da requisição original e a repete
          originalRequest.headers['Authorization'] = `Bearer ${response.data.access}`;
          return api(originalRequest);
        } catch (refreshError) {
          // Se a renovação falhar, desloga o usuário
          console.error('Unable to refresh token:', refreshError);
          authStore.logout();
          return Promise.reject(refreshError);
        }
      } else {
         // Se não há refresh token, desloga
         authStore.logout();
      }
    }

    return Promise.reject(error);
  }
);

export default api;
