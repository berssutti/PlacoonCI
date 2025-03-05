<template>
  <v-dialog max-width="1200px" persistent>
    <v-card class="rounded-lg">
      <v-card-title class="d-flex justify-space-between align-center pa-4">
        <h2 class="text-h5 text-md-h4">Visualização de Parcelas por Área</h2>
        <v-btn icon @click="emitClose" class="ml-2">
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
                <div><strong>Pendentes:</strong> {{ pendingInstallments.length }}</div>
                <div><strong>Quitadas:</strong> {{ paidInstallments.length }}</div>
              </div>
              
              <v-btn-toggle
                v-model="selectedView"
                mandatory
                class="mt-2 mt-sm-0"
                dense
                outlined
              >
                <v-btn value="both" small>Ambos</v-btn>
                <v-btn value="pending" small>Apenas Pendentes</v-btn>
                <v-btn value="paid" small>Apenas Quitadas</v-btn>
              </v-btn-toggle>
            </div>
          </v-col>
        </v-row>
        
        <v-row class="mt-2">
          <template v-if="selectedView === 'both'">
            <v-col cols="12" md="6">
              <div v-if="pendingInstallments.length > 0">
                <stacked-bar-chart :installments="pendingInstallments" :graphTitle="pendingTitle"/>
              </div>
              <v-card v-else class="pa-6 d-flex justify-center align-center" height="450">
                <div class="text-center">
                  <v-icon large color="grey lighten-1">mdi-chart-bar</v-icon>
                  <p class="text-subtitle-1 mt-2 grey--text">Não há parcelas pendentes para exibir</p>
                </div>
              </v-card>
            </v-col>
            <v-col cols="12" md="6">
              <div v-if="paidInstallments.length > 0">
                <stacked-bar-chart :installments="paidInstallments" :graphTitle="paidTitle"/>
              </div>
              <v-card v-else class="pa-6 d-flex justify-center align-center" height="450">
                <div class="text-center">
                  <v-icon large color="grey lighten-1">mdi-chart-bar</v-icon>
                  <p class="text-subtitle-1 mt-2 grey--text">Não há parcelas quitadas para exibir</p>
                </div>
              </v-card>
            </v-col>
          </template>
          
          <template v-else-if="selectedView === 'pending'">
            <v-col cols="12">
              <div v-if="pendingInstallments.length > 0">
                <stacked-bar-chart :installments="pendingInstallments" :graphTitle="pendingTitle"/>
              </div>
              <v-card v-else class="pa-6 d-flex justify-center align-center" height="450">
                <div class="text-center">
                  <v-icon large color="grey lighten-1">mdi-chart-bar</v-icon>
                  <p class="text-subtitle-1 mt-2 grey--text">Não há parcelas pendentes para exibir</p>
                </div>
              </v-card>
            </v-col>
          </template>
          
          <template v-else-if="selectedView === 'paid'">
            <v-col cols="12">
              <div v-if="paidInstallments.length > 0">
                <stacked-bar-chart :installments="paidInstallments" :graphTitle="paidTitle"/>
              </div>
              <v-card v-else class="pa-6 d-flex justify-center align-center" height="450">
                <div class="text-center">
                  <v-icon large color="grey lighten-1">mdi-chart-bar</v-icon>
                  <p class="text-subtitle-1 mt-2 grey--text">Não há parcelas quitadas para exibir</p>
                </div>
              </v-card>
            </v-col>
          </template>
        </v-row>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
import { ref } from 'vue';
import StackedBarChart from '@/components/shared/charts/BarChart.vue';

export default {
  name: 'ChartModal',

  components: {
    StackedBarChart,
  },

  props: {
    installments: {
      type: Array,
      required: true,
    },
  },

  setup(props, { emit }) {
    const selectedView = ref('both');
    
    const pendingInstallments = props.installments.filter(installment => installment.status == 'Pendente');
    const paidInstallments = props.installments.filter(installment => installment.status == 'Quitada');

    const pendingTitle = "Distribuição de Parcelas Pendentes por Área";
    const paidTitle = "Distribuição de Parcelas Quitadas por Área";

    const emitClose = () => {
      emit('close', false)
    };

    return {
      pendingInstallments,
      paidInstallments,
      pendingTitle,
      paidTitle,
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