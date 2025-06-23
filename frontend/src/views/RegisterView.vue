<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>Criar Conta</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form @submit.prevent="handleRegister">
              <v-alert v-if="error" type="error" dense class="mb-4" closable @click:close="error = ''">
                <ul>
                  <li v-for="(msg, field) in error" :key="field">
                    {{ field }}: {{ msg.join(', ') }}
                  </li>
                </ul>
              </v-alert>

              <v-text-field
                v-model="formData.username"
                label="Nome de Usuário"
                prepend-icon="mdi-account"
                required
              ></v-text-field>

              <v-text-field
                v-model="formData.email"
                label="E-mail"
                type="email"
                prepend-icon="mdi-email"
                required
              ></v-text-field>

              <v-text-field
                v-model="formData.password"
                label="Senha"
                type="password"
                prepend-icon="mdi-lock"
                required
              ></v-text-field>

              <v-text-field
                v-model="formData.password_confirmation"
                label="Confirme a Senha"
                type="password"
                prepend-icon="mdi-lock-check"
                required
              ></v-text-field>

              <v-card-actions class="pa-0">
                 <v-btn text to="/login">Já tem uma conta?</v-btn>
                <v-spacer></v-spacer>
                <v-btn type="submit" color="primary" :loading="loading">Cadastrar</v-btn>
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

const formData = reactive({
  username: '',
  email: '',
  password: '',
  password_confirmation: '',
});

const loading = ref(false);
// O erro agora pode ser um objeto para exibir múltiplas mensagens
const error = ref(null);

async function handleRegister() {
  // Limpa erros anteriores
  error.value = null;

  // Validação simples no frontend antes de enviar
  if (formData.password !== formData.password_confirmation) {
    error.value = { password: ['As senhas não coincidem.'] };
    return;
  }
  
  loading.value = true;
  try {
    await authStore.register(formData);
    // O redirecionamento é feito dentro da action
  } catch (err) {
    // Captura os erros da API (que foram relançados pela action)
    error.value = err;
  } finally {
    loading.value = false;
  }
}
</script>