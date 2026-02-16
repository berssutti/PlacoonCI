<template>
  <div>
    <h4 class="mb-3"><v-icon class="mr-1">mdi-cash-multiple</v-icon>Orçamento</h4>
    <v-row>
      <v-col cols="12" md="6">
        <v-text-field v-model="displayUnbAmount" @input="handleUnbAmountInput" label="Custos Indiretos UnB" prefix="R$"
          :rules="[rules.required]" placeholder="Valor esperado para UnB" required></v-text-field>
      </v-col>
      <v-col cols="12" md="6">
        <v-text-field v-model="displayFcteAmount" @input="handleFcteAmountInput" label="Custos Indiretos FCTE"
          prefix="R$" :rules="[rules.required]" placeholder="Valor esperado para FCTE" required></v-text-field>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { parseCurrency } from '@/utils/currencyUtils';

const props = defineProps({
  project: Object,
  rules: Object,
});

const emit = defineEmits(['update:project']);

const displayUnbAmount = computed({
  get() {
    return props.project.total_unb_amount_expected
      ? props.project.total_unb_amount_expected.toFixed(2)
      : '';
  },
  set(newValue) {
    return newValue;
  }
});

const displayFcteAmount = computed({
  get() {
    return props.project.total_fcte_amount_expected
      ? props.project.total_fcte_amount_expected.toFixed(2)
      : '';
  },
  set(newValue) {
    return newValue;
  }
});

const handleUnbAmountInput = (event) => {
  const numericValue = parseCurrency(event.target.value);
  emit('update:project', {
    ...props.project,
    total_unb_amount_expected: numericValue
  });
};

const handleFcteAmountInput = (event) => {
  const numericValue = parseCurrency(event.target.value);
  emit('update:project', {
    ...props.project,
    total_fcte_amount_expected: numericValue
  });
};
</script>