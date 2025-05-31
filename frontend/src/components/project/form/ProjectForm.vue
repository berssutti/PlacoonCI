<template>
  <v-container>
    <v-card elevation="2" class="pa-4">
      <v-card-title class="text-h5 font-weight-bold">
        {{ isEditing ? 'Editar Projeto' : 'Novo Projeto' }}
      </v-card-title>
      <v-divider></v-divider>

      <v-card-text>
        <v-form @submit.prevent="saveProject">
          <h4 class="mb-3">Informações Gerais</h4>
          <v-row>
            <v-col cols="12" md="6">
              <v-text-field v-model="project.name" label="Nome do Projeto" counter maxlength="100"
                :rules="[rules.required, rules.maxLength(100)]" placeholder="Digite o nome do projeto"
                prepend-inner-icon="mdi-file-document-outline" required></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-textarea v-model="project.description" label="Descrição"
                :rules="[rules.required, rules.maxLength(200)]" placeholder="Descreva brevemente o projeto"
                prepend-inner-icon="mdi-text-box-outline" rows="1" auto-grow counter maxlength="200"
                required></v-textarea>
            </v-col>
          </v-row>

          <v-row>
            <v-col cols="12" md="6">
              <v-text-field v-model="project.processo_sei" label="Processo SEI" placeholder="*****.******/****-**"
                :rules="[rules.required, rules.seiFormat]" prepend-inner-icon="mdi-file-document-multiple-outline"
                required></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-select v-model="project.status" :items="statusOptions" label="Status"
                prepend-inner-icon="mdi-flag-outline" @change="validateStatus"></v-select>
            </v-col>
          </v-row>

          <v-row>
            <v-col cols="12" md="6">
              <v-text-field v-model="project.start_date" label="Data de Início" type="date"
                prepend-inner-icon="mdi-calendar-start" :rules="[rules.required]" required></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field v-model="project.end_date" label="Data de Término" type="date"
                prepend-inner-icon="mdi-calendar-end" :rules="[rules.required]" required></v-text-field>
            </v-col>
          </v-row>

          <div v-if="project.status === 'Recebido'">
            <h4 class="mb-3">Célula Orçamentária</h4>
            <v-row>
              <v-col cols="12" md="4">
                <v-text-field v-model="project.nota_dotacao" label="Nota de Dotação"
                  prepend-inner-icon="mdi-note-text-outline" :rules="[rules.required]" required></v-text-field>
              </v-col>
              <v-col cols="12" md="4">
                <v-text-field v-model="project.ptres" label="PTRES" prepend-inner-icon="mdi-identifier"
                  :rules="[rules.required]" required></v-text-field>
              </v-col>
              <v-col cols="12" md="4">
                <v-text-field v-model="project.ugr" label="UGR" prepend-inner-icon="mdi-office-building-outline"
                  :rules="[rules.required]" required></v-text-field>
              </v-col>
            </v-row>
          </div>

          <h4 class="mb-3">Gestão</h4>
          <v-row>
            <v-col cols="12" md="4">
              <v-text-field v-model="project.coordinator" label="Coordenador"
                :rules="[rules.required, rules.maxLength(100)]" prepend-inner-icon="mdi-account-tie"
                placeholder="Nome do coordenador" counter maxlength="100" required></v-text-field>
            </v-col>
            <v-col cols="12" md="4">
              <v-text-field v-model="project.substitute_coordinator" label="Coordenador Substituto"
                :rules="[rules.required, rules.maxLength(100)]" placeholder="Nome do coordenador substituto"
                prepend-inner-icon="mdi-account-switch" counter maxlength="100" required></v-text-field>
            </v-col>
            <v-col cols="12" md="4">
              <v-text-field v-model="project.academic_supervisor" label="Supervisor Acadêmico"
                :rules="[rules.required, rules.maxLength(100)]" placeholder="Nome do supervisor acadêmico"
                prepend-inner-icon="mdi-school" counter maxlength="100" required></v-text-field>
            </v-col>
          </v-row>

          <h4 class="mb-3">Orçamento</h4>
          <v-row>
            <v-col cols="12" md="6">
              <v-text-field v-model="project.total_unb_amount_expected" label="Custos Indiretos UnB" type="number"
                prefix="R$" :rules="[rules.required, rules.positive]" prepend-inner-icon="mdi-cash-multiple"
                placeholder="Valor esperado para UnB" required></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field v-model="project.total_fcte_amount_expected" label="Custos Indiretos FCTE" type="number"
                prefix="R$" :rules="[rules.required, rules.positive]" prepend-inner-icon="mdi-cash-multiple"
                placeholder="Valor esperado para FCTE" required></v-text-field>
            </v-col>
          </v-row>


          <h4 class="mb-3">Áreas</h4>
          <v-row v-for="(area, index) in project.areas" :key="index">
            <v-col cols="6">
              <v-select v-model="area.id" :items="filteredAreaList(index)" item-title="name" item-value="id"
                label="Área" prepend-inner-icon="mdi-shape-outline" :rules="[rules.required]" required></v-select>
            </v-col>
            <v-col cols="4">
              <v-text-field v-model.number="area.percentage" label="Porcentagem" type="number" suffix="%"
                :rules="[rules.required, rules.percentage]" required></v-text-field>
            </v-col>
            <v-col cols="2" class="text-center">
              <v-btn icon color="red" @click="removeArea(index)">
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </v-col>
          </v-row>
          <v-btn color="secondary" @click="addArea" class="mb-4" prepend-icon="mdi-plus">Adicionar Área</v-btn>

          <v-divider class="my-4"></v-divider>

          <v-row>
            <v-col cols="12" class="text-right">
              <v-btn color="grey" class="mr-2" @click="$router.back()">Cancelar</v-btn>
              <v-btn type="submit" color="primary">Salvar</v-btn>
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useProject } from '@/composables/useProject';
import { useInstallments } from '@/composables/useInstallments';

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
const statusOptions = ref(['Processando', 'Recebido']);
const isEditing = ref(false);


const rules = {
  required: (value) => !!value || 'Campo obrigatório.',
  maxLength: (max) => (value) => value.length <= max || `Máximo de ${max} caracteres.`,
  positive: (value) => parseFloat(value) > 0 || 'Deve ser um número positivo.',
  seiFormat: (value) => /^\d{5}\.\d{6}\/\d{4}-\d{2}$/.test(value) ||
    'Formato inválido. Use: *****.******/****-**',
  percentage: (value) => value >= 0 && value <= 100 || 'A porcentagem deve estar entre 0 e 100.',
};

const filteredAreaList = (index) => {
  const selectedAreas = project.value.areas
    .map((a, i) => (i !== index ? a.id : null))
    .filter((id) => id);
  return areaList.value.filter((area) => !selectedAreas.includes(area.id));
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

const validateStatus = () => {
  if (
    project.value.status === 'Recebido' &&
    (!project.value.nota_dotacao || !project.value.ptres || !project.value.ugr)
  ) {
    alert(
      'Para alterar o status para "Recebido", é necessário preencher os campos Nota de Dotação, PTRES e UGR.'
    );
    project.value.status = 'Processando';
  }
};

const saveProject = async () => {
  try {
    if (
      project.value.status === 'Recebido' &&
      (!project.value.nota_dotacao || !project.value.ptres || !project.value.ugr)
    ) {
      alert(
        'Para salvar com o status "Recebido", preencha os campos Nota de Dotação, PTRES e UGR.'
      );
      return;
    }
    if (!validadePercentage()) {
      alert('A soma das porcentagens das áreas deve ser 100%');
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
      throw new Error('Erro ao salvar projeto');
    }

    const projectData = await response.json();
    router.push(`/projects/${isEditing.value ? props.id : projectData.id}`);
  } catch (error) {
    console.error('Erro:', error);
    alert('Ocorreu um erro ao salvar o projeto. Tente novamente.');
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