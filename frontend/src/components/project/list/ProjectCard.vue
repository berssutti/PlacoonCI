<template>
    <v-card class="pa-2" @click="$emit('click')" elevation="1">
      <v-card-title>{{ project.name }}</v-card-title>
      <v-card-subtitle>{{ project.description }}</v-card-subtitle>
      <v-card-text>
        <p><strong>Coordenador:</strong> {{ project.coordinator }}</p>
        <p><strong>Data de Início:</strong> {{ formatDate(project.start_date) }}</p>
        <p><strong>Data de Término:</strong> {{ formatDate(project.end_date) }}</p>
        <p><strong>Custo Indireto FCTE:</strong> {{ formatNumber(project.total_fcte_amount_expected) }}</p>
        <p><strong>Estado:</strong> {{ project.status }}</p>
      </v-card-text>
      <v-card-actions>
        <v-btn text color="primary">Ver Detalhes</v-btn>
      </v-card-actions>
    </v-card>
  </template>
  
  <script setup>
  import { defineProps, defineEmits } from 'vue';
  import { numberFormatter } from '@/utils/numberFormatter';

  const props = defineProps({
    project: {
      type: Object,
      required: true
    }
  });
  
  defineEmits(['click']);
  
  const formatNumber = (num) => numberFormatter(num);

  const formatDate = (date) => {
    if (!date) return 'N/A';
    return new Date(date).toLocaleDateString('pt-BR', {timeZone: 'UTC'});
  };
  </script>
  
  <style scoped>
  .v-card {
    cursor: pointer;
    transition: transform 0.2s ease-in-out;
  }
  .v-card:hover {
    transform: scale(1.03);
  }
  </style>