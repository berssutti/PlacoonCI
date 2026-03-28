<template>
  <v-card class="project-card pa-6 bg-surface-container-lowest no-line-card" @click="$emit('click')">
    <v-card-item class="pa-0 mb-6">
      <template v-slot:prepend>
        <v-avatar color="surface-container-low" rounded="xl" size="56" class="mr-4">
          <v-icon color="primary" size="28">mdi-folder-outline</v-icon>
        </v-avatar>
      </template>
      <v-card-title class="text-h6 font-weight-bold mb-n1">
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

    <v-card-text class="pa-0">
      <div class="mb-6">
        <div class="text-overline font-weight-bold mb-1">COORDINATOR</div>
        <div class="text-body-1 font-weight-medium text-on-surface">{{ project.coordinator }}</div>
      </div>

      <v-row no-gutters class="mb-8">
        <v-col cols="6">
          <div class="text-overline font-weight-bold mb-1">START DATE</div>
          <div class="text-body-1 text-on-surface">{{ formatDate(project.start_date) }}</div>
        </v-col>
        <v-col cols="6">
          <div class="text-overline font-weight-bold mb-1">END DATE</div>
          <div class="text-body-1 text-on-surface">{{ formatDate(project.end_date) }}</div>
        </v-col>
      </v-row>

      <div class="d-flex align-center justify-space-between mt-6 pt-6" style="border-top: 2px solid #f0f4fd">
        <v-chip
          :color="getStatusColor(projectStatus)"
          variant="flat"
          size="small"
          class="font-weight-bold px-4"
          style="background-color: #d4e3ff !important; color: #001c3a !important"
        >
          {{ projectStatus }}
        </v-chip>
        <div class="text-h6 font-weight-black text-primary">
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