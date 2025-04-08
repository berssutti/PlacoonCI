<template>
  <div class="chart-container" :style="{ height: `${height}px` }">
    <h3 v-if="graphTitle" class="chart-title">{{ graphTitle }}</h3>
    <div class="chart-wrapper">
      <bar-chart :data="chartData" :options="chartOptions" />
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
  BarElement,
  CategoryScale,
  LinearScale,
  Title,
  Tooltip,
  Legend
} from "chart.js";
import { Bar } from "vue-chartjs";

ChartJS.register(
  BarElement,
  CategoryScale,
  LinearScale,
  Title,
  Tooltip,
  Legend
);

export default defineComponent({
  name: "StackedBarChart",
  components: { BarChart: Bar },
  props: {
    installments: {
      type: Array,
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
  },
  data() {
    return {
      chartData: null,
      chartOptions: null,
      colors: [
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
      ],
      areaColors: {
        'Engenharia de Software': '#4CAF50',   // Verde
        'Engenharia de Energia': '#FFC107',    // Amarelo
        'Engenharia Eletrônica': '#2196F3',    // Azul
        'Engenharia Aeroespacial': '#9C27B0',  // Roxo
        'Engenharia Automotiva': '#F44336',    // Vermelho
      }
    };
  },
  watch: {
    installments: {
      handler() {
        this.prepareChartData();
      },
      deep: true,
      immediate: true
    }
  },
  mounted() {
    this.prepareChartData();
    window.addEventListener('resize', this.handleResize);
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.handleResize);
  },
  methods: {
    handleResize() {
      if (this.chartData) {
        this.$nextTick(() => {
          ChartJS.defaults.font.size = window.innerWidth < 768 ? 10 : 12;
        });
      }
    },
    formatCurrency(value) {
      return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL',
      }).format(value);
    },
    prepareChartData() {
      console.log("Bar chart data", this.installments);
      if (!this.installments || this.installments.length === 0) {
        console.log('No data to display Bar chart');
        this.chartData = {
          labels: [],
          datasets: []
        };
        return;
      }

      const sortedInstallments = [...this.installments].sort((a, b) => {
        const dateA = a.effective_date ? new Date(a.effective_date) : new Date(a.estimated_date);
        const dateB = b.effective_date ? new Date(b.effective_date) : new Date(b.estimated_date);
        return dateA - dateB;
      });

      const labels = [];
      const areaNames = new Set();
      const areaDataMap = {};
      let totalValue = 0;

      sortedInstallments.forEach((installment) => {
        const dateToUse = installment.effective_date || installment.estimated_date;
        const monthYear = new Date(dateToUse).toLocaleDateString("pt-BR", {
          month: "short",
          year: "numeric",
        });
        
        if (!labels.includes(monthYear)) {
          labels.push(monthYear);
        }

        Object.entries(installment.area_values || {}).forEach(([area, value]) => {
          if (typeof value === 'number' && !isNaN(value)) {
            areaNames.add(area);
            if (!areaDataMap[area]) {
              areaDataMap[area] = new Array(labels.length).fill(0);
            }
            const monthIndex = labels.indexOf(monthYear);
            areaDataMap[area][monthIndex] = (areaDataMap[area][monthIndex] || 0) + value;
            totalValue += value;
          }
        });
      });

      const areaTotals = {};
      Array.from(areaNames).forEach(area => {
        areaTotals[area] = (areaDataMap[area] || []).reduce((sum, val) => sum + val, 0);
      });
      
      const sortedAreas = Array.from(areaNames).sort((a, b) => areaTotals[b] - areaTotals[a]);
      
      const datasets = sortedAreas.map((area, index) => {
        const color = this.areaColors[area] || this.colors[index % this.colors.length];
        
        return {
          label: area,
          data: areaDataMap[area],
          backgroundColor: color,
          borderColor: '#ffffff',
          borderWidth: 2,
          borderRadius: 8,
        };
      });

      this.chartData = {
        labels,
        datasets,
      };

      this.chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        layout: {
          padding: {
            bottom: 20,
            left: 10,
            right: 10,
            top: 10
          }
        },
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
          title: {
            display: false,
          },
          tooltip: {
            mode: 'index',
            intersect: false,
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            padding: 10,
            titleFont: {
              size: 14,
              weight: 'bold',
              family: "'Roboto', sans-serif"
            },
            bodyFont: {
              size: 13,
              family: "'Roboto', sans-serif"
            },
            callbacks: {
              label: (context) => {
                const label = context.dataset.label || '';
                const value = context.parsed.y;
                const percentage = totalValue > 0 
                  ? ((value / totalValue) * 100).toFixed(1) + '%' 
                  : '0%';
                return `${label}: ${this.formatCurrency(value)} (${percentage})`;
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
                weight: 'bold',
                size: 14,
                family: "'Roboto', sans-serif"
              },
              padding: 10
            },
            grid: {
              display: false
            },
            ticks: {
              maxRotation: 45,
              minRotation: 45,
              font: {
                family: "'Roboto', sans-serif",
                size: 11
              },
              padding: 5,
              autoSkip: true,
              maxTicksLimit: 12
            }
          },
          y: {
            stacked: true,
            beginAtZero: true,
            title: {
              display: true,
              text: 'Valor (R$)',
              font: {
                weight: 'bold',
                size: 14,
                family: "'Roboto', sans-serif"
              },
              padding: 10
            },
            ticks: {
              callback: (value) => this.formatCurrency(value),
              font: {
                family: "'Roboto', sans-serif"
              }
            }
          }
        },
        animation: {
          duration: 1000,
          easing: 'easeOutQuart'
        }
      };
    },
  },
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