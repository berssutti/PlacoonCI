<template>
  <v-dialog :model-value="modelValue" @update:model-value="updateModelValue" max-width="500px">
    <v-card class="rounded-lg">
      <v-card-title>
        <span class="headline">{{ isEditing ? 'Editar Parcela' : 'Adicionar Parcela' }}</span>
      </v-card-title>
      <v-card-text>
        <v-form ref="form" v-model="valid">
          <v-text-field
            v-model="displayAmount"
            @input="handleAmountInput"
            label="Valor"
            :rules="[v => !!v || 'Campo obrigatório']"
            prefix="R$"
          />
          <v-text-field
            v-model="localInstallment.estimated_date"
            label="Data Estimada"
            :rules="[v => !!v || 'Campo obrigatório']"
            type="date"
          />
          <v-textarea
            v-model="localInstallment.observation"
            label="Observação"
            rows="1"
            counter
            auto-grow
            maxlength="200"
          />
          <v-textarea
            v-model="localInstallment.destination"
            label="Destino"
            rows="1"
            auto-grow
            counter
            maxlength="200"
          />

          <v-select
            v-model="localInstallment.status"
            :items="statusOptions"
            label="Estado"
            :rules="[v => !!v || 'Campo obrigatório']"
          />

          <v-text-field
            v-if="localInstallment.status === 'Quitada'"
            v-model="localInstallment.effective_date"
            label="Data Efetiva"
            :rules="[v => !!v || 'Campo obrigatório']"
            type="date"
          />
        </v-form>
      </v-card-text>

      <v-card-actions>
        <v-btn color="grey" @click="cancel">Cancelar</v-btn>
        <v-btn color="primary" :disabled="!valid" @click="save">Salvar</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import { ref, watch, reactive, computed } from 'vue';
import { parseCurrency } from '@/utils/currencyUtils';

export default {
  name: 'InstallmentForm',
  props: {
    modelValue: {
      type: Boolean,
      required: true,
    },
    installment: {
      type: Object,
      required: true,
    },
    isEditing: {
      type: Boolean,
      required: true,
    },
  },
  emits: ['update:modelValue', 'save', 'close'],
  setup(props, { emit }) {
    const form = ref(null);
    const valid = ref(false);
    const statusOptions = ref(['Atrasada', 'Quitada', 'Pendente']);
    const localInstallment = reactive({ ...props.installment });

    const displayAmount = computed({
      get() {
        return localInstallment.amount ? localInstallment.amount.toFixed(2)  : '';
      },
      set(newValue) {
        return newValue;
      }
    });

    const handleAmountInput = (event) => {
      localInstallment.amount = parseCurrency(event.target.value);
    };

    const updateModelValue = (value) => {
      emit('update:modelValue', value);
    };

    const cancel = () => {
      props.installment ? Object.assign(localInstallment, props.installment) : Object.assign(localInstallment, {});
      form.value?.resetValidation();
      emit('close');
    };

    const save = () => {
      if (valid.value) {
        emit('save', { ...localInstallment });
      }
    };

    watch(
      () => props.installment,
      (newInstallment) => {
        Object.assign(localInstallment, newInstallment);
      },
      { immediate: true, deep: true }
    );

    return {
      form,
      valid,
      localInstallment,
      displayAmount,
      handleAmountInput,
      updateModelValue,
      cancel,
      save,
      statusOptions,
    };
  },
};
</script>