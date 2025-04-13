<template>
  <div class="chart-container" :style="{ height: `${height}px` }">
    <h3 v-if="graphTitle" class="chart-title">{{ graphTitle }}</h3>
    <div class="chart-wrapper">
      <canvas ref="chartRef"></canvas>
    </div>
    <div v-if="chartData && chartData.datasets.length === 0" class="no-data">
      <p>Não há dados para exibir.</p>
    </div>
  </div>
</template>

<script>
import { defineComponent, ref, onMounted, watch, onBeforeUnmount } from "vue";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

export default defineComponent({
  name: "GroupedBarChart",
  props: {
    data: {
      type: Array,
      required: true,
    },
    graphTitle: {
      type: String,
      required: true,
    },
    height: {
      type: Number,
      default: 500,
    },
  },
  setup(props) {
    const chartRef = ref(null);
    let chart = null;

    const chartData = ref(null);
    const chartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "right",
          labels: {
            padding: 15,
            boxWidth: 15,
            font: {
              size: 12
            }
          }
        },
        tooltip: {
          mode: 'index',
          intersect: false,
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          padding: 10,
          titleFont: {
            size: 14,
            weight: 'bold'
          },
          bodyFont: {
            size: 13
          },
          callbacks: {
            label: (context) => {
              const label = context.dataset.label || "";
              const value = parseFloat(context.raw) || 0;
              return `${label}: ${formatCurrency(value)}`;
            },
            title: (tooltipItems) => {
              return tooltipItems[0].label;
            }
          },
        },
      },
      scales: {
        x: {
          grouped: true,  // Esta opção agrupa as barras
          title: {
            display: true,
            text: "Projetos",
            font: {
              size: 12,
              weight: 600
            }
          },
          grid: {
            display: false
          },
          ticks: {
            maxRotation: 45,
            minRotation: 45
          }
        },
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: "Valor (R$)",
            font: {
              size: 12,
              weight: 600
            }
          },
          ticks: {
            callback: (value) => formatCurrency(value),
          },
          grid: {
            color: "#eeeeee"
          }
        },
      },
      interaction: {
        mode: 'index',
        intersect: false
      }
    };

    const colors = {
      expected: '#2196F3',    // Azul - Valor esperado
      executed: '#4CAF50',    // Verde - Valor executado
      overdue: '#F44336',     // Vermelho - Valor atrasado
      pending: '#FFC107'      // Amarelo - Valor pendente
    };

    const formatCurrency = (value) => {
      return new Intl.NumberFormat("pt-BR", {
        style: "currency",
        currency: "BRL",
      }).format(value);
    };

    const prepareChartData = () => {
      if (!props.data || props.data.length === 0) {
        chartData.value = {
          labels: [],
          datasets: [],
        };
        return;
      }

      // Ordenar projetos por valor esperado (do maior para o menor)
      const sortedProjects = [...props.data].sort((a, b) => {
        return parseFloat(b.expected) - parseFloat(a.expected);
      });

      const labels = sortedProjects.map(project => project.name);
      
      // Converter strings para números
      const expectedValues = sortedProjects.map(project => parseFloat(project.expected));
      const executedValues = sortedProjects.map(project => parseFloat(project.executed));
      const overdueValues = sortedProjects.map(project => parseFloat(project.overdue));
      const pendingValues = sortedProjects.map(project => parseFloat(project.pending));

      const datasets = [
        {
          label: 'Valor Esperado',
          data: expectedValues,
          backgroundColor: colors.expected,
          borderColor: '#ffffff',
          borderWidth: 2,
          borderRadius: 4,
        },
        {
          label: 'Valor Executado',
          data: executedValues,
          backgroundColor: colors.executed,
          borderColor: '#ffffff',
          borderWidth: 2,
          borderRadius: 4,
        },
        {
          label: 'Valor Atrasado',
          data: overdueValues,
          backgroundColor: colors.overdue,
          borderColor: '#ffffff',
          borderWidth: 2,
          borderRadius: 4,
        },
        {
          label: 'Valor Pendente',
          data: pendingValues,
          backgroundColor: colors.pending,
          borderColor: '#ffffff',
          borderWidth: 2,
          borderRadius: 4,
        }
      ];

      chartData.value = {
        labels,
        datasets,
      };
    };

    const initChart = () => {
      if (chartRef.value && chartData.value) {
        const ctx = chartRef.value.getContext('2d');
        chart = new ChartJS(ctx, {
          type: 'bar',
          data: chartData.value,
          options: chartOptions
        });
      }
    };

    const updateChart = () => {
      if (chart && chartData.value) {
        chart.data = chartData.value;
        chart.update();
      }
    };

    watch(() => props.data, () => {
      prepareChartData();
      updateChart();
    }, { deep: true });

    onMounted(() => {
      prepareChartData();
      initChart();
    });

    onBeforeUnmount(() => {
      if (chart) {
        chart.destroy();
      }
    });

    return {
      chartRef,
      chartData,
      chartOptions,
      formatCurrency
    };
  }
});
</script>

<style scoped>
.chart-container {
  display: flex;
  flex-direction: column;
  padding: 15px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.chart-title {
  text-align: center;
  font-size: 18px;
  font-weight: 600;
  color: #333333;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eeeeee;
}

.chart-wrapper {
  flex: 1;
  position: relative;
  min-height: 300px;
}

.no-data {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  color: #888888;
  font-style: italic;
}
</style>