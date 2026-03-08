<template>
  <div>
    <h4 class="mb-3"><v-icon class="mr-1">mdi-account-tie</v-icon>Gestão</h4>
    <v-row>
      <v-col cols="12" md="4">
        <v-text-field v-model="project.coordinator" label="Coordenador" :rules="[rules.required, rules.maxLength(100)]"
          placeholder="Nome do coordenador" counter maxlength="100" required></v-text-field>
      </v-col>
      <v-col cols="12" md="4">
        <v-text-field v-model="project.substitute_coordinator" label="Coordenador Substituto"
          :rules="[rules.required, rules.maxLength(100)]" placeholder="Nome do coordenador substituto" counter
          maxlength="100" required></v-text-field>
      </v-col>
      <v-col cols="12" md="4">
        <v-text-field v-model="project.academic_supervisor" label="Supervisor Acadêmico"
          :rules="[rules.required, rules.maxLength(100)]" placeholder="Nome do supervisor acadêmico" counter
          maxlength="100" required></v-text-field>
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