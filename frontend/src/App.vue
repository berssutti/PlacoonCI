<template>
  <v-app>
    <v-navigation-drawer
      v-model="drawer"
      permanent
      elevation="0"
      border="0"
      class="bg-surface-container-low border-none"
      width="280"
    >
      <v-list class="pa-6" bg-color="transparent">
        <v-list-item class="px-0 mb-10">
          <div class="d-flex align-center">
            <div class="rounded-xl pa-3 mr-4" style="background: linear-gradient(135deg, #004e2d 0%, #00693e 100%)">
              <v-icon color="white" size="24">mdi-finance</v-icon>
            </div>
            <span class="text-h5 font-weight-bold font-display" style="letter-spacing: -0.04em">PlacoonCI</span>
          </div>
        </v-list-item>

        <v-list-item
          to="/"
          prepend-icon="mdi-view-dashboard-outline"
          title="Visão Geral"
          rounded="md"
          active-color="primary"
          class="mb-2 py-3 px-4"
        ></v-list-item>

        <v-list-item
          to="/projects"
          prepend-icon="mdi-folder-outline"
          title="Lista de Projetos"
          rounded="md"
          active-color="primary"
          class="mb-2 py-3 px-4"
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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');

body, .v-application {
  font-family: 'Inter', sans-serif !important;
}

.text-h1, .text-h2, .text-h3, .text-h4, .text-h5, .text-h6, .font-display {
  font-family: 'Manrope', sans-serif !important;
  letter-spacing: -0.02em !important;
  color: #004e2d !important; /* Headlines deep green */
}

.text-overline, .text-caption, .text-label {
  color: #3f4941 !important; /* Labels variant */
}

.v-main {
  min-height: 100vh;
}

.bg-surface-container-low {
  background-color: #f0f4fd !important;
}

/* Glassmorphism utility */
.glass-effect {
  background: rgba(255, 255, 255, 0.8) !important;
  backdrop-filter: blur(24px);
}

/* Tonal Architecture - Remove borders globally when using certain classes */
.no-line-card {
  border: none !important;
}
</style>
