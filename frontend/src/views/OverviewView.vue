<template>
    <v-container>
      <v-row>
        <v-col cols="12">
          <h1 class="text-h4 mb-4">Visão Geral</h1>
        </v-col>
      </v-row>
  
      <!-- Gráficos -->
      <v-row>
        <v-col cols="12" md="6">
          <pie-chart
            :areas-summary="areasSummary"
            graph-title="Distribuição do Orçamento por Área"
          />
        </v-col>
        <v-col cols="12" md="6">
          <line-chart
            :installments="allInstallments"
            graph-title="Evolução do Orçamento Executado"
          />
        </v-col>
      </v-row>
  
      <v-row>
        <v-col cols="12" md="6">
          <doughnut-chart
            :areas-summary="areasSummary"
            graph-title="Orçamento Executado por Área"
          />
        </v-col>
        <v-col cols="12" md="6">
          <bar-chart
            :installments="allInstallments"
            graph-title="Status dos Projetos"
          />
        </v-col>
      </v-row>
  
      <!-- Resumo Financeiro -->
      <v-row>
        <v-col cols="12">
          <v-card>
            <v-card-title class="text-h6">Resumo Financeiro</v-card-title>
            <v-card-text>
              <v-simple-table>
                <template v-slot:default>
                  <thead>
                    <tr>
                      <th>Área</th>
                      <th>Valor Alocado (R$)</th>
                      <th>Valor Executado (R$)</th>
                      <th>Saldo (R$)</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="area in areasSummary" :key="area.name">
                      <td>{{ area.name }}</td>
                      <td>{{ formatCurrency(area.allocated) }}</td>
                      <td>{{ formatCurrency(area.executed) }}</td>
                      <td>{{ formatCurrency(area.balance) }}</td>
                    </tr>
                  </tbody>
                </template>
              </v-simple-table>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script>
  import { ref, onMounted } from "vue";
  import { useProject } from "@/composables/useProject";
  import { useInstallments } from "@/composables/useInstallments";
  import BarChart from "@/components/shared/charts/BarChart.vue";
  import PieChart from "@/components/shared/charts/PieChart.vue";
  import LineChart from "@/components/shared/charts/LineChart.vue";
  import DoughnutChart from "@/components/shared/charts/DoughnutChart.vue";
  
  export default {
    name: "OverviewView",
    components: {
      BarChart,
      PieChart,
      LineChart,
      DoughnutChart,
    },
    setup() {
      const { project, fetchProject } = useProject();
      const { installments, fetchInstallments } = useInstallments();
      const allInstallments = ref([]);
      const areasSummary = ref([]);
  
      const formatCurrency = (value) => {
        return new Intl.NumberFormat("pt-BR", {
          style: "currency",
          currency: "BRL",
        }).format(value);
      };
  
      onMounted(async () => {
        await fetchProject();
        const allInstallmentsData = [];
  
        if (project.value && project.value.length > 0) {
          for (const proj of project.value) {
            await fetchInstallments(proj.id);
            if (installments.value && installments.value.length > 0) {
              allInstallmentsData.push(...installments.value);
            }
          }
        }
  
        allInstallments.value = allInstallmentsData;
        calculateAreasSummary();
      });
  
      const calculateAreasSummary = () => {
        const summary = {};
  
        allInstallments.value.forEach((installment) => {
          Object.entries(installment.area_values || {}).forEach(([area, value]) => {
            if (!summary[area]) {
              summary[area] = {
                name: area,
                allocated: 0,
                executed: 0,
                balance: 0,
              };
            }
  
            summary[area].allocated += value;
            if (installment.effective_date) {
              summary[area].executed += value;
            }
          });
        });
  
        Object.values(summary).forEach((area) => {
          area.balance = area.allocated - area.executed;
        });
  
        areasSummary.value = Object.values(summary);
      };
  
      return {
        allInstallments,
        areasSummary,
        formatCurrency,
      };
    },
  };
  </script>
  
  <style scoped>
  .v-card {
    margin-bottom: 20px;
  }
  </style>