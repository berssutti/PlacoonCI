<template>
  <v-card elevation="2" class="rounded-lg h-100 project-card" @click="$emit('click')">
    <v-card-title class="text-h6 d-flex align-center">
      <v-icon class="mr-2">mdi-file-document-outline</v-icon>
      <span class="text-truncate">{{ project.name }}</span>
      <v-spacer></v-spacer>
      <v-tooltip v-if="project.has_alerts" text="Este projeto possui alertas">
        <template v-slot:activator="{ props }">
          <v-icon v-bind="props" color="error" class="ml-2">mdi-alert-circle</v-icon>
        </template>
      </v-tooltip>
    </v-card-title>
    <v-card-subtitle>
      Processo SEI: {{ project.processo_sei }}
    </v-card-subtitle>
    <v-card-text>
      <v-row no-gutters>
        <v-col cols="12" class="mb-2">
          <div class="caption text-uppercase font-weight-bold text-grey">Coordenador</div>
          <div>{{ project.coordinator }}</div>
        </v-col>
      </v-row>
      <v-row no-gutters>
        <v-col cols="6" class="mb-2">
          <div class="caption text-uppercase font-weight-bold text-grey">Início</div>
          <div>{{ formatDate(project.start_date) }}</div>
        </v-col>
        <v-col cols="6" class="mb-2">
          <div class="caption text-uppercase font-weight-bold text-grey">Término</div>
          <div>{{ formatDate(project.end_date) }}</div>
        </v-col>
      </v-row>
      <v-row no-gutters>
        <v-col cols="12">
          <div class="caption text-uppercase font-weight-bold text-grey mb-1">Situação do Projeto</div>
          <v-chip :color="getStatusColor(projectStatus)" text-color="white" small class="px-2">
            <v-icon small left>{{ getStatusIcon(projectStatus) }}</v-icon>
            {{ projectStatus }}
          </v-chip>
          <div class="mt-2 text-caption">
            {{ remainingTime }}
          </div>
        </v-col>
      </v-row>

      <v-divider class="my-3"></v-divider>

      <v-row no-gutters>
        <v-col cols="12">
          <div class="caption text-uppercase font-weight-bold text-grey mb-2">Informações de Custo</div>
          <v-row no-gutters>
            <v-col cols="6" class="mb-2">
              <div class="text-caption text-grey">Valor Total</div>
              <div class="font-weight-medium">{{ formatCurrency(project.total_fcte_amount_expected) }}</div>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn color="primary" text @click.stop="$emit('click')">
        Ver Detalhes
        <v-icon right>mdi-arrow-right</v-icon>
      </v-btn>
    </v-card-actions>
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