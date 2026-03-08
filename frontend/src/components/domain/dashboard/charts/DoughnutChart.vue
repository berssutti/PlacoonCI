<template>
  <div class="chart-container" :style="{ height: `${height}px` }">
    <h3 v-if="graphTitle" class="chart-title">{{ graphTitle }}</h3>
    <div class="chart-wrapper">
      <BaseDoughnutChart v-if="chartData" :chart-data="chartData" :options="chartOptions" />
    </div>
    <div v-if="chartData && chartData.datasets[0].data.length === 0" class="no-data">
      <p>Não há dados para exibir.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import BaseDoughnutChart from "@/components/ui/charts/BaseDoughnutChart.vue";
import { formatCurrency } from "@/utils/currencyUtils";

const props = defineProps({
  data: {
    type: Array,
    required: true,
  },
  graphTitle: {
    type: String,
    default: "",
  },
  height: {
    type: Number,
    default: 400,
  },
});

const chartData = ref(null);
const chartOptions = {
  cutout: '65%',
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
          const label = context.label || "";
          const value = context.raw || 0;
          const total = context.chart.data.datasets[0].data.reduce((a, b) => a + b, 0);
          const percentage = ((value / total) * 100).toFixed(1);
          return `${label}: ${formatCurrency(value)} (${percentage}%)`;
        },
      },
    },
  },
};

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

const prepareChartData = () => {
  if (!props.data || props.data.length === 0) {
    chartData.value = {
      labels: [],
      datasets: [{ data: [] }],
    };
    return;
  }

  // Filtrar áreas com valores positivos
  const filteredAreas = props.data.filter(area => area.value > 0);

  // Organizar áreas por valor (maior para menor)
  filteredAreas.sort((a, b) => b.value - a.value);

  const labels = filteredAreas.map(area => area.name);
  const data = filteredAreas.map(area => area.value);

  // Criar array de cores com quantidade suficiente
  const backgroundColors = [];
  for (let i = 0; i < labels.length; i++) {
    backgroundColors.push(colors[i % colors.length]);
  }

  chartData.value = {
    labels,
    datasets: [
      {
        data,
        backgroundColor: backgroundColors,
        borderWidth: 2,
        borderColor: '#fff'
      },
    ],
  };
};

watch(() => props.data, () => {
  prepareChartData();
}, { deep: true, immediate: true });
</script>

<style scoped>
.chart-container {
  display: flex;
  flex-direction: column;
  padding: 15px;
  background-color: #ffffff;
  border-radius: 8px;
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