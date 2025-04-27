<template>
    <!-- O template permanece o mesmo -->
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
import { defineComponent, computed, watch, onMounted, onBeforeUnmount } from 'vue';
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
        // Cores para diferentes áreas (mantido igual)
        const areaColors = {
            'Engenharia de Software': '#4CAF50',
            'Engenharia de Energia': '#FFC107',
            'Engenharia Eletrônica': '#2196F3',
            'Engenharia Aeroespacial': '#9C27B0',
            'Engenharia Automotiva': '#F44336',
            'Outras Áreas': '#009688'
        };

        const formatCurrency = (value) => {
            return new Intl.NumberFormat('pt-BR', {
                style: 'currency',
                currency: 'BRL'
            }).format(value);
        };

        const chartData = computed(() => {
            if (!props.installments || props.installments.length === 0) {
                return { labels: [], datasets: [] };
            }

            try {
                const monthlyData = {};
                const allAreas = new Set();

                // Processar cada parcela
                props.installments.forEach(installment => {
                    const dateStr = installment.effective_date || installment.estimated_date;
                    if (!dateStr) return;

                    // Extrair ano e mês da data no formato YYYY-MM-DD
                    const [year, month] = dateStr.split('-').map(Number);
                    const monthYearKey = `${year}-${month.toString().padStart(2, '0')}`;

                    if (!monthlyData[monthYearKey]) {
                        monthlyData[monthYearKey] = {
                            year,
                            month,
                            data: {}
                        };
                    }

                    // Processar valores por área
                    if (installment.area_values) {
                        Object.entries(installment.area_values).forEach(([area, value]) => {
                            if (!monthlyData[monthYearKey].data[area]) {
                                monthlyData[monthYearKey].data[area] = 0;
                            }
                            monthlyData[monthYearKey].data[area] += parseFloat(value) || 0;
                            allAreas.add(area);
                        });
                    }
                });

                // Nomes dos meses abreviados
                const monthNames = [
                    'jan', 'fev', 'mar', 'abr', 'mai', 'jun',
                    'jul', 'ago', 'set', 'out', 'nov', 'dez'
                ];

                // Ordenar os dados por ano e mês
                const sortedEntries = Object.entries(monthlyData).sort((a, b) => {
                    if (a[1].year !== b[1].year) {
                        return a[1].year - b[1].year;
                    }
                    return a[1].month - b[1].month;
                });

                // Gerar labels no formato "abr/2025"
                const labels = sortedEntries.map(([_, monthData]) => {
                    const monthName = monthNames[monthData.month - 1];
                    return `${monthName}/${monthData.year}`;
                });

                // Criar datasets para cada área
                const datasets = Array.from(allAreas).map((area, index) => {
                    const color = areaColors[area] || Object.values(areaColors)[index % Object.values(areaColors).length];
                    const data = sortedEntries.map(([_, monthData]) => monthData.data[area] || 0);

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

        // Restante do código permanece igual
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
                            const percentage = total > 0 ? ((value / total) * 100).toFixed(1) + '%' : '0%';
                            return `${label}: ${formatCurrency(value)} (${percentage})`;
                        },
                        title: (tooltipItems) => {
                            return `Período: ${tooltipItems[0].label}`;
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
                        text: 'Período',
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
/* Os estilos permanecem os mesmos */
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