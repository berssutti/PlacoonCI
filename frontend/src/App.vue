<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>Execução Orçamentária</v-toolbar-title>
      <v-spacer></v-spacer>
      
      <template v-if="isLoggedIn">
        <v-btn to="/" text>Visão Geral</v-btn>
        <v-btn to="/projects" text>Lista de Projetos</v-btn>
        <v-btn @click="logout" text>
          <v-icon left>mdi-logout</v-icon>
          Sair
        </v-btn>
      </template>
    </v-app-bar>

    <v-main>
      <v-container>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import { mapState, mapActions } from 'pinia';
import { useAuthStore } from '@/stores/auth';

export default {
  name: 'App',
  computed: {
    ...mapState(useAuthStore, ['isLoggedIn']),
  },
  methods: {
    ...mapActions(useAuthStore, ['logout']),
  }
};
</script>

<style>
.v-main {
  /* 64px é a altura padrão da v-app-bar */
  min-height: calc(100vh - 64px); 
}
</style>