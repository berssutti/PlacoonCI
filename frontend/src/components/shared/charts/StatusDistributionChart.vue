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
  name: "StatusDistributionChart",
  props: {
    installments: {
      type: Array,
      required: true,
    },
    graphTitle: {
      type: String,
      required: true,
    },
    height: {
      type: Number,
      default: 400,
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
              const value = context.raw || 0;
              return `${label}: ${formatCurrency(value)}`;
            },
          },
        },
      },
      scales: {
        x: {
          stacked: true,
          title: {
            display: true,
            text: "Área",
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
          stacked: true,
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
    };

    const colors = {
      'Quitada': '#4CAF50',    // Verde
      'Pendente': '#FFC107',   // Amarelo
      'Atrasada': '#F44336',   // Vermelho
    };

    const formatCurrency = (value) => {
      return new Intl.NumberFormat("pt-BR", {
        style: "currency",
        currency: "BRL",
      }).format(value);
    };

    const prepareChartData = () => {
      if (!props.installments || props.installments.length === 0) {
        chartData.value = {
          labels: [],
          datasets: [],
        };
        return;
      }

      const areaData = {};
      const areaNames = new Set();

      // Coletar todas as áreas e seus valores por status
      props.installments.forEach((installment) => {
        Object.entries(installment.area_values || {}).forEach(([area, value]) => {
          if (typeof value === 'number' && !isNaN(value)) {
            areaNames.add(area);
            if (!areaData[area]) {
              areaData[area] = {
                'Quitada': 0,
                'Pendente': 0,
                'Atrasada': 0
              };
            }

            // Determinar o status da parcela
            let status = 'Pendente';
            if (installment.effective_date) {
              status = 'Quitada';
            } else if (installment.status === 'Atrasada') {
              status = 'Atrasada';
            }

            areaData[area][status] += value;
          }
        });
      });

      // Ordenar áreas por valor total
      const sortedAreas = Array.from(areaNames).sort((a, b) => {
        const totalA = Object.values(areaData[a]).reduce((sum, val) => sum + val, 0);
        const totalB = Object.values(areaData[b]).reduce((sum, val) => sum + val, 0);
        return totalB - totalA;
      });

      const datasets = [
        {
          label: 'Quitada',
          data: sortedAreas.map(area => areaData[area]['Quitada']),
          backgroundColor: colors['Quitada'],
          borderColor: '#ffffff',
          borderWidth: 2,
        },
        {
          label: 'Pendente',
          data: sortedAreas.map(area => areaData[area]['Pendente']),
          backgroundColor: colors['Pendente'],
          borderColor: '#ffffff',
          borderWidth: 2,
        },
        {
          label: 'Atrasada',
          data: sortedAreas.map(area => areaData[area]['Atrasada']),
          backgroundColor: colors['Atrasada'],
          borderColor: '#ffffff',
          borderWidth: 2,
        }
      ];

      chartData.value = {
        labels: sortedAreas,
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

    watch(() => props.installments, () => {
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
  display: flex;
  justify-content: center;
  align-items: center;
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