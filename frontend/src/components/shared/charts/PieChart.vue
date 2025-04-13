<template>
    <div class="chart-container">
      <h3 class="chart-title">{{ graphTitle }}</h3>
      <div class="chart-wrapper">
        <pie :data="chartData" :options="chartOptions" />
      </div>
      <div v-if="chartData && chartData.datasets.length === 0" class="no-data">
        <p>Não há dados para exibir.</p>
      </div>
    </div>
  </template>
  
  <script>
  import { defineComponent } from "vue";
  import { Chart as ChartJS, ArcElement, Tooltip, Legend } from "chart.js";
  import { Pie } from "vue-chartjs";
  
  ChartJS.register(ArcElement, Tooltip, Legend);
  
  export default defineComponent({
    name: "PieChart",
    components: { Pie },
    props: {
      data: {
        type: Array,
        required: true,
      },
      graphTitle: {
        type: String,
        required: true,
      },
    },
    data() {
      return {
        chartData: null,
        chartOptions: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: "top",
            },
            tooltip: {
              callbacks: {
                label: (context) => {
                  const label = context.label || "";
                  const value = context.raw || 0;
                  return `${label}: ${this.formatCurrency(value)}`;
                },
              },
            },
          },
        },
      };
    },
    watch: {
      data: {
        handler() {
          this.prepareChartData();
        },
        deep: true,
        immediate: true,
      },
    },
    methods: {
      formatCurrency(value) {
        return new Intl.NumberFormat("pt-BR", {
          style: "currency",
          currency: "BRL",
        }).format(value);
      },
      prepareChartData() {
        if (!this.data || this.data.length === 0) {
          this.chartData = {
            labels: [],
            datasets: [],
          };
          return;
        }
  
        const labels = this.data.map((area) => area.name);
        const data = this.data.map((area) => area.allocated);
  
        this.chartData = {
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
      },
    },
  });
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