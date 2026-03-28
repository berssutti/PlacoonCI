<template>
  <v-container fluid>
    <v-row class="mb-6">
      <v-col cols="12" class="d-flex align-center justify-space-between">
        <div class="d-flex align-center">
          <v-btn icon="mdi-arrow-left" variant="text" @click="handleBack" class="mr-4"></v-btn>
          <div>
            <h1 class="text-h4 font-weight-bold mb-1">Detalhes do Projeto</h1>
            <p class="text-subtitle-1 text-grey" v-if="project">{{ project.name }}</p>
          </div>
        </div>
        <div class="d-flex gap-2">
          <v-btn
            color="primary"
            variant="outlined"
            prepend-icon="mdi-pencil"
            @click="handleEditProject"
            class="mr-2"
          >
            Editar
          </v-btn>
          <v-btn
            color="error"
            variant="outlined"
            prepend-icon="mdi-delete"
            @click="showDeleteProjectDialog = true"
          >
            Excluir
          </v-btn>
        </div>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="8">
        <v-card class="mb-6">
          <v-card-title class="pa-6 border-b">
            <span class="text-h6 font-weight-bold">Informações Gerais</span>
          </v-card-title>
          <v-card-text class="pa-6">
            <ProjectInfo v-if="project" :project="project" />
          </v-card-text>
        </v-card>

        <v-card>
          <v-card-title class="pa-6 border-b d-flex justify-space-between align-center">
            <span class="text-h6 font-weight-bold">Parcelas de Ressarcimento</span>
            <div class="d-flex gap-2">
              <v-btn
                v-if="installments.length > 0"
                variant="text"
                color="primary"
                prepend-icon="mdi-chart-bar"
                @click="handleProjectInstallmentChart"
                class="mr-2"
              >
                Gráfico
              </v-btn>
              <v-btn
                color="primary"
                prepend-icon="mdi-plus"
                @click="handleAddInstallment"
              >
                Adicionar Parcela
              </v-btn>
            </div>
          </v-card-title>
          <v-card-text class="pa-0">
            <InstallmentList
              :installments="installments"
              @add="handleAddInstallment"
              @edit="handleEditInstallment"
              @delete="handleShowDeleteInstallmentDialog"
              @chart="handleProjectInstallmentChart"
            />
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="4">
        <!-- Sidebar style summary if needed -->
        <v-card v-if="project" class="mb-6">
           <v-card-title class="pa-6 border-b">Resumo Financeiro</v-card-title>
           <v-card-text class="pa-6">
              <div class="mb-4">
                <div class="text-caption text-grey font-weight-bold text-uppercase mb-1">TOTAL ESPERADO</div>
                <div class="text-h5 font-weight-bold">{{ formatCurrency(project.total_fcte_amount_expected) }}</div>
              </div>
              <v-divider class="my-4"></v-divider>
              <div class="d-flex justify-space-between mb-2">
                <span class="text-body-2 text-grey">Status</span>
                <v-chip size="x-small" :color="getStatusColor(getProjectStatus(project))" variant="tonal" class="font-weight-bold">
                  {{ getProjectStatus(project) }}
                </v-chip>
              </div>
              <div class="d-flex justify-space-between">
                <span class="text-body-2 text-grey">Processo SEI</span>
                <span class="text-body-2 font-weight-medium">{{ project.processo_sei }}</span>
              </div>
           </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <InstallmentForm v-model="showInstallmentForm" :installment="currentInstallment" :isEditing="isEditing"
        @save="handleSaveInstallment" @close="handleCloseInstallmentForm" />

    <ProjectInstallmentChart v-model="showProjectInstallmentChart" v-if="installments.length > 0"
        :installments="installments" @close="handleCloseProjectInstallmentChart" />

    <ConfirmDialog v-model="showDeleteProjectDialog" title="Confirmar Exclusão de Projeto"
        message="Tem certeza que deseja excluir este projeto? Esta ação não pode ser desfeita."
        confirm-text="Excluir" confirm-color="red" @confirm="confirmDeleteProject" />

    <ConfirmDialog v-model="showDeleteInstallmentDialog" title="Confirmar Exclusão de Parcela"
        message="Tem certeza que deseja excluir esta parcela? Esta ação não pode ser desfeita."
        confirm-text="Excluir" confirm-color="red" @confirm="confirmDeleteInstallment" />

    <FeedbackSnackbar v-model="snackbar.show" :message="snackbar.text" :color="snackbar.color" />
  </v-container>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useProject } from '@/composables/useProject';
import { useInstallments } from '@/composables/useInstallments';
import { useProjectStatus } from '@/composables/useProjectStatus';
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

        const { getProjectStatus, getStatusColor } = useProjectStatus();

        return {
            project,
            projectLoading,
            installments,
            installmentsLoading,
            getProjectStatus,
            getStatusColor,

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