<template>
  <v-menu v-model="menu" :close-on-content-click="false" offset-y nudge-bottom="10" min-width="350" max-width="450">
    <template v-slot:activator="{ props }">
      <v-btn icon v-bind="props" class="mr-2">
        <v-badge :content="visibleAlerts.length" :model-value="visibleAlerts.length > 0" color="error" overlap>
          <v-icon>mdi-bell</v-icon>
        </v-badge>
      </v-btn>
    </template>

    <v-card class="rounded-lg">
      <v-card-title class="d-flex align-center py-3 px-4">
        <v-icon class="mr-2">mdi-bell-outline</v-icon>
        Alertas
        <v-spacer></v-spacer>
        <v-chip v-if="visibleAlerts.length > 0" size="x-small" color="error" variant="flat">
          {{ visibleAlerts.length }} pendente(s)
        </v-chip>
      </v-card-title>
      <v-divider></v-divider>

      <v-list v-if="visibleAlerts.length > 0" class="py-0" max-height="400" style="overflow-y: auto">
        <template v-for="(alert, index) in visibleAlerts" :key="alert.id">
          <v-tooltip location="bottom" open-delay="500">
            <template v-slot:activator="{ props }">
              <v-list-item v-bind="props" :prepend-icon="getAlertIcon(alert.type)" :title="alert.project_name"
                :subtitle="alert.message" @click="goToProject(alert)" class="py-3 pr-2">
                <template v-slot:prepend>
                  <v-icon :color="getAlertColor(alert.type)" class="mr-2">{{ getAlertIcon(alert.type) }}</v-icon>
                </template>
                <template v-slot:append>
                  <div class="d-flex align-center">
                    <v-btn icon="mdi-close" size="x-small" variant="text" color="grey" @click.stop="dismissAlert(alert.id)"
                      class="ml-2"></v-btn>
                    <v-icon size="small" color="grey" class="ml-1">mdi-chevron-right</v-icon>
                  </div>
                </template>
              </v-list-item>
            </template>
            <span>{{ alert.message }}</span>
          </v-tooltip>
          <v-divider v-if="index < visibleAlerts.length - 1"></v-divider>
        </template>
      </v-list>

      <v-card-text v-else class="text-center py-6">
        <v-icon size="48" color="grey-lighten-1">mdi-bell-off-outline</v-icon>
        <div class="text-body-1 grey--text mt-2">Nenhum alerta no momento.</div>
      </v-card-text>

      <v-divider v-if="visibleAlerts.length > 0 || dismissedAlerts.size > 0"></v-divider>
      <v-card-actions v-if="visibleAlerts.length > 0 || dismissedAlerts.size > 0" class="pa-2 d-flex flex-column">
        <v-btn v-if="dismissedAlerts.size > 0" block variant="text" size="x-small" color="primary" @click="resetDismissed"
          class="mb-1">
          Restaurar alertas removidos
        </v-btn>
        <v-btn block variant="tonal" size="small" @click="menu = false">Fechar</v-btn>
      </v-card-actions>
    </v-card>
  </v-menu>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { projectService } from '@/services/projectService';

const router = useRouter();
const menu = ref(false);
const alerts = ref([]);
const dismissedAlerts = ref(new Set());

const STORAGE_KEY = 'dismissed_alerts';

const loadDismissed = () => {
  const saved = localStorage.getItem(STORAGE_KEY);
  if (saved) {
    try {
      dismissedAlerts.value = new Set(JSON.parse(saved));
    } catch (e) {
      console.error('Error loading dismissed alerts', e);
    }
  }
};

const saveDismissed = () => {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(Array.from(dismissedAlerts.value)));
};

const dismissAlert = (alertId) => {
  dismissedAlerts.value.add(alertId);
  saveDismissed();
};

const resetDismissed = () => {
  dismissedAlerts.value.clear();
  saveDismissed();
};

const visibleAlerts = computed(() => {
  return alerts.value.filter(a => !dismissedAlerts.value.has(a.id));
});

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

const goToProject = (alert) => {
  menu.value = false;
  const query = {};
  if (alert.installment_id) {
    query.highlight_installment = alert.installment_id;
  }
  router.push({
    name: 'ProjectDetails',
    params: { id: alert.project_id },
    query
  });
};

let pollingInterval = null;

onMounted(() => {
  loadDismissed();
  fetchAlerts();
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
