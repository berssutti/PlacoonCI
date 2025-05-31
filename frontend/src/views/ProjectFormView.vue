<template>
  <v-container>
    <v-card elevation="2" class="pa-4">
      <v-card-title class="text-h5 font-weight-bold">
        {{ isEditing ? 'Editar Projeto' : 'Novo Projeto' }}
      </v-card-title>
      <v-divider></v-divider>

      <v-card-text>
        <v-form @submit.prevent="saveProject">
          <GeneralInfo v-model:project="project" :rules="rules" />

          <BudgetInfo v-if="project.status === 'Recebido'" v-model:project="project" :rules="rules" />

          <ManagementInfo v-model:project="project" :rules="rules" />

          <ProjectBudget v-model:project="project" :rules="rules" />

          <AreasSection v-model:areas="project.areas" :areaList="areaList" :rules="rules" @add-area="addArea"
            @remove-area="removeArea" />

          <v-divider class="my-4"></v-divider>

          <ActionButtons @cancel="$router.back()" @save="saveProject" />
        </v-form>
      </v-card-text>
      <FeedbackSnackbar v-model="snackbar.show" :message="snackbar.text" :color="snackbar.color" />

    </v-card>
  </v-container>
</template>
<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useProject } from '@/composables/useProject';
import { useInstallments } from '@/composables/useInstallments';
import GeneralInfo from '@/components/project/form/GeneralInfo.vue';
import BudgetInfo from '@/components/project/form/BudgetInfo.vue';
import ManagementInfo from '@/components/project/form/ManagementInfo.vue';
import ProjectBudget from '@/components/project/form/ProjectBudget.vue';
import AreasSection from '@/components/project/form/AreasSection.vue';
import ActionButtons from '@/components/project/form/ActionButtons.vue';
import FeedbackSnackbar from '@/components/shared/FeedbackSnackbar.vue';

const props = defineProps({
  id: String
});

const router = useRouter();
const { project: projectData, loading: projectLoading, error: projectError, fetchProject } = useProject();
const { installments, loading: installmentsLoading, error: installmentsError, fetchInstallments } = useInstallments();

const project = ref({
  name: '',
  description: '',
  start_date: null,
  end_date: null,
  coordinator: '',
  substitute_coordinator: '',
  academic_supervisor: '',
  processo_sei: '',
  status: 'Processando',
  nota_dotacao: '',
  ptres: '',
  ugr: '',
  total_unb_amount_expected: '',
  total_fcte_amount_expected: '',
  areas: [],
});

const areaList = ref([]);
const isEditing = ref(false);
const snackbar = ref({
  show: false,
  text: '',
  color: 'success'
});


const rules = {
  required: (value) => !!value || 'Campo obrigatório.',
  maxLength: (max) => (value) => value.length <= max || `Máximo de ${max} caracteres.`,
  seiFormat: (value) => /^\d{5}\.\d{6}\/\d{4}-\d{2}$/.test(value) ||
    'Formato inválido. Use: *****.******/****-**',
  percentage: (value) => value >= 0 && value <= 100 || 'A porcentagem deve estar entre 0 e 100.',
};

const showSnackbar = (text, color = 'success') => {
  snackbar.value = {
    show: true,
    text,
    color
  };
};

const fetchProjectDetails = async () => {
  if (props.id) {
    await fetchProject(props.id);

    if (projectData.value) {
      project.value = {
        ...projectData.value,
        areas: projectData.value.areas.map((area) => ({
          id: getAreaIdByName(area.area_name),
          area_name: area.area_name,
          percentage: parseFloat(area.percentage),
        })),
      }
    }
  }
};

const fetchAreas = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/areas/');
    if (!response.ok) throw new Error('Erro ao buscar lista de áreas');
    areaList.value = await response.json();
  } catch (error) {
    console.error('Erro:', error);
  }
};

const getAreaIdByName = (areaName) => {
  const area = areaList.value.find((item) => item.name === areaName);
  return area ? area.id : null;
};

const getAreaNameById = (areaId) => {
  const area = areaList.value.find((item) => item.id === areaId);
  return area ? area.name : '';
};

const addArea = () => {
  project.value.areas.push({ name: '', percentage: 0 });
};

const removeArea = (index) => {
  project.value.areas.splice(index, 1);
};

const validadePercentage = () => {
  const totalPercentage = project.value.areas.reduce(
    (sum, area) => sum + (Number(area.percentage) || 0),
    0
  );
  return totalPercentage === 100;
};

const saveProject = async () => {
  try {
    if (
      project.value.status === 'Recebido' &&
      (!project.value.nota_dotacao || !project.value.ptres || !project.value.ugr)
    ) {
      showSnackbar('Para salvar com o status "Recebido", preencha os campos Nota de Dotação, PTRES e UGR.', 'error');
      return;
    }
    if (!validadePercentage()) {
      showSnackbar('A soma das porcentagens das áreas deve ser 100%', 'error');
      return;
    }

    const url = isEditing.value
      ? `http://localhost:8000/api/projects/${props.id}/`
      : 'http://localhost:8000/api/projects/';
    const method = isEditing.value ? 'PUT' : 'POST';

    const projectPayload = {
      ...project.value,
      areas: project.value.areas.map((area) => ({
        area_name: getAreaNameById(area.id),
        percentage: area.percentage,
      })),
    };

    const response = await fetch(url, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(projectPayload),
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error('Erro ao salvar projeto:', errorData);
    }

    const projectData = await response.json();
    router.push({ name: 'ProjectDetails', params: { id: projectData.id } });
  } catch (error) {
    console.error('Erro:', error);
  }
};

onMounted(async () => {
  await fetchAreas();
  if (props.id) {
    isEditing.value = true;
    await fetchProjectDetails();
    await fetchInstallments(props.id);
  }
});
</script>

<style scoped>
.v-card {
  max-width: 900px;
  margin: auto;
}

h4 {
  font-weight: bold;
  margin-top: 16px;
}

.v-btn {
  text-transform: none;
}
</style>