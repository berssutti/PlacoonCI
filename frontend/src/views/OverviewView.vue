<template>
  <v-container fluid>
    <v-row>
      <v-col cols="12">
        <v-card elevation="2" class="rounded-lg">
          <v-card-title class="d-flex flex-wrap align-center py-4 px-6">
            <div class="d-flex align-center">
              <v-icon size="large" class="mr-2">mdi-chart-donut</v-icon>
              <span class="text-h4 text-sm-h4 text-md-h4 primary--text">Visão Geral dos Ressarcimentos</span>
            </div>
            <v-spacer></v-spacer>
            <v-select
              v-model="selectedYear"
              :items="availableYears"
              label="Ano"
              class="mt-2 mt-sm-0 align-self-center"
              style="max-width: 150px;"
              density="compact"
              variant="outlined"
              @update:model-value="handleYearChange"
            ></v-select>
          </v-card-title>
        </v-card>
      </v-col>
    </v-row>

    <v-row v-if="loading" justify="center" class="mt-4">
      <v-col cols="12" class="text-center py-6">
        <v-progress-circular indeterminate size="64" color="primary"></v-progress-circular>
        <div class="text-h6 grey--text mt-4">Carregando dados...</div>
      </v-col>
    </v-row>

    <v-row v-else-if="error" justify="center" class="mt-4">
      <v-col cols="12">
        <v-alert type="error" elevation="2" class="rounded-lg">{{ error }}</v-alert>
      </v-col>
    </v-row>

    <template v-else>
      <v-row class="mt-4">
        <v-col cols="12" sm="6" md="3">
          <v-card elevation="2" class="rounded-lg h-100" color="primary" dark>
            <v-card-text class="text-center d-flex flex-column justify-center h-100 pa-3 pa-sm-4">
              <div class="text-subtitle-1 text-sm-h6 mb-2">Ressarcimento Total Esperado</div>
              <div class="text-h5 text-sm-h4">{{ formatCurrency(totalBudget) }}</div>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" sm="6" md="3">
          <v-card elevation="2" class="rounded-lg h-100" color="success" dark>
            <v-card-text class="text-center d-flex flex-column justify-center h-100 pa-3 pa-sm-4">
              <div class="text-subtitle-1 text-sm-h6 mb-2">Ressarcimento Executado</div>
              <div class="text-h5 text-sm-h4">{{ formatCurrency(totalExecuted) }}</div>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" sm="6" md="3">
          <v-card elevation="2" class="rounded-lg h-100" color="warning" dark>
            <v-card-text class="text-center d-flex flex-column justify-center h-100 pa-3 pa-sm-4">
              <div class="text-subtitle-1 text-sm-h6 mb-2">Ressarcimento Pendente</div>
              <div class="text-h5 text-sm-h4">{{ formatCurrency(totalPending) }}</div>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" sm="6" md="3">
          <v-card elevation="2" class="rounded-lg h-100" color="error" dark>
            <v-card-text class="text-center d-flex flex-column justify-center h-100 pa-3 pa-sm-4">
              <div class="text-subtitle-1 text-sm-h6 mb-2">Ressarcimento Atrasado</div>
              <div class="text-h5 text-sm-h4">{{ formatCurrency(totalOverdue) }}</div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <v-row class="mt-4">
        <v-col cols="12">
          <v-card class="mb-4">
            <v-card-title class="text-subtitle-1 text-sm-h6 primary--text py-3 py-sm-4 px-4 px-sm-6">
              <v-icon size="small" size-sm="default" class="mr-2">mdi-cash-multiple</v-icon>
              Resumo Financeiro por Área
            </v-card-title>
            <v-card-text class="pa-1 pa-sm-3">
              <div class="table-responsive">
                <v-table class="elevation-1" density="compact" density-sm="default">
                  <thead>
                    <tr>
                      <th v-for="header in headers" :key="header.key" :class="header.align">
                        {{ header.title }}
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="area in areasSummary" :key="area.name">
                      <td>{{ area.name }}</td>
                      <td class="text-end">{{ formatCurrency(area.budget) }}</td>
                      <td class="text-end">{{ formatCurrency(area.executed) }}</td>
                      <td class="text-end">{{ formatCurrency(area.pending) }}</td>
                      <td class="text-end">{{ formatCurrency(area.overdue) }}</td>
                      <td class="text-center">
                        <v-progress-linear
                          :model-value="area.progress"
                          :color="getProgressColor(area.progress)"
                          height="16"
                          height-sm="20"
                          rounded
                          striped
                        >
                          <template v-slot:default="{ value }">
                            <strong class="text-caption text-sm-body-2">{{ Math.ceil(value) }}%</strong>
                          </template>
                        </v-progress-linear>
                      </td>
                    </tr>
                  </tbody>
                </v-table>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <v-row class="mt-4">
        <v-col cols="12">
          <v-card class="mb-4">
            <v-card-title class="text-subtitle-1 text-sm-h6 primary--text py-3 py-sm-4 px-4 px-sm-6">
              <v-icon size="small" size-sm="default" class="mr-2">mdi-chart-timeline-variant</v-icon>
              Detalhamento Financeiro
            </v-card-title>
            <v-card-text class="pa-1 pa-sm-3">
              <v-tabs v-model="activeTab" color="primary">
                <v-tab value="institution">Instituição</v-tab>
                <v-tab value="destination">Destinação</v-tab>
                <v-tab value="areas">Áreas</v-tab>
              </v-tabs>

              <v-window v-model="activeTab">
                <v-window-item value="institution">
                  <v-card flat class="mt-4">
                    <v-card-text>
                      <v-row>
                        <v-col cols="12" md="6">
                          <v-card outlined class="pa-4">
                            <div class="text-subtitle-1 font-weight-bold mb-2">Total Recebido por Instituição</div>
                            <v-list>
                              <v-list-item v-for="(amount, institution) in institutionSummary" :key="institution">
                                <v-list-item-title>{{ institution }}</v-list-item-title>
                                <template v-slot:append>
                                  <span class="text-subtitle-1 font-weight-bold">{{ formatCurrency(amount) }}</span>
                                </template>
                              </v-list-item>
                            </v-list>
                          </v-card>
                        </v-col>
                        <v-col cols="12" md="6">
                          <v-card outlined class="pa-4">
                            <div class="text-subtitle-1 font-weight-bold mb-2">Distribuição por Ano</div>
                            <v-list>
                              <v-list-item v-for="(amount, year) in yearSummary" :key="year">
                                <v-list-item-title>{{ year }}</v-list-item-title>
                                <template v-slot:append>
                                  <span class="text-subtitle-1 font-weight-bold">{{ formatCurrency(amount) }}</span>
                                </template>
                              </v-list-item>
                            </v-list>
                          </v-card>
                        </v-col>
                      </v-row>
                    </v-card-text>
                  </v-card>
                </v-window-item>

                <v-window-item value="destination">
                  <v-card flat class="mt-4">
                    <v-card-text>
                      <v-row>
                        <v-col cols="12">
                          <v-card outlined class="pa-4">
                            <div class="text-subtitle-1 font-weight-bold mb-2">Destinação dos Recursos</div>
                            <v-list>
                              <v-list-item v-for="(amount, destination) in destinationSummary" :key="destination">
                                <v-list-item-title>{{ destination }}</v-list-item-title>
                                <template v-slot:append>
                                  <span class="text-subtitle-1 font-weight-bold">{{ formatCurrency(amount) }}</span>
                                </template>
                              </v-list-item>
                            </v-list>
                          </v-card>
                        </v-col>
                      </v-row>
                    </v-card-text>
                  </v-card>
                </v-window-item>

                <v-window-item value="areas">
                  <v-card flat class="mt-4">
                    <v-card-text>
                      <v-row>
                        <v-col cols="12" md="6">
                          <v-card outlined class="pa-4">
                            <div class="text-subtitle-1 font-weight-bold mb-2">Distribuição por Área</div>
                            <v-list>
                              <v-list-item v-for="area in areasSummary" :key="area.name">
                                <v-list-item-title>{{ area.name }}</v-list-item-title>
                                <template v-slot:append>
                                  <span class="text-subtitle-1 font-weight-bold">{{ formatCurrency(area.budget) }}</span>
                                </template>
                              </v-list-item>
                            </v-list>
                          </v-card>
                        </v-col>
                        <v-col cols="12" md="6">
                          <v-card outlined class="pa-4">
                            <div class="text-subtitle-1 font-weight-bold mb-2">Execução por Área</div>
                            <v-list>
                              <v-list-item v-for="area in areasSummary" :key="area.name">
                                <v-list-item-title>{{ area.name }}</v-list-item-title>
                                <template v-slot:append>
                                  <span class="text-subtitle-1 font-weight-bold">{{ formatCurrency(area.executed) }}</span>
                                </template>
                              </v-list-item>
                            </v-list>
                          </v-card>
                        </v-col>
                      </v-row>
                    </v-card-text>
                  </v-card>
                </v-window-item>
              </v-window>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <v-row class="mt-4">
        <v-col cols="12">
          <v-card elevation="2" class="rounded-lg">
            <v-card-title class="text-subtitle-1 text-sm-h6">
              <v-icon size="small" size-sm="default" class="mr-2">{{ getSelectedGraphIcon }}</v-icon>
              {{ getSelectedGraphTitle }}
            </v-card-title>
            <v-card-subtitle class="pb-0">{{ getSelectedGraphSubtitle }}</v-card-subtitle>
            <v-card-text>
              <v-row>
                <v-col cols="12" class="d-flex justify-center mb-2 mb-sm-4">
                  <v-btn-group class="flex-wrap">
                    <v-btn
                      v-for="graph in graphs"
                      :key="graph.id"
                      :color="selectedGraph === graph.id ? 'primary' : ''"
                      @click="selectedGraph = graph.id"
                      class="ma-1"
                      variant="outlined"
                      size="x-small"
                      size-sm="small"
                      density="compact"
                      density-sm="default"
                    >
                      <v-icon size="x-small" size-sm="small" class="mr-0 mr-sm-1">{{ graph.icon }}</v-icon>
                      <span class="d-none d-sm-inline">{{ graph.name }}</span>
                      <span class="d-sm-none">{{ graph.shortName || graph.name.substring(0, 3) + '...' }}</span>
                    </v-btn>
                  </v-btn-group>
                </v-col>
                <v-col cols="12">
                  <component
                    :is="getSelectedGraphComponent"
                    v-bind="getSelectedGraphProps"
                    :height="chartHeight"
                  />
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </template>
  </v-container>
</template>

<script>
import { ref, computed, onMounted, watch } from "vue";
import { useProject } from "@/composables/useProject";
import { useInstallments } from "@/composables/useInstallments";
import BarChart from "@/components/shared/charts/BarChart.vue";
import LineChart from "@/components/shared/charts/LineChart.vue";
import DoughnutChart from "@/components/shared/charts/DoughnutChart.vue";
import StatusDistributionChart from "@/components/shared/charts/StatusDistributionChart.vue";
import GroupedBarChart from "@/components/shared/charts/GroupedBarChart.vue";
import { useOverview } from '@/composables/useOverview';

export default {
  name: "OverviewView",
  components: {
    BarChart,
    LineChart,
    DoughnutChart,
    StatusDistributionChart,
    GroupedBarChart,
  },
  setup() {
    const { project, fetchProject } = useProject();
    const { installments, fetchInstallments } = useInstallments();
    const { overview, loading, error, fetchOverview } = useOverview();
    const allInstallments = ref([]);
    const selectedGraph = ref('status');
    const windowWidth = ref(window.innerWidth);
    const chartHeight = ref(getChartHeight());
    const selectedYear = ref(new Date().getFullYear());
    const availableYears = ref([]);
    const activeTab = ref('institution');

    const headers = [
      { title: "Área", key: "name", align: "start" },
      { title: "Orçamento", key: "budget", align: "end" },
      { title: "Executado", key: "executed", align: "end" },
      { title: "Pendente", key: "pending", align: "end" },
      { title: "Atrasado", key: "overdue", align: "end" },
      { title: "Progresso", key: "progress", align: "center" },
    ];

    const updateAvailableYears = () => {
      if (!project.value || project.value.length === 0) {
        availableYears.value = [new Date().getFullYear()];
        return;
      }

      const years = new Set();
      project.value.forEach(proj => {
        const startYear = new Date(proj.start_date).getFullYear();
        const endYear = new Date(proj.end_date).getFullYear();
        
        for (let year = startYear; year <= endYear; year++) {
          years.add(year);
        }
      });

      availableYears.value = Array.from(years).sort((a, b) => b - a);
      
      if (!availableYears.value.includes(selectedYear.value)) {
        selectedYear.value = availableYears.value[0];
      }
    };

    const handleYearChange = async () => {
      await fetchOverview(selectedYear.value);
    };

    function getChartHeight() {
      if (window.innerWidth < 600) return 250;
      if (window.innerWidth < 960) return 300;
      return 400;
    }

    function handleResize() {
      windowWidth.value = window.innerWidth;
      chartHeight.value = getChartHeight();
    }

    onMounted(() => {
      window.addEventListener('resize', handleResize);
    });

    const totalBudget = computed(() => {
      return overview.value?.total_expected || 0;
    });

    const totalExecuted = computed(() => {
      return overview.value?.total_executed || 0;
    });

    const totalPending = computed(() => {
      return overview.value?.total_pending || 0;
    });

    const totalOverdue = computed(() => {
      return overview.value?.total_overdue || 0;
    });

    const projectCount = computed(() => {
      return project.value ? project.value.length : 0;
    });

    const completedAreasSummary = computed(() => {
      return overview.value?.areas_summary.map(area => ({
        name: area.name,
        value: area.executed
      })).filter(area => area.value > 0);
    });

    const pendingAreasSummary = computed(() => {
      return overview.value?.areas_summary.map(area => ({
        name: area.name,
        value: area.pending
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
        maximumFractionDigits: windowWidth.value < 600 ? 0 : 2,
      }).format(value);
    };

    const getProgressColor = (percentage) => {
      if (percentage < 30) return "error";
      if (percentage < 70) return "warning";
      return "success";
    };

    const graphs = [
      {
        id: 'status',
        name: 'Estados das Parcelas por Área',
        shortName: 'Est',
        icon: 'mdi-chart-bar-stacked',
        component: 'status-distribution-chart',
        props: { 
          installments: allInstallments,
          graphTitle: 'Distribuição de Estados das Parcelas por Área'
        },
        title: 'Distribuição de Estados das Parcelas por Área',
        subtitle: 'Estados das parcelas por área de investimento'
      },
      {
        id: 'grouped_bar',
        name: 'Ressarcimentos por Projeto',
        shortName: 'Proj',
        icon: 'mdi-chart-bar',
        component: 'grouped-bar-chart',
        props: { 
          projects: project,
          graphTitle: 'Valores dos Ressarcimentos por Projeto'
        },
        title: 'Ressarcimentos por Projeto',
        subtitle: 'Distribuição de valores por projeto'
      },
      {
        id: 'area_distribution',
        name: 'Distribuição de Ressarcimentos por Área',
        shortName: 'Área',
        icon: 'mdi-chart-bar',
        component: 'bar-chart',
        props: { 
          installments: allInstallments,
          graphTitle: 'Distribuição de Ressarcimentos por Área'
        },
        title: 'Distribuição de Ressarcimentos por Área',
        subtitle: 'Valores executados por área de investimento'
      },
      {
        id: 'evolution',
        name: 'Evolução do Ressarcimento Executado',
        shortName: 'Evol',
        icon: 'mdi-chart-line',
        component: 'line-chart',
        props: { 
          installments: allInstallments,
          graphTitle: 'Evolução dos Ressarcimentos Executados'
        },
        title: 'Evolução dos Ressarcimentos Executados',
        subtitle: ''
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
      
      props.responsive = true;
      props.maintainAspectRatio = false;
      
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
      await fetchProject();
      updateAvailableYears();
      await fetchOverview(selectedYear.value);
    });

    // Watch for changes in project data to update available years
    watch(() => project.value, () => {
      updateAvailableYears();
    }, { deep: true });

    const loadInstallments = async () => {
      const allInstallmentsData = [];

      if (project.value && project.value.length > 0) {
        for (const proj of project.value) {
          await fetchInstallments(proj.id);
          if (installments.value && installments.value.length > 0) {
            allInstallmentsData.push(...installments.value);
          }
        }
      }

      allInstallmentsData.sort((a, b) => {
        const dateA = new Date(a.effective_date || a.estimated_date);
        const dateB = new Date(b.effective_date || b.estimated_date);
        return dateA - dateB;
      });

      allInstallments.value = allInstallmentsData;
    };

    const areasSummary = computed(() => {
      return overview.value?.areas_summary || [];
    });

    const institutionSummary = computed(() => {
      return overview.value?.institution_summary || {};
    });

    const yearSummary = computed(() => {
      return overview.value?.year_summary || {};
    });

    const destinationSummary = computed(() => {
      return overview.value?.destination_summary || {};
    });

    const projectsSummary = computed(() => {
      return overview.value?.projects_summary || [];
    });

    const monthlySummary = computed(() => {
      return overview.value?.monthly_summary || {};
    });

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
      getSelectedGraphIcon,
      chartHeight,
      windowWidth,
      selectedYear,
      availableYears,
      handleYearChange,
      activeTab,
      institutionSummary,
      yearSummary,
      destinationSummary,
      projectsSummary,
      monthlySummary,
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
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.v-table {
  background-color: #ffffff;
}

.v-table thead th {
  background-color: #f5f5f5;
  font-weight: 600;
  color: #333333;
  font-family: 'Roboto', sans-serif;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.v-table tbody td {
  font-family: 'Roboto', sans-serif;
}

.v-table tbody tr:hover {
  background-color: #f8f9fa;
}

.text-end {
  text-align: end;
}

.text-center {
  text-align: center;
}

.table-responsive {
  width: 100%;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

@media (max-width: 599px) {
  .v-btn-group {
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .v-card-title {
    font-size: 1.25rem !important;
  }
  
  .v-table {
    font-size: 0.75rem;
  }
  
  .v-table thead th {
    padding: 8px !important;
    font-size: 0.7rem;
  }
  
  .v-table tbody td {
    padding: 6px !important;
  }
}

@media (min-width: 600px) and (max-width: 959px) {
  .v-table thead th {
    padding: 10px !important;
  }
  
  .v-table tbody td {
    padding: 8px !important;
  }
}

.v-list-item {
  border-bottom: 1px solid #eee;
}

.v-list-item:last-child {
  border-bottom: none;
}

.v-card--outlined {
  border: 1px solid rgba(0, 0, 0, 0.12);
  border-radius: 8px;
}
</style>