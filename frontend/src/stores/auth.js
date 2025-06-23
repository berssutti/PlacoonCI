// src/stores/auth.js

import { defineStore } from 'pinia';
import api from '@/services/api';
import router from '@/router';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: localStorage.getItem('accessToken') || null,
    refreshToken: localStorage.getItem('refreshToken') || null,
    user: JSON.parse(localStorage.getItem('user')) || null,
  }),

  getters: {
    isLoggedIn: (state) => !!state.accessToken,
    userRoles: (state) => state.user?.groups?.map(group => group.name) || [],
    isAdmin: (state) => state.userRoles.includes('Administrador'),
  },

  actions: {
    async login(credentials) {
      const response = await api.post('/auth/jwt/create/', credentials);
      
      this.accessToken = response.data.access;
      this.refreshToken = response.data.refresh;

      localStorage.setItem('accessToken', this.accessToken);
      localStorage.setItem('refreshToken', this.refreshToken);
      
      await this.fetchUser();
      router.push('/');
    },

    async fetchUser() {
      if (this.accessToken) {
        api.defaults.headers.common['Authorization'] = `Bearer ${this.accessToken}`;
        
        const response = await api.get('/auth/users/me/');
        this.user = response.data;
        localStorage.setItem('user', JSON.stringify(this.user));
      }
    },

    logout() {
      this.accessToken = null;
      this.refreshToken = null;
      this.user = null;

      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      localStorage.removeItem('user');
      
      delete api.defaults.headers.common['Authorization'];

      router.push('/login');
    },

    async register(userData) {
      try {
        await api.post('/auth/users/', {
          username: userData.username,
          email: userData.email,
          password: userData.password,
          re_password: userData.password_confirmation, // O frontend envia a confirmação
        });

        alert('Cadastro realizado com sucesso! Você será redirecionado para a tela de login. Aguarde a aprovação de um administrador para ter acesso completo ao sistema.');
        router.push('/login');   
      } catch (error) {
        console.error('Falha no cadastro:', error.response.data);
        throw error.response.data;
      }
    },
  },
});