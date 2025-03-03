<template>
  <div class="chart-container">
    <h3 class="chart-title">{{ graphTitle }}</h3>
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
      required: true,
    },
  },
  data() {
    return {
      chartData: null,
      chartOptions: null,
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
    
    // Adicionar responsividade ao redimensionar a janela
    window.addEventListener('resize', this.handleResize);
  },
  beforeUnmount() {
    // Remover o event listener quando o componente for desmontado
    window.removeEventListener('resize', this.handleResize);
  },
  methods: {
    handleResize() {
      // Atualizar o gráfico quando a janela for redimensionada
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
      if (!this.installments || this.installments.length === 0) {
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

      const defaultColor = '#777777';
      
      const areaTotals = {};
      Array.from(areaNames).forEach(area => {
        areaTotals[area] = (areaDataMap[area] || []).reduce((sum, val) => sum + val, 0);
      });
      
      const sortedAreas = Array.from(areaNames).sort((a, b) => areaTotals[b] - areaTotals[a]);
      
      const datasets = sortedAreas.map((area) => ({
        label: area,
        data: areaDataMap[area],
        backgroundColor: this.areaColors[area] || defaultColor,
        borderColor: '#ffffff',
        borderWidth: 1,
      }));

      this.chartData = {
        labels,
        datasets,
      };

      this.chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: "top",
            labels: {
              usePointStyle: true,
              padding: 15,
              font: {
                size: 12
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
              weight: 'bold'
            },
            bodyFont: {
              size: 13
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
                size: 14
              },
              padding: 10
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
              text: 'Valor (R$)',
              font: {
                weight: 'bold',
                size: 14
              },
              padding: 10
            },
            ticks: {
              callback: (value) => this.formatCurrency(value)
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
  height: 450px;
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

@media (max-width: 767px) {
  .chart-container {
    height: 350px;
    padding: 10px;
  }
  
  .chart-title {
    font-size: 16px;
    margin-bottom: 10px;
  }
}
</style>