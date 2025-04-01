<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card elevation="2" class="rounded-lg">
          <v-card-title class="text-h4 primary--text py-4 px-6">
            <v-icon large class="mr-2">mdi-chart-donut</v-icon>
            Visão Geral dos Ressarcimentos
          </v-card-title>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mt-4">
      <v-col cols="12" md="3">
        <v-card elevation="2" class="rounded-lg h-100" color="primary" dark>
          <v-card-text class="text-center d-flex flex-column justify-center h-100">
            <div class="text-h6 mb-2">Ressarcimento Total Esperado</div>
            <div class="text-h4">{{ formatCurrency(totalBudget) }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="3">
        <v-card elevation="2" class="rounded-lg h-100" color="success" dark>
          <v-card-text class="text-center d-flex flex-column justify-center h-100">
            <div class="text-h6 mb-2">Ressarcimento Executado</div>
            <div class="text-h4">{{ formatCurrency(totalExecuted) }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="3">
        <v-card elevation="2" class="rounded-lg h-100" color="warning" dark>
          <v-card-text class="text-center d-flex flex-column justify-center h-100">
            <div class="text-h6 mb-2">Ressarcimento Pendente</div>
            <div class="text-h4">{{ formatCurrency(totalPending) }}</div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="3">
        <v-card elevation="2" class="rounded-lg h-100" color="error" dark>
          <v-card-text class="text-center d-flex flex-column justify-center h-100">
            <div class="text-h6 mb-2">Ressarcimento Atrasado</div>
            <div class="text-h4">{{ formatCurrency(totalOverdue) }}</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Gráficos -->
    <v-row class="mt-4">
      <v-col cols="12">
        <v-card elevation="2" class="rounded-lg">
          <v-card-title class="text-h6">
            <v-icon class="mr-2">{{ getSelectedGraphIcon }}</v-icon>
            {{ getSelectedGraphTitle }}
          </v-card-title>
          <v-card-subtitle class="pb-0">{{ getSelectedGraphSubtitle }}</v-card-subtitle>
          <v-card-text>
            <v-row>
              <v-col cols="12" class="d-flex justify-center mb-4">
                <v-btn-group>
                  <v-btn
                    v-for="graph in graphs"
                    :key="graph.id"
                    :color="selectedGraph === graph.id ? 'primary' : ''"
                    @click="selectedGraph = graph.id"
                  >
                    <v-icon left>{{ graph.icon }}</v-icon>
                    {{ graph.name }}
                  </v-btn>
                </v-btn-group>
              </v-col>
              <v-col cols="12">
                <component
                  :is="getSelectedGraphComponent"
                  v-bind="getSelectedGraphProps"
                  :height="400"
                />
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Resumo Financeiro -->
    <v-row class="mt-4">
      <v-col cols="12">
        <v-card elevation="2" class="rounded-lg">
          <v-card-title class="text-h6">
            <v-icon class="mr-2">mdi-table</v-icon>
            Resumo Financeiro
          </v-card-title>
          <v-card-text>
            <v-data-table
              :headers="headers"
              :items="areasSummary"
              :items-per-page="5"
              class="elevation-1"
            >
              <template v-slot:item.pending="{ item }">
                {{ formatCurrency(item.pending) }}
              </template>
              <template v-slot:item.completed="{ item }">
                {{ formatCurrency(item.completed) }}
              </template>
              <template v-slot:item.balance="{ item }">
                <span :class="item.balance >= 0 ? 'success--text' : 'error--text'">
                  {{ formatCurrency(item.balance) }}
                </span>
              </template>
              <template v-slot:item.progress="{ item }">
                <v-progress-linear
                  :value="(item.completed / item.pending) * 100"
                  height="25"
                  rounded
                  :color="getProgressColor((item.completed / item.pending) * 100)"
                >
                  <template v-slot:default="{ value }">
                    <strong>{{ Math.round(value) }}%</strong>
                  </template>
                </v-progress-linear>
              </template>
            </v-data-table>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { ref, computed, onMounted } from "vue";
import { useProject } from "@/composables/useProject";
import { useInstallments } from "@/composables/useInstallments";
import BarChart from "@/components/shared/charts/BarChart.vue";
import LineChart from "@/components/shared/charts/LineChart.vue";
import DoughnutChart from "@/components/shared/charts/DoughnutChart.vue";

export default {
  name: "OverviewView",
  components: {
    BarChart,
    LineChart,
    DoughnutChart,
  },
  setup() {
    const { project, fetchProject } = useProject();
    const { installments, fetchInstallments } = useInstallments();
    const allInstallments = ref([]);
    const areasSummary = ref([]);
    const selectedGraph = ref('completed');
    const headers = [
      { text: "Área", value: "name", align: "start" },
      { text: "Valor Alocado", value: "pending", align: "end" },
      { text: "Valor Executado", value: "completed", align: "end" },
      { text: "Saldo", value: "balance", align: "end" },
      { text: "Progresso", value: "progress", align: "center" },
    ];

    const totalBudget = computed(() => {
      return project.value ? project.value.reduce((total, proj) => total + proj.total_compensation_expected, 0) : 0;
    });

    const totalExecuted = computed(() => {
      return project.value ? project.value.reduce((total, proj) => total + proj.total_compensation_executed, 0) : 0;
    });

    const totalPending = computed(() => {
      return project.value ? project.value.reduce((total, proj) => total + proj.total_compensation_pending, 0) : 0;
    });

    const totalOverdue = computed(() => {
      return project.value ? project.value.reduce((total, proj) => total + proj.total_compensation_overdue, 0) : 0;
    });

    const projectCount = computed(() => {
      return project.value ? project.value.length : 0;
    });

    const completedAreasSummary = computed(() => {
      return areasSummary.value.map(area => ({
        name: area.name,
        value: area.completed
      })).filter(area => area.value > 0);
    });

    const pendingAreasSummary = computed(() => {
      return areasSummary.value.map(area => ({
        name: area.name,
        value: area.pending - area.completed
      })).filter(area => area.value > 0);
    });

    const overdueAreasSummary = computed(() => {
      const summary = {};
      
      if (!allInstallments.value) return [];

      allInstallments.value.forEach((installment) => {
        if (!installment.area_values || installment.status !== 'Atrasada') return;
        
        Object.entries(installment.area_values).forEach(([area, value]) => {
          if (!summary[area]) {
            summary[area] = 0;
          }
          summary[area] += value;
        });
      });

      return Object.entries(summary).map(([name, value]) => ({
        name,
        value
      })).filter(area => area.value > 0);
    });

    const formatCurrency = (value) => {
      return new Intl.NumberFormat("pt-BR", {
        style: "currency",
        currency: "BRL",
      }).format(value);
    };

    const getProgressColor = (percentage) => {
      if (percentage < 30) return "error";
      if (percentage < 70) return "warning";
      return "success";
    };

    const graphs = [
      {
        id: 'completed',
        name: 'Parcelas Quitadas',
        icon: 'mdi-check-circle-outline',
        component: 'doughnut-chart',
        props: { areasSummary: completedAreasSummary },
        title: 'Distribuição de Parcelas Quitadas',
        subtitle: 'Por área de investimento'
      },
      {
        id: 'pending',
        name: 'Parcelas Pendentes',
        icon: 'mdi-clock-outline',
        component: 'doughnut-chart',
        props: { areasSummary: pendingAreasSummary },
        title: 'Distribuição de Parcelas Pendentes',
        subtitle: 'Por área de investimento'
      },
      {
        id: 'overdue',
        name: 'Parcelas Atrasadas',
        icon: 'mdi-alert-circle-outline',
        component: 'doughnut-chart',
        props: { areasSummary: overdueAreasSummary },
        title: 'Distribuição de Parcelas Atrasadas',
        subtitle: 'Por área de investimento'
      },
      {
        id: 'evolution',
        name: 'Evolução',
        icon: 'mdi-chart-line',
        component: 'line-chart',
        props: { 
          installments: allInstallments,
          graphTitle: 'Evolução do Orçamento Executado'
        },
        title: 'Evolução do Orçamento Executado',
        subtitle: 'Últimos 12 meses'
      },
      {
        id: 'status',
        name: 'Status',
        icon: 'mdi-chart-bar',
        component: 'bar-chart',
        props: { installments: allInstallments },
        title: 'Status dos Projetos',
        subtitle: 'Por fase de execução'
      }
    ];

    const getSelectedGraphComponent = computed(() => {
      const graph = graphs.find(g => g.id === selectedGraph.value);
      return graph ? graph.component : 'doughnut-chart';
    });

    const getSelectedGraphProps = computed(() => {
      const graph = graphs.find(g => g.id === selectedGraph.value);
      if (!graph) return {};
      
      const props = {};
      Object.entries(graph.props).forEach(([key, value]) => {
        if (value && typeof value === 'object' && 'value' in value) {
          props[key] = value.value;
        } else {
          props[key] = value;
        }
      });
      return props;
    });

    const getSelectedGraphTitle = computed(() => {
      const graph = graphs.find(g => g.id === selectedGraph.value);
      return graph ? graph.title : '';
    });

    const getSelectedGraphSubtitle = computed(() => {
      const graph = graphs.find(g => g.id === selectedGraph.value);
      return graph ? graph.subtitle : '';
    });

    const getSelectedGraphIcon = computed(() => {
      const graph = graphs.find(g => g.id === selectedGraph.value);
      return graph ? graph.icon : 'mdi-chart-donut';
    });

    onMounted(async () => {
      try {
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

        // Ordenar as parcelas por data
        allInstallmentsData.sort((a, b) => {
          const dateA = new Date(a.effective_date || a.estimated_date);
          const dateB = new Date(b.effective_date || b.estimated_date);
          return dateA - dateB;
        });

        allInstallments.value = allInstallmentsData;
        calculateAreasSummary();
      } catch (error) {
        console.error('Error loading data:', error);
      }
    });

    const calculateAreasSummary = () => {
      const summary = {};

      if (!allInstallments.value) return;

      allInstallments.value.forEach((installment) => {
        if (!installment.area_values) return;
        
        Object.entries(installment.area_values).forEach(([area, value]) => {
          if (!summary[area]) {
            summary[area] = {
              name: area,
              pending: 0,
              completed: 0,
              balance: 0,
            };
          }

          summary[area].pending += value;
          
          if (installment.effective_date) {
            summary[area].completed += value;
          }
        });
      });

      Object.values(summary).forEach((area) => {
        area.balance = area.pending - area.completed;
      });

      areasSummary.value = Object.values(summary);
    };

    return {
      allInstallments,
      areasSummary,
      headers,
      formatCurrency,
      getProgressColor,
      completedAreasSummary,
      pendingAreasSummary,
      overdueAreasSummary,
      totalBudget,
      totalExecuted,
      totalPending,
      totalOverdue,
      projectCount,
      selectedGraph,
      graphs,
      getSelectedGraphComponent,
      getSelectedGraphProps,
      getSelectedGraphTitle,
      getSelectedGraphSubtitle,
      getSelectedGraphIcon
    };
  },
};
</script>

<style scoped>
.v-card {
  transition: transform 0.3s, box-shadow 0.3s;
  height: 100%;
}

.v-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1) !important;
}

.h-100 {
  height: 100%;
}

.rounded-lg {
  border-radius: 12px !important;
}

.v-card-text {
  min-height: 120px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
</style>