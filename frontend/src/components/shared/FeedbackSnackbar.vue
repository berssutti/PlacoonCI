<template>
  <v-snackbar :model-value="modelValue" @update:model-value="$emit('update:modelValue', $event)" :color="color"
    :timeout="timeout" :position="position">
    {{ message }}
    <template v-slot:action="{ attrs }">
      <v-btn v-if="showCloseButton" text v-bind="attrs" @click="onClose">
        {{ closeText }}
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script>
export default {
  name: 'FeedbackSnackbar',
  props: {
    modelValue: {
      type: Boolean,
      required: true
    },
    message: {
      type: String,
      required: true
    },
    color: {
      type: String,
      default: 'success'
    },
    timeout: {
      type: Number,
      default: 3000
    },
    position: {
      type: String,
      default: 'bottom'
    },
    showCloseButton: {
      type: Boolean,
      default: true
    },
    closeText: {
      type: String,
      default: 'Fechar'
    }
  },
  emits: ['update:modelValue', 'close'],
  setup(props, { emit }) {
    const onClose = () => {
      emit('update:modelValue', false);
      emit('close');
    };

    return {
      onClose
    };
  }
};
</script>