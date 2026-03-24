<template>
  <v-menu v-model="menu" :close-on-content-click="false" offset-y nudge-bottom="10" min-width="350" max-width="400">
    <template v-slot:activator="{ props }">
      <v-btn icon v-bind="props" class="mr-2">
        <v-badge :content="alerts.length" :model-value="alerts.length > 0" color="error" overlap>
          <v-icon>mdi-bell</v-icon>
        </v-badge>
      </v-btn>
    </template>

    <v-card class="rounded-lg">
      <v-card-title class="d-flex align-center py-3 px-4">
        <v-icon class="mr-2">mdi-bell-outline</v-icon>
        Alertas
        <v-spacer></v-spacer>
        <v-chip v-if="alerts.length > 0" size="x-small" color="error" variant="flat">
          {{ alerts.length }} pendente(s)
        </v-chip>
      </v-card-title>
      <v-divider></v-divider>

      <v-list v-if="alerts.length > 0" class="py-0" max-height="400" style="overflow-y: auto">
        <template v-for="(alert, index) in alerts" :key="index">
          <v-list-item :prepend-icon="getAlertIcon(alert.type)" :title="alert.project_name" :subtitle="alert.message"
            @click="goToProject(alert.project_id)" class="py-3">
            <template v-slot:prepend>
              <v-icon :color="getAlertColor(alert.type)" class="mr-2">{{ getAlertIcon(alert.type) }}</v-icon>
            </template>
            <template v-slot:append>
              <v-icon size="small" color="grey">mdi-chevron-right</v-icon>
            </template>
          </v-list-item>
          <v-divider v-if="index < alerts.length - 1"></v-divider>
        </template>
      </v-list>

      <v-card-text v-else class="text-center py-6">
        <v-icon size="48" color="grey-lighten-1">mdi-bell-off-outline</v-icon>
        <div class="text-body-1 grey--text mt-2">Nenhum alerta no momento.</div>
      </v-card-text>

      <v-divider v-if="alerts.length > 0"></v-divider>
      <v-card-actions v-if="alerts.length > 0" class="pa-2">
        <v-btn block variant="text" size="small" @click="menu = false">Fechar</v-btn>
      </v-card-actions>
    </v-card>
  </v-card>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { projectService } from '@/services/projectService';

const router = useRouter();
const menu = ref(false);
const alerts = ref([]);

const fetchAlerts = async () => {
  try {
    const response = await projectService.getAlerts();
    alerts.value = response.data;
  } catch (error) {
    console.error('Erro ao buscar alertas:', error);
  }
};

const getAlertIcon = (type) => {
  switch (type) {
    case 'deadline_overdue':
      return 'mdi-alert-octagon';
    case 'deadline_near':
      return 'mdi-alert-circle';
    case 'installment_overdue':
      return 'mdi-cash-remove';
    default:
      return 'mdi-bell';
  }
};

const getAlertColor = (type) => {
  switch (type) {
    case 'deadline_overdue':
      return 'error';
    case 'deadline_near':
      return 'warning';
    case 'installment_overdue':
      return 'error';
    default:
      return 'primary';
  }
};

const goToProject = (projectId) => {
  menu.value = false;
  router.push({ name: 'ProjectDetails', params: { id: projectId } });
};

let pollingInterval = null;

onMounted(() => {
  fetchAlerts();
  // Optional: poll for alerts every 5 minutes
  pollingInterval = setInterval(fetchAlerts, 5 * 60 * 1000);
});

onUnmounted(() => {
  if (pollingInterval) {
    clearInterval(pollingInterval);
  }
});
</script>

<style scoped>
.v-list-item {
  transition: background-color 0.2s;
}

.v-list-item:hover {
  background-color: rgba(0, 0, 0, 0.05);
  cursor: pointer;
}
</style>
