import { ref } from 'vue';
import { installmentService } from '@/services/installmentService';

export function useInstallments() {
    const installments = ref([]);
    const loading = ref(false);
    const error = ref(null);

    const fetchInstallments = async (projectId) => {
        loading.value = true;

        try {
            const response = await installmentService.getProjectInstallments(projectId);
            installments.value = response.data;
        } catch (err) {
            error.value = 'Erro ao carregar parcelas';
            console.error(err);
        } finally {
            loading.value = false;
        }
    };

    const createInstallment = async (projectId, data) => {
        loading.value = true;

        try {
            await installmentService.createInstallment(projectId, data);
        } catch (err) {
            error.value = 'Erro ao criar parcela';
            console.error(err);
        } finally {
            loading.value = false;
        }
    };

    const updateInstallment = async (projectId, installmentId, data) => {
        loading.value = true;

        try {
            await installmentService.updateInstallment(projectId, installmentId, data);
        } catch (err) {
            error.value = 'Erro ao atualizar parcela';
            console.error(err);
        } finally {
            loading.value = false;
        }
    };

    const deleteInstallment = async (projectId, installmentId) => {
        loading.value = true;

        try {
            await installmentService.deleteInstallment(projectId, installmentId);
            installments.value = installments.value.filter(installment => installment.id !== installmentId);
        } catch (err) {
            error.value = 'Erro ao deletar parcela';
            console.error(err);
        } finally {
            loading.value = false;
        }
    };

    return {
        installments,
        loading,
        error,
        fetchInstallments,
        createInstallment,
        updateInstallment,
        deleteInstallment
    };
}