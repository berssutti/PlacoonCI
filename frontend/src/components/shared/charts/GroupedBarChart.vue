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
import { useRouter } from 'vue-router';
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
    projects: {
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
    const router = useRouter();
    const chartRef = ref(null);
    let chart = null;

    const chartData = ref(null);
    const chartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      onClick: (event, elements) => {
        if (elements && elements.length > 0) {
          const index = elements[0].index;
          const sortedProjects = [...props.projects].sort((a, b) => {
            return b.total_compensation_expected - a.total_compensation_expected;
          });
          const projectId = sortedProjects[index].id;
          router.push(`/projects/${projectId}`);
        }
      },
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
              const value = context.raw || 0;
              const total = context.chart.data.datasets[0].data[context.dataIndex];
              const percentage = total > 0 ? ((value / total) * 100).toFixed(1) + '%' : '0%';
              return `${label}: ${formatCurrency(value)} (${percentage})`;
            },
          },
        },
      },
      scales: {
        x: {
          stacked: false,
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
          stacked: false,
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
      hover: {
        mode: 'index',
        intersect: false,
        onHover: (event, elements) => {
          event.native.target.style.cursor = elements.length ? 'pointer' : 'default';
        }
      },
    };

    const colors = {
      total: '#2196F3',    // Azul
      executed: '#4CAF50', // Verde
      overdue: '#F44336',  // Vermelho
      pending: '#FFC107'   // Amarelo
    };

    const formatCurrency = (value) => {
      return new Intl.NumberFormat("pt-BR", {
        style: "currency",
        currency: "BRL",
      }).format(value);
    };

    const prepareChartData = () => {
      if (!props.projects || props.projects.length === 0) {
        chartData.value = {
          labels: [],
          datasets: [],
        };
        return;
      }

      // Ordenar projetos por valor total (do maior para o menor)
      const sortedProjects = [...props.projects].sort((a, b) => {
        return b.total_compensation_expected - a.total_compensation_expected;
      });

      const labels = sortedProjects.map(project => project.name);
      
      const datasets = [
        {
          label: 'Ressarcimento Total',
          data: sortedProjects.map(project => project.total_compensation_expected),
          backgroundColor: colors.total,
          borderColor: '#ffffff',
          borderWidth: 2,
          borderRadius: 8,
        },
        {
          label: 'Ressarcimento Executado',
          data: sortedProjects.map(project => project.total_compensation_executed),
          backgroundColor: colors.executed,
          borderColor: '#ffffff',
          borderWidth: 2,
          borderRadius: 8,
        },
        {
          label: 'Ressarcimento Atrasado',
          data: sortedProjects.map(project => project.total_compensation_overdue),
          backgroundColor: colors.overdue,
          borderColor: '#ffffff',
          borderWidth: 2,
          borderRadius: 8,
        },
        {
          label: 'Ressarcimento Pendente',
          data: sortedProjects.map(project => project.total_compensation_pending),
          backgroundColor: colors.pending,
          borderColor: '#ffffff',
          borderWidth: 2,
          borderRadius: 8,
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

    watch(() => props.projects, () => {
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