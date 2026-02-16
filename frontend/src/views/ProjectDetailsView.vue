<template>
    <v-container>
        <v-card elevation="2" class="pa-4 project-card">
            <ProjectHeader :project="project" @edit="handleEditProject" @delete="showDeleteProjectDialog = true"
                @back="handleBack" />

            <ProjectInfo v-if="project" :project="project" />

            <InstallmentList :installments="installments" @add="handleAddInstallment" @edit="handleEditInstallment"
                @delete="handleShowDeleteInstallmentDialog" @chart="handleProjectInstallmentChart" />

            <InstallmentForm v-model="showInstallmentForm" :installment="currentInstallment" :isEditing="isEditing"
                @save="handleSaveInstallment" @close="handleCloseInstallmentForm" />

            <ProjectInstallmentChart v-model="showProjectInstallmentChart" v-if="installments.length > 0"
                :installments="installments" @close="handleCloseProjectInstallmentChart" />

            <ConfirmDialog v-model="showDeleteProjectDialog" title="Confirmar Exclusão de Projeto"
                message="Tem certeza que deseja excluir este projeto? Esta ação não pode ser desfeita."
                confirm-text="Excluir" confirm-color="red darken-1" @confirm="confirmDeleteProject" />

            <ConfirmDialog v-model="showDeleteInstallmentDialog" title="Confirmar Exclusão de Parcela"
                message="Tem certeza que deseja excluir esta parcela? Esta ação não pode ser desfeita."
                confirm-text="Excluir" confirm-color="red darken-1" @confirm="confirmDeleteInstallment" />

            <FeedbackSnackbar v-model="snackbar.show" :message="snackbar.text" :color="snackbar.color" />
        </v-card>
    </v-container>

</template>

<script>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useProject } from '@/composables/useProject';
import { useInstallments } from '@/composables/useInstallments';
import ProjectHeader from '@/components/domain/projects/details/ProjectHeader.vue';
import ProjectInfo from '@/components/domain/projects/details/ProjectInfo.vue';
import InstallmentList from '@/components/domain/projects/details/installment/InstallmentList.vue';
import InstallmentForm from '@/components/domain/projects/details/installment/InstallmentForm.vue';
import ProjectInstallmentChart from '@/components/domain/projects/details/installment/ProjectInstallmentChart.vue';
import ConfirmDialog from '@/components/ui/ConfirmDialog.vue';
import FeedbackSnackbar from '@/components/ui/FeedbackSnackbar.vue';

export default {
    name: 'ProjectDetailsView',

    components: {
        ProjectHeader,
        ProjectInfo,
        InstallmentList,
        InstallmentForm,
        ProjectInstallmentChart,
        ConfirmDialog,
        FeedbackSnackbar,
    },

    setup() {
        const { project, loading: projectLoading, fetchProject, deleteProject } = useProject();
        const { installments, loading: installmentsLoading, fetchInstallments, createInstallment, updateInstallment, deleteInstallment } = useInstallments();
        const route = useRoute();
        const router = useRouter();

        const showInstallmentForm = ref(false);
        const showProjectInstallmentChart = ref(false);
        const currentInstallment = ref({});
        const isEditing = ref(false);
        const showDeleteProjectDialog = ref(false);
        const showDeleteInstallmentDialog = ref(false);
        const installmentToDelete = ref(null);
        const snackbar = ref({
            show: false,
            text: '',
            color: 'success'
        });



        const handleBack = () => router.push({ name: 'ProjectList' });

        const showSnackbar = (text, color = 'success') => {
            snackbar.value = {
                show: true,
                text,
                color
            };
        };

        const confirmDeleteProject = async () => {
            try {
                await deleteProject(project.value.id);
                showSnackbar('Projeto excluído com sucesso');
                router.push({ name: 'ProjectList' });
            } catch (error) {
                console.error('Erro ao deletar o projeto:', error);
                showSnackbar('Erro ao excluir o projeto', 'error');
            }
        };

        const handleEditProject = () => {
            router.push({ name: 'ProjectEdit', params: { id: project.value.id } });
        };

        const handleShowDeleteInstallmentDialog = (installmentId) => {
            installmentToDelete.value = installmentId;
            showDeleteInstallmentDialog.value = true;
        };

        const confirmDeleteInstallment = async () => {
            try {
                await deleteInstallment(project.value.id, installmentToDelete.value);
                await fetchInstallments(project.value.id);
                await fetchProject(project.value.id);
                showSnackbar('Parcela excluída com sucesso');
            } catch (error) {
                console.error('Erro ao deletar a parcela:', error);
                showSnackbar('Erro ao excluir a parcela', 'error');
            } finally {
                installmentToDelete.value = null;
            }
        };


        const handleAddInstallment = () => {
            currentInstallment.value = {
                amount: '',
                estimated_date: null,
                observation: '',
                destination: '',
                status: 'Pendente',
                effective_date: null
            };
            isEditing.value = false;
            showInstallmentForm.value = true;
        };

        const handleEditInstallment = (installment) => {
            currentInstallment.value = { ...installment };
            isEditing.value = true;
            showInstallmentForm.value = true;
        };

        const handleSaveInstallment = async (installment) => {
            try {
                installment.project = project.value.id;
                if (isEditing.value) {
                    await updateInstallment(project.value.id, currentInstallment.value.id, installment);
                    showSnackbar('Parcela atualizada com sucesso');
                } else {
                    await createInstallment(project.value.id, installment);
                    showSnackbar('Parcela criada com sucesso');
                }

                await fetchInstallments(project.value.id);
                await fetchProject(project.value.id);

                handleCloseInstallmentForm();
            } catch (error) {
                console.error('Erro ao salvar a parcela:', error);
                showSnackbar('Erro ao salvar a parcela', 'error');
            }
        };

        const handleCloseInstallmentForm = () => {
            showInstallmentForm.value = false;
            currentInstallment.value = {};
            isEditing.value = false;
        };

        const handleProjectInstallmentChart = () => {
            if (installments.value.length === 0) {
                showSnackbar('Não há parcelas para exibir no gráfico', 'warning');
                return;
            }
            showProjectInstallmentChart.value = true;
        }

        const handleCloseProjectInstallmentChart = () => {
            showProjectInstallmentChart.value = false;
        }

        onMounted(async () => {
            const id = route.params.id;
            try {
                await Promise.all([fetchProject(id), fetchInstallments(id)]);
            } catch (error) {
                console.error('Erro ao carregar o projeto ou as parcelas:', error);
                showSnackbar('Erro ao carregar dados do projeto', 'error');
            }
        });

        return {
            project,
            projectLoading,
            installments,
            installmentsLoading,

            handleBack,
            showInstallmentForm,
            showProjectInstallmentChart,
            currentInstallment,
            isEditing,
            showDeleteProjectDialog,
            showDeleteInstallmentDialog,
            snackbar,
            handleAddInstallment,
            handleEditInstallment,
            handleSaveInstallment,
            handleShowDeleteInstallmentDialog,
            confirmDeleteProject,
            confirmDeleteInstallment,
            handleCloseInstallmentForm,
            handleProjectInstallmentChart,
            handleCloseProjectInstallmentChart,
            handleEditProject,
        };
    }
};
</script>

<style scoped>
.project-card {
    max-width: 800px;
    margin: 20px auto;
    border-radius: 8px;
}
</style>