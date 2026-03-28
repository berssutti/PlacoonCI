<template>
  <v-row no-gutters class="align-center">
    <v-col cols="12" md="8" class="pr-md-4">
      <v-text-field
        v-model="searchQuery"
        label="Buscar projetos"
        placeholder="Nome do projeto, coordenador ou SEI..."
        prepend-inner-icon="mdi-magnify"
        hide-details
        clearable
        @update:model-value="emitFilters"
      ></v-text-field>
    </v-col>
    <v-col cols="12" md="4" class="mt-4 mt-md-0">
      <v-select
        v-model="selectedYear"
        :items="years"
        label="Ano"
        prepend-inner-icon="mdi-calendar"
        hide-details
        @update:model-value="emitFilters"
      ></v-select>
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