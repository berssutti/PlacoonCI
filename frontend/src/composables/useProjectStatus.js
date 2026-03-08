import { computed } from 'vue';

export function useProjectStatus() {
    const getProjectStatus = (project) => {
        if (!project || !project.start_date || !project.end_date) return '';
        const start = new Date(project.start_date);
        const end = new Date(project.end_date);
        const today = new Date();

        if (today < start) return "Não Iniciado";
        if (today > end) return "Concluído";
        return "Em Andamento";
    };

    const getStatusColor = (status) => {
        if (status === "Não Iniciado") return "grey";
        if (status === "Em Andamento") return "primary";
        return "success";
    };

    const getStatusIcon = (status) => {
        if (status === "Não Iniciado") return "mdi-clock-outline";
        if (status === "Em Andamento") return "mdi-progress-clock";
        return "mdi-check-circle-outline";
    };

    const getRemainingTime = (project) => {
        if (!project || !project.start_date || !project.end_date) return '';
        const start = new Date(project.start_date);
        const end = new Date(project.end_date);
        const today = new Date();

        if (today < start) {
            const daysToStart = Math.ceil((start - today) / (1000 * 60 * 60 * 24));
            return `Inicia em ${daysToStart} dia${daysToStart !== 1 ? 's' : ''}`;
        }

        if (today > end) {
            const daysAfterEnd = Math.ceil((today - end) / (1000 * 60 * 60 * 24));
            return `Finalizado há ${daysAfterEnd} dia${daysAfterEnd !== 1 ? 's' : ''}`;
        }

        const daysRemaining = Math.ceil((end - today) / (1000 * 60 * 60 * 24));
        return `${daysRemaining} dia${daysRemaining !== 1 ? 's' : ''} restante${daysRemaining !== 1 ? 's' : ''}`;
    };

    return {
        getProjectStatus,
        getStatusColor,
        getStatusIcon,
        getRemainingTime
    };
}
