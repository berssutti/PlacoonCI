<template>
  <h3 class="section-title">Parcelas</h3>
  <v-row align="center" justify="space-between">
    <v-col cols="auto" class="d-flex gap-2">
      <v-btn prepend-icon="mdi-plus" color="success" @click="emitAdd">
        Adicionar Parcela
      </v-btn>
      <v-btn prepend-icon="mdi-chart-bar-stacked" color="primary" @click="emitViewChart" class="ml-2">
        Visualizar Gráfico
      </v-btn>
    </v-col>
  </v-row>

  <v-list v-if="installments.length > 0">
    <v-list-group v-for="(installment, index) in installments" :key="index" v-model:opened="installment.opened">
      <template v-slot:activator="{ props }">
        <v-list-item v-bind="props" @click="toggleDetails(index)">

          <v-list-item-title :id="`installment-${installment.id}`" :class="{ 'text-error font-weight-bold': installment.status === 'Atrasada' }">
            <v-icon v-if="installment.status === 'Atrasada'" color="error" size="small" class="mr-1">mdi-alert-circle-outline</v-icon>
            Parcela {{ index + 1 }} - Estado: {{ installment.status }} - R$ {{ formatNumber(installment.amount) }}
          </v-list-item-title>

          <v-list-item-action>
            <v-btn @click="emitEdit(installment)" color="primary" size="small">Editar</v-btn>
            <v-btn class="ml-2" @click="emitDelete(installment.id)" color="red" size="small">Deletar</v-btn>
          </v-list-item-action>
        </v-list-item>
      </template>
      <v-list-item v-if="expandedIndex === index">

        <v-list-item-subtitle>
          <strong>Data Estimada:</strong> {{ formatDate(installment.estimated_date) }}
        </v-list-item-subtitle>
        <v-list-item-subtitle v-if="installment.status === 'Quitada'">
          <strong>Data Efetiva:</strong> {{ formatDate(installment.effective_date) || 'N/A' }}
        </v-list-item-subtitle>
        <v-list-item-subtitle>
          <strong>Observação:</strong> {{ installment.observation || 'N/A' }}
        </v-list-item-subtitle>
        <v-list-item-subtitle>
          <strong>Destino:</strong> {{ installment.destination || 'N/A' }}
        </v-list-item-subtitle>

      </v-list-item>
    </v-list-group>
  </v-list>

  <v-row v-else>
    <v-col cols="12">
      <v-alert type="info" :value="true">
        Nenhuma parcela cadastrada.
      </v-alert>
    </v-col>
  </v-row>
</template>

<script>
import { ref, defineComponent, toRefs, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { dateFormatter } from '@/utils/dateFormatter';
import { numberFormatter } from '@/utils/numberFormatter';

export default defineComponent({
  name: 'InstallmentList',
  props: {
    installments: {
      type: Array,
      required: true,
      default: () => [],
    },
  },
  emits: ['add', 'edit', 'delete', 'chart'],
  setup(props, { emit }) {
    const { installments } = toRefs(props);
    const route = useRoute();

    const formatDate = (date) => dateFormatter(date);
    const formatNumber = (num) => numberFormatter(num);

    const expandedIndex = ref(null);

    const emitAdd = () => emit('add');
    const emitViewChart = () => emit('chart');
    const emitEdit = (installment) => emit('edit', installment);
    const emitDelete = (id) => emit('delete', id);

    const toggleDetails = (index) => expandedIndex.value = index;

    const highlightInstallment = () => {
      const highlightId = route.query.highlight_installment;
      if (highlightId && installments.value.length > 0) {
        const index = installments.value.findIndex(i => String(i.id) === String(highlightId));
        if (index !== -1) {
          expandedIndex.value = index;
          // Smooth scroll to the element
          setTimeout(() => {
            const element = document.getElementById(`installment-${highlightId}`);
            if (element) {
              element.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
          }, 500);
        }
      }
    };

    onMounted(highlightInstallment);
    watch(() => installments.value, highlightInstallment);

    return {
      installments,
      formatDate,
      formatNumber,
      expandedIndex,
      emitAdd,
      emitViewChart,
      toggleDetails,
      emitEdit,
      emitDelete,
    };
  },
});
</script>

<style scoped>
.section-title {
  font-size: 1.1em;
  font-weight: bold;
  margin-top: 16px;
  margin-bottom: 8px;
  border-bottom: 2px solid #eeeeee;
  padding-bottom: 4px;
}
</style>
