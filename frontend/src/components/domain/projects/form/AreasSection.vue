<template>
  <div>
    <h4 class="mb-3"><v-icon class="mr-1">mdi-shape-outline</v-icon>Áreas</h4>
    <v-row v-for="(area, index) in areas" :key="index">
      <v-col cols="6">
        <v-select v-model="area.id" :items="filteredAreaList(index)" item-title="name" item-value="id" label="Área"
          :rules="[rules.required]" required></v-select>
      </v-col>
      <v-col cols="4">
        <v-text-field v-model.number="area.percentage" label="Porcentagem" type="number" suffix="%"
          :rules="[rules.required, rules.percentage]" required></v-text-field>
      </v-col>
      <v-col cols="2" class="text-center">
        <v-btn icon aria-label="Remover Área" color="red" @click="$emit('remove-area', index)">
          <v-icon>mdi-delete</v-icon>
        </v-btn>
      </v-col>
    </v-row>
    <v-btn color="success" @click="$emit('add-area')" class="mb-4" prepend-icon="mdi-plus">
      Adicionar Área
    </v-btn>
  </div>
</template>

<script setup>
const props = defineProps({
  areas: Array,
  areaList: Array,
  rules: Object,
});

const emit = defineEmits(['update:areas', 'add-area', 'remove-area']);

const filteredAreaList = (index) => {
  const selectedAreas = props.areas
    .map((a, i) => (i !== index ? a.id : null))
    .filter((id) => id);
  return props.areaList.filter((area) => !selectedAreas.includes(area.id));
};
</script>