<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>Login do Sistema</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form @submit.prevent="handleLogin">
              <v-alert v-if="error" type="error" dense class="mb-4">{{ error }}</v-alert>
              <v-text-field v-model="credentials.username" label="Usuário" name="login" prepend-icon="mdi-account"
                type="text" required></v-text-field>
              <v-text-field v-model="credentials.password" label="Senha" name="password" prepend-icon="mdi-lock"
                type="password" required></v-text-field>
              <v-card-actions>
                <v-btn text to="/register">
                  Não tem conta?
                </v-btn>
                <v-spacer></v-spacer>
                <v-btn type="submit" color="primary" :loading="loading">Login</v-btn>
              </v-card-actions>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { reactive, ref } from 'vue';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();

const credentials = reactive({
  username: '',
  password: '',
});

const loading = ref(false);
const error = ref('');

async function handleLogin() {
  loading.value = true;
  error.value = '';
  try {
    await authStore.login(credentials);
    // O redirecionamento é feito dentro da action do Pinia
  } catch (err) {
    error.value = 'Usuário ou senha inválidos.';
    console.error(err);
  } finally {
    loading.value = false;
  }
}
</script>