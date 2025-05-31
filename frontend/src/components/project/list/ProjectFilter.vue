<template>
  <v-row class="mb-4">
    <v-col cols="12" md="6">
      <v-text-field v-model="searchQuery" label="Buscar projeto por palavra-chave" placeholder="Digite para buscar..."
        clearable dense @update:model-value="emitFilters"></v-text-field>
    </v-col>
    <v-col cols="12" md="6">
      <v-select v-model="selectedYear" :items="years" label="Filtrar por ano" placeholder="Selecione o ano" dense
        @update:model-value="emitFilters"></v-select>
    </v-col>
  </v-row>
</template>

<script setup>
import { ref, defineProps, defineEmits, onMounted } from 'vue';

const props = defineProps({
  years: {
    type: Array,
    required: true
  },
  initialFilters: {
    type: Object,
    default: () => ({
      searchQuery: '',
      selectedYear: new Date().getFullYear()
    })
  }
});

const emit = defineEmits(['update:filters']);

const searchQuery = ref(props.initialFilters.searchQuery);
const selectedYear = ref(props.initialFilters.selectedYear);

const emitFilters = () => {
  emit('update:filters', {
    searchQuery: searchQuery.value,
    selectedYear: selectedYear.value
  });
};

onMounted(() => {
  emitFilters();
});
</script>