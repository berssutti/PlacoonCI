<template>
  <v-card 
    elevation="2" 
    class="rounded-lg h-100 project-card" 
    @click="$emit('click')"
  >
    <v-card-title class="text-h6">
      <v-icon class="mr-2">mdi-file-document-outline</v-icon>
      {{ project.name }}
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
          <v-chip
            :color="getStatusColor"
            text-color="white"
            small
            class="px-2"
          >
            <v-icon small left>{{ getStatusIcon }}</v-icon>
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
      <v-btn 
        color="primary" 
        text 
        @click.stop="$emit('click')"
      >
        Ver Detalhes
        <v-icon right>mdi-arrow-right</v-icon>
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  project: {
    type: Object,
    required: true
  },
});

defineEmits(['click']);

const formatDate = (dateString) => {
  const options = { day: '2-digit', month: '2-digit', year: 'numeric' };
  return new Date(dateString + 'T00:00:00').toLocaleDateString('pt-BR', options);
};

const formatCurrency = (value) => {
  if (!value) return 'R$ 0,00';
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(value);
};

const projectStatus = computed(() => {
  const start = new Date(props.project.start_date);
  const end = new Date(props.project.end_date);
  const today = new Date();
  
  if (today < start) return "Não Iniciado";
  if (today > end) return "Concluído";
  return "Em Andamento";
});

const getStatusColor = computed(() => {
  if (projectStatus.value === "Não Iniciado") return "grey";
  if (projectStatus.value === "Em Andamento") return "primary";
  return "success";
});

const getStatusIcon = computed(() => {
  if (projectStatus.value === "Não Iniciado") return "mdi-clock-outline";
  if (projectStatus.value === "Em Andamento") return "mdi-progress-clock";
  return "mdi-check-circle-outline";
});

const remainingTime = computed(() => {
  const start = new Date(props.project.start_date);
  const end = new Date(props.project.end_date);
  const today = new Date();
  
  if (today < start) {
    const daysToStart = Math.ceil((start - today) / (1000 * 60 * 60 * 24));
    return `Inicia em ${daysToStart} dia${daysToStart !== 1 ? 's' : ''}`;
  }
  
  if (today > end) {
    const daysAfterEnd = Math.ceil((today - end) / (1000 * 60 * 60 * 24));
    return `Finalizado há ${daysAfterEnd} dia${daysAfterEnd !== 1 ? 's' : ''}`;
  }
  
  const daysRemaining = Math.ceil((end - today) / (1000 * 60 * 60 * 24));
  return `${daysRemaining} dia${daysRemaining !== 1 ? 's' : ''} restante${daysRemaining !== 1 ? 's' : ''}`;
});
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