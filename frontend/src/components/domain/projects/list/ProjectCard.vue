<template>
  <v-card class="project-card pa-2" @click="$emit('click')">
    <v-card-item>
      <template v-slot:prepend>
        <v-avatar color="indigo-lighten-5" rounded="lg" class="mr-3">
          <v-icon color="primary">mdi-folder-outline</v-icon>
        </v-avatar>
      </template>
      <v-card-title class="text-subtitle-1 font-weight-bold">
        <span class="text-truncate d-inline-block" style="max-width: 200px;">{{ project.name }}</span>
      </v-card-title>
      <v-card-subtitle class="text-caption">
        SEI: {{ project.processo_sei }}
      </v-card-subtitle>
      <template v-slot:append>
        <v-tooltip v-if="project.has_alerts" text="Este projeto possui alertas">
          <template v-slot:activator="{ props }">
            <v-icon v-bind="props" color="error" size="small">mdi-alert-circle</v-icon>
          </template>
        </v-tooltip>
      </template>
    </v-card-item>

    <v-card-text class="pt-2">
      <div class="mb-4">
        <div class="text-caption text-grey font-weight-bold text-uppercase mb-1">Coordenador</div>
        <div class="text-body-2 font-weight-medium">{{ project.coordinator }}</div>
      </div>

      <v-row no-gutters class="mb-4">
        <v-col cols="6">
          <div class="text-caption text-grey font-weight-bold text-uppercase mb-1">Início</div>
          <div class="text-body-2">{{ formatDate(project.start_date) }}</div>
        </v-col>
        <v-col cols="6">
          <div class="text-caption text-grey font-weight-bold text-uppercase mb-1">Término</div>
          <div class="text-body-2">{{ formatDate(project.end_date) }}</div>
        </v-col>
      </v-row>

      <div class="d-flex align-center justify-space-between mt-auto pt-4 border-t">
        <v-chip
          :color="getStatusColor(projectStatus)"
          variant="tonal"
          size="small"
          class="font-weight-bold"
        >
          {{ projectStatus }}
        </v-chip>
        <div class="text-subtitle-2 font-weight-bold text-primary">
          {{ formatCurrency(project.total_fcte_amount_expected) }}
        </div>
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { computed } from 'vue';
import { useProjectStatus } from '@/composables/useProjectStatus';
import { formatCurrency } from '@/utils/currencyUtils';
import { dateFormatter } from '@/utils/dateFormatter';

const props = defineProps({
  project: {
    type: Object,
    required: true
  },
});

defineEmits(['click']);

const { getProjectStatus, getStatusColor, getStatusIcon, getRemainingTime } = useProjectStatus();

const formatDate = (date) => dateFormatter(date);

const projectStatus = computed(() => getProjectStatus(props.project));
const remainingTime = computed(() => getRemainingTime(props.project));
</script>

<style scoped>
.project-card {
  transition: transform 0.2s ease-in-out;
  cursor: pointer;
}

.project-card:hover {
  transform: translateY(-4px);
}
</style>