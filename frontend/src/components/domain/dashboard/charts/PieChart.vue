<template>
  <div class="chart-container">
    <h3 class="chart-title">{{ graphTitle }}</h3>
    <div class="chart-wrapper">
      <BasePieChart v-if="chartData" :chart-data="chartData" :options="chartOptions" />
    </div>
    <div v-if="chartData && chartData.datasets.length === 0" class="no-data">
      <p>Não há dados para exibir.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import BasePieChart from "@/components/ui/charts/BasePieChart.vue";
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
});

const chartData = ref(null);
const chartOptions = {
  plugins: {
    legend: {
      position: "top",
    },
    tooltip: {
      callbacks: {
        label: (context) => {
          const label = context.label || "";
          const value = context.raw || 0;
          return `${label}: ${formatCurrency(value)}`;
        },
      },
    },
  },
};

const prepareChartData = () => {
  if (!props.data || props.data.length === 0) {
    chartData.value = {
      labels: [],
      datasets: [],
    };
    return;
  }

  const labels = props.data.map((area) => area.name);
  const data = props.data.map((area) => area.allocated);

  chartData.value = {
    labels,
    datasets: [
      {
        label: "Orçamento Alocado",
        data,
        backgroundColor: [
          "#4CAF50",
          "#FFC107",
          "#2196F3",
          "#9C27B0",
          "#F44336",
        ],
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
  height: 400px;
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