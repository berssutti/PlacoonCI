<template>
    <div>
      <h4 class="mb-3"><v-icon class="mr-1">mdi-note-text-outline</v-icon>Célula Orçamentária</h4>
      <v-row>
        <v-col cols="12" md="4">
          <v-text-field
            v-model="project.nota_dotacao"
            label="Nota de Dotação"
            counter
            maxlength="100"
            clearable
            required
            :rules="[rules.required]"
          ></v-text-field>
        </v-col>
        <v-col cols="12" md="4">
          <v-text-field
            v-model="project.ptres"
            label="PTRES"
            counter
            maxlength="100"
            clearable
            required
            :rules="[rules.required]"
          ></v-text-field>
        </v-col>
        <v-col cols="12" md="4">
          <v-text-field
            v-model="project.ugr"
            label="UGR"
            counter
            maxlength="100"
            clearable
            required
            :rules="[rules.required]"
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" md="6">
          <v-text-field
            v-model="project.funding_source"
            label="Fonte de Recurso"
            counter
            maxlength="100"
            clearable
            required
            :rules="[rules.required]"
          ></v-text-field>
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field
            v-model="project.detailed_nature"
            label="Natureza Detalhada"
            counter
            maxlength="8"
            clearable
            required
            :rules="[rules.required]"
          ></v-text-field>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" md="6">
          <v-text-field
            v-model="project.internal_plan"
            label="Plano Interno"
            counter
            maxlength="100"
            clearable
            required
            :rules="[rules.required]"
          ></v-text-field>
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field
            v-model="project.internal_plan_name"
            label="Nome Plano Interno"
            counter
            maxlength="100"
            clearable
            required
            :rules="[rules.required]"
          ></v-text-field>
        </v-col>
      </v-row>
    </div>
  </template>
  
  <script setup>
  defineProps({
    project: Object,
    rules: Object,
  });
  
  defineEmits(['update:project']);
  </script>