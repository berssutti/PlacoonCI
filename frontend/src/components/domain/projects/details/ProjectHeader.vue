<template>
  <v-card-title class="d-flex flex-column">
    <h2 class="mb-2">Detalhes do Projeto</h2>
    <v-divider class="mb-3"></v-divider>
    <v-row align="center" justify="space-between">
      <v-col cols="auto" class="d-flex gap-2">
        <v-btn prepend-icon="mdi-pencil" color="primary" @click="$emit('edit')">
          Editar
        </v-btn>
        <v-btn prepend-icon="mdi-delete" color="red" class="ml-2" @click="$emit('delete')">
          Deletar
        </v-btn>
      </v-col>
      <v-col cols="auto">
        <v-btn prepend-icon="mdi-arrow-left" rounded="xl" color="grey" @click="$emit('back')">
          Voltar
        </v-btn>
      </v-col>
    </v-row>
  </v-card-title>
</template>

<script>
export default {
  name: 'ProjectHeader',
  emits: ['edit', 'delete', 'back']
};
</script>