<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>Execução Orçamentária</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn to="/" text>Visão Geral</v-btn>
      <v-btn to="/projects" text>Lista de Projetos</v-btn>
    </v-app-bar>

    <v-main>
      <v-container>
        <router-view />
      </v-container>
    </v-main>

  </v-app>
</template>

<script>
  export default {
    name: 'App',
  };
</script>

<style>
.v-main {
  min-height: calc(100vh - 64px);
}
</style>
