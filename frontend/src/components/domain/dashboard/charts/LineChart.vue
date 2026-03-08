<template>
  <div class="chart-container" :style="{ height: `${height}px` }">
    <h3 v-if="graphTitle" class="chart-title">{{ graphTitle }}</h3>
    <div class="chart-wrapper">
      <BaseLineChart v-if="chartData" :chart-data="chartData" :options="chartOptions" />
    </div>
    <div v-if="chartData && chartData.datasets.length === 0" class="no-data">
      <p>Não há dados para exibir.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from "vue";
import BaseLineChart from "@/components/ui/charts/BaseLineChart.vue";
import { formatCurrency } from "@/utils/currencyUtils";

const props = defineProps({
  data: {
    type: Object,
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
      callbacks: {
        label: (context) => {
          const label = context.dataset.label || "";
          const value = context.raw || 0;
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
      title: {
        display: true,
        text: "Mês",
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
};

const colors = [
  "#4CAF50", // verde
  "#2196F3", // azul
  "#FFC107", // amarelo
  "#9C27B0", // roxo
  "#F44336", // vermelho
];

const prepareChartData = () => {
  if (!props.data || Object.keys(props.data).length === 0) {
    chartData.value = {
      labels: [],
      datasets: [],
    };
    return;
  }

  const months = Object.keys(props.data)
    .map(month => parseInt(month))
    .sort((a, b) => a - b);

  const monthNames = [
    'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
    'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'
  ];

  const labels = months.map(month => `${monthNames[month - 1]}`);
  const values = months.map(month => parseFloat(props.data[month]) || 0);

  chartData.value = {
    labels,
    datasets: [
      {
        label: "Orçamento Executado",
        data: values,
        borderColor: colors[0],
        backgroundColor: `${colors[0]}33`,
        borderWidth: 2,
        tension: 0.3,
        pointBackgroundColor: colors[0],
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointRadius: 5,
        pointHoverRadius: 7,
        fill: true
      },
    ],
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
