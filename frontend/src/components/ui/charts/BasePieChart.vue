<template>
    <Pie :data="chartData" :options="chartOptions" />
</template>

<script setup>
import {
    Chart as ChartJS,
    ArcElement,
    Tooltip,
    Legend
} from 'chart.js'
import { Pie } from 'vue-chartjs'
import { computed } from 'vue'

ChartJS.register(ArcElement, Tooltip, Legend)

const props = defineProps({
    chartData: {
        type: Object,
        required: true
    },
    options: {
        type: Object,
        default: () => ({})
    }
})

const chartOptions = computed(() => {
    return {
        responsive: true,
        maintainAspectRatio: false,
        ...props.options
    }
})
</script>
