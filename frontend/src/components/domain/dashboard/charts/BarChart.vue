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
import { ref, watch, onMounted, onBeforeUnmount, nextTick } from "vue";
import BaseBarChart from "@/components/ui/charts/BaseBarChart.vue";
import { formatCurrency } from "@/utils/currencyUtils";
import { Chart as ChartJS } from "chart.js";

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
  graphTitle: {
    type: String,
    default: "",
  },
  height: {
    type: Number,
    default: 450,
  },
});

const chartData = ref(null);
const chartOptions = ref(null);

const colors = [
  "#4CAF50", // verde
  "#2196F3", // azul
  "#FFC107", // amarelo
  "#9C27B0", // roxo
  "#F44336", // vermelho
  "#00BCD4", // ciano
  "#FF9800", // laranja
  "#3F51B5", // indigo
  "#E91E63", // rosa
  "#009688", // verde-azulado
  "#8BC34A", // verde claro
  "#673AB7", // roxo escuro
];

const areaColors = {
  'Engenharia de Software': '#4CAF50',   // Verde
  'Engenharia de Energia': '#FFC107',    // Amarelo
  'Engenharia Eletrônica': '#2196F3',    // Azul
  'Engenharia Aeroespacial': '#9C27B0',  // Roxo
  'Engenharia Automotiva': '#F44336',    // Vermelho
};

const handleResize = () => {
  if (chartData.value) {
    nextTick(() => {
      ChartJS.defaults.font.size = window.innerWidth < 768 ? 10 : 12;
    });
  }
};

const prepareChartData = () => {
  if (!props.data || Object.keys(props.data).length === 0) {
    chartData.value = {
      labels: [],
      datasets: []
    };
    return;
  }

  const months = Object.keys(props.data).sort((a, b) => parseInt(a) - parseInt(b));
  const areas = new Set();

  months.forEach(month => {
    Object.keys(props.data[month]).forEach(area => {
      areas.add(area);
    });
  });

  const datasets = Array.from(areas).map((area, index) => {
    const color = areaColors[area] || colors[index % colors.length];

    const areaData = months.map(month => {
      return props.data[month][area] || 0; // Se não existir o valor, usar 0
    });

    return {
      label: area,
      data: areaData,
      backgroundColor: color,
      borderColor: '#ffffff',
      borderWidth: 2,
      borderRadius: 8,
    };
  });

  const monthNames = [
    'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
    'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'
  ];

  const labels = months.map(month => {
    return `${monthNames[parseInt(month) - 1]}`;
  });

  const totalValue = months.reduce((sum, month) => {
    return sum + Object.values(props.data[month]).reduce((areaSum, val) => areaSum + val, 0);
  }, 0);

  chartData.value = {
    labels,
    datasets,
  };

  chartOptions.value = {
    plugins: {
      legend: {
        position: "right",
        labels: {
          boxWidth: 15,
          padding: 15,
          font: {
            size: 12,
            family: "'Roboto', sans-serif"
          }
        }
      },
      tooltip: {
        mode: 'index',
        intersect: false,
        callbacks: {
          label: (context) => {
            const label = context.dataset.label || '';
            const value = context.parsed.y;
            const percentage = totalValue > 0
              ? ((value / totalValue) * 100).toFixed(1) + '%'
              : '0%';
            return `${label}: ${formatCurrency(value)} (${percentage})`;
          },
          title: (tooltipItems) => {
            return `Mês: ${tooltipItems[0].label}`;
          }
        }
      }
    },
    scales: {
      x: {
        stacked: true,
        title: {
          display: true,
          text: 'Mês',
          font: {
            weight: 'bold'
          }
        }
      },
      y: {
        stacked: true,
        beginAtZero: true,
        title: {
          display: true,
          text: 'Valor (R$)',
          font: {
            weight: 'bold'
          }
        },
        ticks: {
          callback: (value) => formatCurrency(value)
        }
      }
    }
  };
};

watch(() => props.data, () => {
  prepareChartData();
}, { deep: true, immediate: true });

onMounted(() => {
  prepareChartData();
  window.addEventListener('resize', handleResize);
});

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize);
});
</script>

<style scoped>
.chart-container {
  display: flex;
  flex-direction: column;
  padding: 15px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  width: 100%;
  height: 100%;
}

.chart-title {
  text-align: center;
  font-size: 18px;
  font-weight: 600;
  color: #333333;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eeeeee;
  font-family: 'Roboto', sans-serif;
}

.chart-wrapper {
  flex: 1;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
  width: 100%;
  padding-bottom: 40px;
}

.no-data {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  color: #888888;
  font-style: italic;
  font-family: 'Roboto', sans-serif;
}

@media (max-width: 767px) {
  .chart-container {
    padding: 10px;
  }

  .chart-title {
    font-size: 16px;
    margin-bottom: 10px;
  }

  .chart-wrapper {
    min-height: 300px;
    padding-bottom: 60px;
  }
}
</style>