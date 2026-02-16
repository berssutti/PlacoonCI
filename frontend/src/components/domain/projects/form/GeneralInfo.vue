<template>
  <div>
    <h4 icon="mdi-file-document-multiple-outline" class="mb-3"><v-icon
        class="mr-1">mdi-file-document-multiple-outline</v-icon>Informações Gerais</h4>
    <v-row>
      <v-col cols="12" md="6">
        <v-text-field v-model="project.name" label="Nome do Projeto" clearable counter maxlength="100"
          :rules="[rules.required, rules.maxLength(100)]" placeholder="Digite o nome do projeto"
          required></v-text-field>
      </v-col>
      <v-col cols="12" md="6">
        <v-textarea v-model="project.description" label="Descrição" :rules="[rules.required, rules.maxLength(200)]"
          placeholder="Descreva brevemente o projeto" clearable rows="1" auto-grow counter maxlength="200"
          required></v-textarea>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="6">
        <v-text-field v-model="project.processo_sei" clearable label="Processo SEI" placeholder="*****.******/****-**"
          :rules="[rules.required, rules.seiFormat]"
          @input="project.processo_sei = formatSeiProcess($event.target.value)" required></v-text-field>
      </v-col>
      <v-col cols="12" md="6">
        <v-select v-model="project.status" :items="statusOptions" label="Estado"
          @change="$emit('status-change')"></v-select>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="6">
        <v-text-field v-model="project.start_date" label="Data de Início" type="date" :rules="[rules.required]"
          required></v-text-field>
      </v-col>
      <v-col cols="12" md="6">
        <v-text-field v-model="project.end_date" label="Data de Término" type="date" :rules="[rules.required]"
          required></v-text-field>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { ref, defineProps, defineEmits, computed } from 'vue'

const props = defineProps({
  project: Object,
  rules: Object,
})

const statusOptions = ['Processando', 'Recebido']
const emit = defineEmits(['update:project', 'status-change'])

const formatSeiProcess = (value) => {
  if (!value) return value

  const cleanedValue = value.replace(/\D/g, '')

  if (cleanedValue.length <= 5) {
    return cleanedValue
  } else if (cleanedValue.length <= 11) {
    return `${cleanedValue.slice(0, 5)}.${cleanedValue.slice(5)}`
  } else if (cleanedValue.length <= 15) {
    return `${cleanedValue.slice(0, 5)}.${cleanedValue.slice(5, 11)}/${cleanedValue.slice(11, 15)}`
  } else {
    return `${cleanedValue.slice(0, 5)}.${cleanedValue.slice(5, 11)}/${cleanedValue.slice(11, 15)}-${cleanedValue.slice(15, 17)}`
  }
}

const formattedSeiProcess = computed(() => {
  return formatSeiProcess(props.project.processo_sei)
})

</script>