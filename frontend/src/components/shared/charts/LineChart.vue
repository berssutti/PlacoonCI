<template>
    <div class="chart-container">
      <h3 class="chart-title">{{ graphTitle }}</h3>
      <div class="chart-wrapper">
        <line :data="chartData" :options="chartOptions" />
      </div>
      <div v-if="chartData && chartData.datasets.length === 0" class="no-data">
        <p>Não há dados para exibir.</p>
      </div>
    </div>
  </template>
  
  <script>
  import { defineComponent } from "vue";
  import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
  } from "chart.js";
  import { Line } from "vue-chartjs";
  
  ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
  );
  
  export default defineComponent({
    name: "LineChart",
    components: { Line },
    props: {
      installments: {
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
                  const label = context.dataset.label || "";
                  const value = context.raw || 0;
                  return `${label}: ${this.formatCurrency(value)}`;
                },
              },
            },
          },
          scales: {
            x: {
              title: {
                display: true,
                text: "Mês",
              },
            },
            y: {
              title: {
                display: true,
                text: "Valor (R$)",
              },
              ticks: {
                callback: (value) => this.formatCurrency(value),
              },
            },
          },
        },
      };
    },
    watch: {
      installments: {
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
        if (!this.installments || this.installments.length === 0) {
          this.chartData = {
            labels: [],
            datasets: [],
          };
          return;
        }
  
        const labels = [];
        const data = [];
  
        this.installments.forEach((installment) => {
          const date = new Date(installment.effective_date || installment.estimated_date);
          const monthYear = date.toLocaleDateString("pt-BR", {
            month: "short",
            year: "numeric",
          });
  
          if (!labels.includes(monthYear)) {
            labels.push(monthYear);
            data.push(installment.amount);
          } else {
            const index = labels.indexOf(monthYear);
            data[index] += installment.amount;
          }
        });
  
        this.chartData = {
          labels,
          datasets: [
            {
              label: "Orçamento Executado",
              data,
              borderColor: "#2196F3",
              backgroundColor: "rgba(33, 150, 243, 0.2)",
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