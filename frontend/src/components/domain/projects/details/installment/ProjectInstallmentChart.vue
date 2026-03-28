<template>
  <v-dialog max-width="1200px" persistent>
    <v-card class="rounded-lg">
      <v-card-title class="d-flex justify-space-between align-center pa-4">
        <h2 class="text-h5 text-md-h4">Visualização de Parcelas por Área</h2>
        <v-btn icon aria-label="Fechar" @click="emitClose" class="ml-2">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </v-card-title>
      <v-divider></v-divider>
      <v-card-text class="pa-4">
        <v-row>
          <v-col cols="12" class="pb-0">
            <div class="d-flex justify-space-between align-center flex-wrap">
              <div class="summary-info">
                <div><strong>Total de Parcelas:</strong> {{ installments.length }}</div>
                <div><strong>Quitadas:</strong> {{ paidInstallments.length }}</div>
                <div><strong>Pendentes:</strong> {{ pendingInstallments.length }}</div>
                <div><strong>Atrasadas:</strong> {{ lateInstallments.length }}</div>
              </div>
              <v-btn-toggle v-model="selectedView" mandatory class="mt-2 mt-sm-0" dense outlined>
                <v-btn value="paid" small>Quitadas</v-btn>
                <v-btn value="pending" small>Pendentes</v-btn>
                <v-btn value="late" small>Atrasadas</v-btn>
              </v-btn-toggle>
            </div>
          </v-col>
        </v-row>
        <v-row class="mt-2">
          <template v-if="selectedView === 'paid'">
            <v-col cols="12">
              <area-stacked-bar-chart :installments="paidInstallments" :graphTitle="paidTitle" />
            </v-col>
          </template>
          <template v-else-if="selectedView === 'pending'">
            <v-col cols="12">
              <area-stacked-bar-chart :installments="pendingInstallments" :graphTitle="pendingTitle" />
            </v-col>
          </template>
          <template v-else-if="selectedView === 'late'">
            <v-col cols="12">
              <area-stacked-bar-chart :installments="lateInstallments" :graphTitle="lateTitle" />
            </v-col>
          </template>
        </v-row>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
import { ref, computed } from 'vue';
import AreaStackedBarChart from './chart/StackedBarChart.vue';

export default {
  name: 'ChartModal',
  components: {
    AreaStackedBarChart,
  },
  props: {
    installments: {
      type: Array,
      required: true,
    },
  },
  setup(props, { emit }) {
    // Definir a visualização padrão como 'paid' (quitadas primeiro)
    const selectedView = ref('paid');

    // Filtrar parcelas por status
    const paidInstallments = computed(() =>
      props.installments.filter(installment => installment.status === 'Quitada')
    );

    const pendingInstallments = computed(() =>
      props.installments.filter(installment => installment.status === 'Pendente')
    );

    const lateInstallments = computed(() =>
      props.installments.filter(installment => installment.status === 'Atrasada')
    );

    // Títulos dos gráficos
    const paidTitle = "Distribuição de Parcelas Quitadas por Área";
    const pendingTitle = "Distribuição de Parcelas Pendentes por Área";
    const lateTitle = "Distribuição de Parcelas Atrasadas por Área";

    const emitClose = () => {
      emit('close', false)
    };

    return {
      paidInstallments,
      pendingInstallments,
      lateInstallments,
      paidTitle,
      pendingTitle,
      lateTitle,
      emitClose,
      selectedView,
    };
  },
};
</script>

<style scoped>
.text-center {
  text-align: center;
  font-size: 16px;
  color: gray;
}

.summary-info {
  display: flex;
  gap: 24px;
  flex-wrap: wrap;
  font-size: 14px;
}

@media (max-width: 599px) {
  .summary-info {
    flex-direction: column;
    gap: 8px;
  }
}
</style>