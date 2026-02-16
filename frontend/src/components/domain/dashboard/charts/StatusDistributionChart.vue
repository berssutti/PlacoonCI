<template>
  <div class="chart-container" :style="{ height: `${height}px` }">
    <h3 v-if="graphTitle" class="chart-title">{{ graphTitle }}</h3>
    <div class="chart-wrapper">
      <BaseBarChart v-if="chartData" :chart-data="chartData" :options="chartOptions" />
    </div>
    <div v-if="chartData && chartData.datasets.length === 0" class="no-data">
      <p>Não há dados para exibir.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from "vue";
import BaseBarChart from "@/components/ui/charts/BaseBarChart.vue";
import { formatCurrency } from "@/utils/currencyUtils";

const props = defineProps({
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
    default: 400,
  },
});

const fullChartLabels = ref([]);
const chartData = ref(null);

const chartOptions = {
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
        title: (tooltipItems) => {
          if (tooltipItems.length > 0) {
            const tooltipItem = tooltipItems[0];
            if (tooltipItem && typeof tooltipItem.dataIndex === 'number') {
              const dataIndex = tooltipItem.dataIndex;
              if (fullChartLabels.value && dataIndex >= 0 && dataIndex < fullChartLabels.value.length) {
                return fullChartLabels.value[dataIndex];
              }
            }
          }
          return '';
        },
        label: (context) => {
          const label = context.dataset.label || "";
          const value = parseFloat(context.raw) || 0;
          const total = context.chart.data.datasets
            .map(d => d.data[context.dataIndex])
            .reduce((a, b) => a + b, 0);
          const percentage = total > 0 ? ((value / total) * 100).toFixed(1) + '%' : '0%';
          return `${label}: ${formatCurrency(value)} (${percentage})`;
        },
        footer: (tooltipItems) => {
          const total = tooltipItems.reduce((sum, tooltip) => sum + parseFloat(tooltip.raw), 0);
          return `Total: ${formatCurrency(total)}`;
        }
      },
    },
  },
  scales: {
    x: {
      stacked: true,
      title: {
        display: true,
        text: "Projeto",
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
  executed: '#4CAF50',    // Verde - Valor executado
  pending: '#FFC107',     // Amarelo - Valor pendente
  overdue: '#F44336',     // Vermelho - Valor atrasado
};

const prepareChartData = () => {
  if (!props.data || props.data.length === 0) {
    chartData.value = {
      labels: [],
      datasets: [],
    };
    fullChartLabels.value = [];
    return;
  }
  const sortedAreas = [...props.data].sort((a, b) => {
    const totalA = parseFloat(a.budget) || 0;
    const totalB = parseFloat(b.budget) || 0;
    return totalB - totalA;
  });

  const originalLabels = sortedAreas.map(area => String(area.name || ''));
  fullChartLabels.value = originalLabels;

  const displayLabels = originalLabels.map(name => {
    if (name.length > 8) {
      return name.substring(0, 8) + "...";
    }
    return name;
  });

  const executedValues = sortedAreas.map(area => parseFloat(area.executed) || 0);
  const pendingValues = sortedAreas.map(area => parseFloat(area.pending) || 0);
  const overdueValues = sortedAreas.map(area => parseFloat(area.overdue) || 0);
  const datasets = [
    {
      label: 'Executado',
      data: executedValues,
      backgroundColor: colors.executed,
      borderColor: '#ffffff',
      borderWidth: 2,
      borderRadius: 8,
    },
    {
      label: 'Pendente',
      data: pendingValues,
      backgroundColor: colors.pending,
      borderColor: '#ffffff',
      borderWidth: 2,
      borderRadius: 8,
    },
    {
      label: 'Atrasado',
      data: overdueValues,
      backgroundColor: colors.overdue,
      borderColor: '#ffffff',
      borderWidth: 2,
      borderRadius: 8,
    }
  ];

  chartData.value = {
    labels: displayLabels,
    datasets,
  };
};

watch(() => props.data, () => {
  prepareChartData();
}, { deep: true });

onMounted(() => {
  prepareChartData();
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