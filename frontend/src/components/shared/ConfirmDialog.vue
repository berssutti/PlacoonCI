<template>
  <v-dialog :model-value="modelValue" @update:model-value="$emit('update:modelValue', $event)" :max-width="width">
    <v-card>
      <v-card-title>{{ title }}</v-card-title>
      <v-card-text>{{ message }}</v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn :color="cancelColor" text @click="onCancel">
          {{ cancelText }}
        </v-btn>
        <v-btn :color="confirmColor" text @click="onConfirm">
          {{ confirmText }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'ConfirmDialog',
  props: {
    modelValue: {
      type: Boolean,
      required: true
    },
    title: {
      type: String,
      default: 'Confirmar'
    },
    message: {
      type: String,
      default: 'Tem certeza que deseja realizar esta ação?'
    },
    confirmText: {
      type: String,
      default: 'Confirmar'
    },
    cancelText: {
      type: String,
      default: 'Cancelar'
    },
    confirmColor: {
      type: String,
      default: 'primary'
    },
    cancelColor: {
      type: String,
      default: 'grey darken-1'
    },
    width: {
      type: [String, Number],
      default: 500
    }
  },
  emits: ['update:modelValue', 'confirm', 'cancel'],
  setup(props, { emit }) {
    const onConfirm = () => {
      emit('confirm');
      emit('update:modelValue', false);
    };

    const onCancel = () => {
      emit('cancel');
      emit('update:modelValue', false);
    };

    return {
      onConfirm,
      onCancel
    };
  }
};
</script>