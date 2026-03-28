<template>
  <v-container fluid>
    <v-row class="mb-12">
      <v-col cols="12" class="d-flex align-end justify-space-between">
        <div>
          <h1 class="text-h2 font-weight-black mb-2 tracking-tight">Dashboard</h1>
          <p class="text-subtitle-1 text-slate-500 font-medium">Curadoria de dados e desempenho orçamentário PlacoonCI</p>
        </div>
        <div style="width: 240px;">
          <v-select
            v-model="selectedYear"
            :items="availableYears"
            label="Exercício Fiscal"
            hide-details
            variant="filled"
            density="comfortable"
            @update:model-value="handleYearChange"
          ></v-select>
        </div>
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
      <v-row class="mb-12">
        <v-col cols="12" sm="6" md="3">
          <v-card class="pa-6 bg-surface-container-lowest elevation-0 no-line-card">
            <div class="d-flex flex-column">
              <div class="rounded-xl pa-4 bg-surface-container-low mb-6 align-self-start">
                <v-icon color="primary" size="32">mdi-currency-usd</v-icon>
              </div>
              <div>
                <div class="text-overline font-weight-bold mb-1">TOTAL EXPECTED</div>
                <div class="text-h4 font-weight-black">{{ formatCurrency(totalBudget) }}</div>
              </div>
            </div>
          </v-card>
        </v-col>
        <v-col cols="12" sm="6" md="3">
          <v-card class="pa-6 bg-surface-container-lowest elevation-0 no-line-card">
            <div class="d-flex flex-column">
              <div class="rounded-xl pa-4 bg-surface-container-low mb-6 align-self-start">
                <v-icon color="success" size="32">mdi-check-circle-outline</v-icon>
              </div>
              <div>
                <div class="text-overline font-weight-bold mb-1">EXECUTED</div>
                <div class="text-h4 font-weight-black">{{ formatCurrency(totalExecuted) }}</div>
              </div>
            </div>
          </v-card>
        </v-col>
        <v-col cols="12" sm="6" md="3">
          <v-card class="pa-6 bg-surface-container-lowest elevation-0 no-line-card">
            <div class="d-flex flex-column">
              <div class="rounded-xl pa-4 bg-surface-container-low mb-6 align-self-start">
                <v-icon color="warning" size="32">mdi-clock-outline</v-icon>
              </div>
              <div>
                <div class="text-overline font-weight-bold mb-1">PENDING</div>
                <div class="text-h4 font-weight-black">{{ formatCurrency(totalPending) }}</div>
              </div>
            </div>
          </v-card>
        </v-col>
        <v-col cols="12" sm="6" md="3">
          <v-card class="pa-6 bg-surface-container-lowest elevation-0 no-line-card">
            <div class="d-flex flex-column">
              <div class="rounded-xl pa-4 bg-surface-container-low mb-6 align-self-start">
                <v-icon color="error" size="32">mdi-alert-circle-outline</v-icon>
              </div>
              <div>
                <div class="text-overline font-weight-bold mb-1">OVERDUE</div>
                <div class="text-h4 font-weight-black">{{ formatCurrency(totalOverdue) }}</div>
              </div>
            </div>
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
                  <v-btn-group class="flex-wrap" rounded>
                    <v-btn v-for="graph in graphs" :key="graph.id"
                      :color="selectedGraph === graph.id ? 'primary' : 'grey-lighten-1'"
                      :class="{ 'selected-btn': selectedGraph === graph.id }" @click="selectedGraph = graph.id"
                      class="ma-1 transition-fast-in-fast-out" variant="flat" size="x-small" size-sm="small"
                      min-width="40" min-height="28" :ripple="false">
                      <v-icon size="x-small" size-sm="small" class="mr-1">{{ graph.icon }}</v-icon>
                      <span class="d-none d-sm-inline">{{ graph.name }}</span>
                      <span class="d-sm-none">{{ graph.shortName || graph.name.substring(0, 3) }}</span>
                    </v-btn>
                  </v-btn-group>
                </v-col>
                <v-col cols="12">
                  <component :is="getSelectedGraphComponent" v-bind="getSelectedGraphProps" :height="chartHeight" />
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <v-row class="mt-4">
        <v-col cols="12">
          <v-card class="mb-10 bg-surface-container-lowest elevation-0 no-line-card">
            <v-card-title class="text-h5 font-weight-bold primary--text py-8 px-8 border-none">
              Resumo Financeiro por Área
            </v-card-title>
            <v-card-text class="pa-0">
              <v-data-table
                :headers="headersAreasSummary"
                :items="areasSummary"
                class="bg-transparent custom-table"
                hide-default-footer
              >
                <template v-slot:item.budget="{ item }">
                  <span class="text-end">{{ formatCurrency(item.budget) }}</span>
                </template>
                <template v-slot:item.executed="{ item }">
                  <span class="text-end">{{ formatCurrency(item.executed) }}</span>
                </template>
                <template v-slot:item.pending="{ item }">
                  <span class="text-end">{{ formatCurrency(item.pending) }}</span>
                </template>
                <template v-slot:item.overdue="{ item }">
                  <span class="text-end">{{ formatCurrency(item.overdue) }}</span>
                </template>
                <template v-slot:item.progress="{ item }">
                  <div class="text-center">
                    <v-progress-linear :model-value="item.progress" :color="getProgressColor(item.progress)" height="16"
                      height-sm="20" rounded striped>
                      <template v-slot:default="{ value }">
                        <strong class="text-caption text-sm-body-2">{{ Math.ceil(value) }}%</strong>
                      </template>
                    </v-progress-linear>
                  </div>
                </template>
              </v-data-table>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <v-row class="mt-4">
        <v-col cols="12">
          <v-card class="mb-4">
            <v-card-title class="text-subtitle-1 text-sm-h6 primary--text py-3 py-sm-4 px-4 px-sm-6">
              <v-icon size="small" size-sm="default" class="mr-2">mdi-pin</v-icon>
              Resumo dos Projetos
            </v-card-title>
            <v-card-text class="pa-1 pa-sm-3">
              <v-data-table :headers="headersProjectsSummary" :items="projectsSummary" class="elevation-1"
                density="compact">
                <template v-slot:item.areas="{ item }">
                  <div class="text-caption">
                    {{ formatAreas(item.areas) }}
                  </div>
                </template>
                <template v-slot:item.expected="{ item }">
                  <div class="text-caption">
                    {{ formatCurrency(item.expected) }}
                  </div>
                </template>
              </v-data-table>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>


      <v-row class="mt-4">
        <v-col cols="12">
          <v-card class="mb-4">
            <v-card-title class="text-subtitle-1 text-sm-h6 primary--text py-3 py-sm-4 px-4 px-sm-6">
              <v-icon size="small" size-sm="default" class="mr-2">mdi-chart-timeline-variant</v-icon>
              Detalhamento da Destinação
            </v-card-title>
            <v-card-text class="pa-1 pa-sm-3">
              <v-data-table :headers="headersDestinationDetails" :items="destinationTableItems" class="elevation-1"
                density="compact">
                <template v-slot:item.amount="{ item }">
                  <span class="text-end">{{ formatCurrency(item.amount) }}</span>
                </template>
              </v-data-table>
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
import BarChart from "@/components/domain/dashboard/charts/BarChart.vue";
import LineChart from "@/components/domain/dashboard/charts/LineChart.vue";
import DoughnutChart from "@/components/domain/dashboard/charts/DoughnutChart.vue";
import StatusDistributionChart from "@/components/domain/dashboard/charts/StatusDistributionChart.vue";
import GroupedBarChart from "@/components/domain/dashboard/charts/GroupedBarChart.vue";
import { useOverview } from '@/composables/useOverview';
import { formatCurrency as formatCurrencyUtil } from "@/utils/currencyUtils";

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
    const { availableYears, fetchAvailableYears } = useProject();
    const { installments, fetchInstallments } = useInstallments();
    const { overview, loading, error, fetchOverview } = useOverview();

    const selectedGraph = ref('status');
    const windowWidth = ref(window.innerWidth);
    const chartHeight = ref(getChartHeight());
    const selectedYear = ref(new Date().getFullYear());

    // const activeTab = ref('institution');

    const headersAreasSummary = [
      { title: "Área", key: "name", align: "start" },
      { title: "Orçamento", key: "budget", align: "end" },
      { title: "Executado", key: "executed", align: "end" },
      { title: "Pendente", key: "pending", align: "end" },
      { title: "Atrasado", key: "overdue", align: "end" },
      { title: "Progresso", key: "progress", align: "center" },
    ];

    const headersProjectsSummary = [
      { title: "Data de Início", key: "start_date", align: "start" },
      { title: "Projeto", key: "name", align: "start" },
      { title: "Coordenador", key: "coordinator", align: "start" },
      { title: "Areas", key: "areas", align: "start" },
      { title: "Ressarcimento Total Esperado", key: "expected", align: "start" },
      { title: "Quantidade de Parcelas", key: "total_installments", align: "start" },
    ];

    const headersDestinationDetails = [
      { title: "Destinação", key: "destination", align: "start" },
      { title: "Valor", key: "amount", align: "end" },
    ];

    const formatAreas = (areas) => {
      return areas.join(', ');
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



    const formatCurrency = (value) => formatCurrencyUtil(value);

    const getProgressColor = (percentage) => {
      if (percentage < 30) return "error";
      if (percentage < 70) return "warning";
      return "success";
    };

    const graphs = [
      {
        id: 'status',
        name: 'Estágios das Parcelas por Área',
        shortName: 'Est',
        icon: 'mdi-chart-bar',
        component: 'grouped-bar-chart',
        props: {
          data: computed(() => overview.value?.areas_summary),
          graphTitle: 'Distribuição de Estágios das Parcelas por Área'
        },
        title: 'Distribuição de Estágios das Parcelas por Área',
        subtitle: 'Estágios das parcelas por área de investimento'
      },
      {
        id: 'grouped_bar',
        name: 'Ressarcimentos por Projeto',
        shortName: 'Proj',
        icon: 'mdi-chart-bar-stacked',
        component: 'status-distribution-chart',
        props: {
          data: computed(() => overview.value?.projects_summary),
          graphTitle: 'Valores dos Ressarcimentos por Projeto'
        },
        title: 'Ressarcimentos por Projeto',
        subtitle: 'Distribuição de valores por projeto'
      },
      {
        id: 'area_distribution',
        name: 'Distribuição dos Ressarcimentos Executados por Área',
        shortName: 'Área',
        icon: 'mdi-chart-bar',
        component: 'bar-chart',
        props: {
          data: computed(() => overview.value?.monthly_area_summary),
          graphTitle: 'Distribuição de Ressarcimentos Executados por Área'
        },
        title: 'Distribuição de Ressarcimentos Executados por Área',
        subtitle: 'Valores executados por área de investimento'
      },
      {
        id: 'evolution',
        name: 'Evolução do Ressarcimento Executado',
        shortName: 'Evol',
        icon: 'mdi-chart-line',
        component: 'line-chart',
        props: {
          data: computed(() => overview.value?.monthly_summary),
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
      await fetchAvailableYears();
      if (availableYears.value.length > 0 && !availableYears.value.includes(selectedYear.value)) {
        selectedYear.value = availableYears.value[0];
      }
      await fetchOverview(selectedYear.value);
    });



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

    const destinationTableItems = computed(() => {
      if (!overview.value?.destination_summary) return [];
      return Object.entries(overview.value.destination_summary).map(([destination, amount]) => ({
        destination,
        amount
      }));
    });


    const projectsSummary = computed(() => {
      return overview.value?.projects_summary || [];

    });

    const monthlySummary = computed(() => {
      return overview.value?.monthly_summary || {};
    });

    return {
      areasSummary,
      headersAreasSummary,
      headersProjectsSummary,
      formatCurrency,
      formatAreas,
      getProgressColor,
      completedAreasSummary,
      pendingAreasSummary,

      totalBudget,
      totalExecuted,
      totalPending,
      totalOverdue,

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
      institutionSummary,
      yearSummary,
      destinationSummary,
      projectsSummary,
      monthlySummary,
      headersDestinationDetails, // Added
      destinationTableItems, // Added

    };
  },
};
</script>

<style scoped>
.bg-indigo-50 { background-color: #EEF2FF !important; }
.bg-emerald-50 { background-color: #ECFDF5 !important; }
.bg-amber-50 { background-color: #FFFBEB !important; }
.bg-rose-50 { background-color: #FFF1F2 !important; }

.text-indigo-600 { color: #4F46E5 !important; }
.text-emerald-600 { color: #059669 !important; }
.text-amber-600 { color: #D97706 !important; }
.text-rose-600 { color: #E11D48 !important; }

.text-slate-900 { color: #0F172A !important; }
.text-slate-500 { color: #64748B !important; }
.text-slate-400 { color: #94A3B8 !important; }

.border-none { border: none !important; }
.elevation-sm { box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1) !important; }

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

.custom-table {
  border: none !important;
}

.custom-table :deep(thead th) {
  background-color: transparent !important;
  font-weight: 700 !important;
  color: #3f4941 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.1em !important;
  font-size: 0.75rem !important;
  border-bottom: none !important;
  padding: 16px 32px !important;
}

.custom-table :deep(tbody td) {
  padding: 24px 32px !important;
  border-bottom: none !important;
  font-size: 0.95rem !important;
}

.custom-table :deep(tbody tr:nth-of-type(even)) {
  background-color: #f0f4fd !important;
}

.custom-table :deep(tbody tr:hover) {
  background-color: #eaeef7 !important;
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

.v-btn {
  text-transform: none;
  letter-spacing: normal;
  font-weight: 500;
}

.v-btn.selected-btn {
  box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.2), 0 4px 5px 0 rgba(0, 0, 0, 0.14), 0 1px 10px 0 rgba(0, 0, 0, 0.12);
}

.v-btn:not(.selected-btn):hover {
  background-color: #e0e0e0 !important;
  transform: translateY(-1px);
}

.transition-fast-in-fast-out {
  transition: all 0.2s ease;
}
</style>