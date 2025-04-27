<template>
    <div class="area-chart-container" :style="{ height: `${height}px` }">
        <h3 v-if="graphTitle" class="area-chart-title">{{ graphTitle }}</h3>
        <div class="area-chart-wrapper">
            <Bar v-if="chartData.datasets.length > 0" :data="chartData" :options="chartOptions" />
            <div v-else class="no-data-message">
                <v-icon large color="grey lighten-1">mdi-chart-bar</v-icon>
                <p class="mt-2 grey--text">Não há dados para exibir</p>
            </div>
        </div>
    </div>
</template>

<script>
import { defineComponent, computed, watch, onMounted, onBeforeUnmount, ref } from 'vue';
import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    BarElement,
    CategoryScale,
    LinearScale
} from 'chart.js';
import { Bar } from 'vue-chartjs';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

export default defineComponent({
    name: 'AreaStackedBarChart',
    components: { Bar },
    props: {
        installments: {
            type: Array,
            required: true,
            default: () => []
        },
        graphTitle: {
            type: String,
            default: 'Distribuição por Área'
        },
        height: {
            type: Number,
            default: 450
        }
    },
    setup(props) {
        // Debug
        watch(() => props.installments, (newVal) => {
            console.log("Processing chart data:", newVal);
        }, { immediate: true, deep: true });

        // Cores para diferentes áreas
        const areaColors = {
            'Engenharia de Software': '#4CAF50',   // Verde
            'Engenharia de Energia': '#FFC107',    // Amarelo
            'Engenharia Eletrônica': '#2196F3',    // Azul
            'Engenharia Aeroespacial': '#9C27B0',  // Roxo
            'Engenharia Automotiva': '#F44336',    // Vermelho
            'Outras Áreas': '#009688'              // Verde-azulado
        };

        // Formatação de valores monetários
        const formatCurrency = (value) => {
            return new Intl.NumberFormat('pt-BR', {
                style: 'currency',
                currency: 'BRL'
            }).format(value);
        };

        // Processar dados para o gráfico
        const chartData = computed(() => {
            if (!props.installments || props.installments.length === 0) {
                return { labels: [], datasets: [] };
            }

            try {
                // Agrupar instalações por mês
                const monthlyData = {};
                const allAreas = new Set();

                props.installments.forEach(installment => {
                    // Usar a data efetiva ou estimada
                    const date = installment.effective_date || installment.estimated_date;
                    if (!date) return;

                    const dateObj = new Date(date);
                    const month = dateObj.getMonth() + 1; // 1-12 para representar meses

                    // Garantir que temos o mês criado no objeto
                    if (!monthlyData[month]) {
                        monthlyData[month] = {};
                    }

                    // Processar cada área do objeto area_values
                    if (installment.area_values) {
                        Object.entries(installment.area_values).forEach(([area, value]) => {
                            if (!monthlyData[month][area]) {
                                monthlyData[month][area] = 0;
                            }
                            monthlyData[month][area] += parseFloat(value) || 0;
                            allAreas.add(area);
                        });
                    }
                });

                // Nomes dos meses para labels
                const monthNames = [
                    'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                    'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'
                ];

                // Ordenar os meses numericamente
                const sortedMonths = Object.keys(monthlyData)
                    .map(Number)
                    .sort((a, b) => a - b);

                // Gerar labels dos meses
                const labels = sortedMonths.map(month => monthNames[month - 1]);

                // Criar datasets para cada área
                const datasets = Array.from(allAreas).map((area, index) => {
                    // Selecionar cor da área ou usar fallback
                    const color = areaColors[area] || Object.values(areaColors)[index % Object.values(areaColors).length];

                    // Dados para cada mês
                    const data = sortedMonths.map(month => {
                        return monthlyData[month][area] || 0;
                    });

                    return {
                        label: area,
                        data,
                        backgroundColor: color,
                        borderColor: '#ffffff',
                        borderWidth: 1,
                        borderRadius: 4
                    };
                });

                return { labels, datasets };
            } catch (error) {
                console.error("Erro ao processar dados do gráfico:", error);
                return { labels: [], datasets: [] };
            }
        });

        // Calcular total por mês para tooltips
        const getMonthlyTotals = computed(() => {
            const monthlyTotals = {};

            if (chartData.value && chartData.value.labels) {
                chartData.value.labels.forEach((label, monthIndex) => {
                    let total = 0;
                    chartData.value.datasets.forEach(dataset => {
                        total += dataset.data[monthIndex] || 0;
                    });
                    monthlyTotals[monthIndex] = total;
                });
            }

            return monthlyTotals;
        });

        // Opções do gráfico
        const chartOptions = computed(() => ({
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
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
                            const monthIndex = context.dataIndex;
                            const total = getMonthlyTotals.value[monthIndex] || 0;

                            const percentage = total > 0
                                ? ((value / total) * 100).toFixed(1) + '%'
                                : '0%';

                            return `${label}: ${formatCurrency(value)} (${percentage})`;
                        },
                        title: (tooltipItems) => {
                            return `Mês: ${tooltipItems[0].label}`;
                        }
                    }
                },
                title: {
                    display: false
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
        }));

        // Ajustar tamanho da fonte baseado no tamanho da tela
        const handleResize = () => {
            ChartJS.defaults.font.size = window.innerWidth < 768 ? 10 : 12;
        };

        onMounted(() => {
            handleResize();
            window.addEventListener('resize', handleResize);
        });

        onBeforeUnmount(() => {
            window.removeEventListener('resize', handleResize);
        });

        return {
            chartData,
            chartOptions
        };
    }
});
</script>

<style scoped>
.area-chart-container {
    display: flex;
    flex-direction: column;
    padding: 15px;
    background-color: #ffffff;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    width: 100%;
    height: 100%;
}

.area-chart-title {
    text-align: center;
    font-size: 18px;
    font-weight: 600;
    color: #333333;
    margin-bottom: 15px;
    padding-bottom: 10px;
    border-bottom: 1px solid #eeeeee;
    font-family: 'Roboto', sans-serif;
}

.area-chart-wrapper {
    flex: 1;
    position: relative;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 380px;
    width: 100%;
}

.no-data-message {
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
    .area-chart-container {
        padding: 10px;
    }

    .area-chart-title {
        font-size: 16px;
        margin-bottom: 10px;
    }

    .area-chart-wrapper {
        min-height: 300px;
    }
}
</style>