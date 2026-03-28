<template>
  <v-app>
    <v-navigation-drawer
      v-model="drawer"
      permanent
      elevation="0"
      border="0"
      class="bg-white border-e"
    >
      <v-list class="pa-4">
        <v-list-item class="px-0 mb-6">
          <div class="d-flex align-center">
            <div class="bg-primary rounded-lg pa-2 mr-3">
              <v-icon color="white" size="24">mdi-finance</v-icon>
            </div>
            <span class="text-h6 font-weight-bold text-primary">Execução Orçamentária</span>
          </div>
        </v-list-item>

        <v-list-item
          to="/"
          prepend-icon="mdi-view-dashboard-outline"
          title="Visão Geral"
          rounded="lg"
          active-color="primary"
          class="mb-1"
        ></v-list-item>

        <v-list-item
          to="/projects"
          prepend-icon="mdi-folder-outline"
          title="Lista de Projetos"
          rounded="lg"
          active-color="primary"
          class="mb-1"
        ></v-list-item>
      </v-list>

      <template v-slot:append>
        <div class="pa-4">
          <v-divider class="mb-4"></v-divider>
          <div class="d-flex align-center justify-space-between px-2">
            <span class="text-caption text-grey">Alertas</span>
            <NotificationBell />
          </div>
        </div>
      </template>
    </v-navigation-drawer>

    <v-main class="bg-background">
      <v-container fluid class="pa-8">
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import { ref } from 'vue';
import NotificationBell from '@/components/ui/NotificationBell.vue';

export default {
  name: 'App',
  components: {
    NotificationBell,
  },
  setup() {
    const drawer = ref(true);
    return { drawer };
  }
};
</script>

<style>
.v-main {
  min-height: 100vh;
}
</style>
