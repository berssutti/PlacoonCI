<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>Execução Orçamentária</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn to="/" text>Visão Geral</v-btn>
      <v-btn to="/projects" text>Lista de Projetos</v-btn>
      <v-divider vertical class="mx-3"></v-divider>
      <NotificationBell />
    </v-app-bar>

    <v-main>
      <v-container>
        <router-view />
      </v-container>
    </v-main>

  </v-app>
</template>

<script>
import NotificationBell from '@/components/ui/NotificationBell.vue';

export default {
  name: 'App',
  components: {
    NotificationBell,
  },
};
</script>

<style>
.v-main {
  min-height: calc(100vh - 64px);
}
</style>
