<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card elevation="2" class="rounded-lg">
          <v-card-title class="text-h4 primary--text py-4 px-6">
            <v-icon large class="mr-2">mdi-folder-multiple</v-icon>
            Lista de Projetos
          </v-card-title>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mt-4">
      <v-col cols="12" md="8">
        <ProjectFilter
          :years="years"
          :initial-filters="initialFilters"
          @update:filters="updateFilters"
        />
      </v-col>
      <v-col cols="12" md="4" class="text-right">
        <v-btn 
          color="primary"
          size="x-large"
          elevation="2" 
          class="rounded-lg" 
          @click="goToCreateProject"
        >
          <v-icon left>mdi-plus</v-icon>
          Cadastrar Novo Projeto
        </v-btn>
      </v-col>
    </v-row>

    <template v-if="!loading">
      <v-row v-if="filteredProjects.length > 0" class="mt-4">
        <v-col
          v-for="project in paginatedProjects"
          :key="project.id"
          cols="12"
          md="4"
          class="mb-4"
        >
          <ProjectCard
            :project="project"
            @click="viewProjectDetails(project.id)"
          />
        </v-col>
      </v-row>
      
      <v-row v-else justify="center" class="mt-4">
        <v-col cols="12">
          <v-card elevation="2" class="rounded-lg text-center py-6">
            <v-icon size="64" color="grey lighten-1">mdi-folder-search-outline</v-icon>
            <div class="text-h6 grey--text mt-4">Nenhum projeto encontrado.</div>
            <div class="text-body-2 grey--text text--lighten-1 mt-2">Tente ajustar os filtros ou criar um novo projeto.</div>
          </v-card>
        </v-col>
      </v-row>

      <v-row v-if="filteredProjects.length > 0" justify="center" class="mt-4">
        <v-pagination
          v-model="currentPage"
          :length="totalPages"
          total-visible="5"
          color="primary"
          circle
        ></v-pagination>
      </v-row>
    </template>

    <v-row v-if="loading" justify="center" class="mt-4">
      <v-col cols="12" class="text-center py-6">
        <v-progress-circular indeterminate size="64" color="primary"></v-progress-circular>
        <div class="text-h6 grey--text mt-4">Carregando projetos...</div>
      </v-col>
    </v-row>

    <v-row v-if="error" justify="center" class="mt-4">
      <v-col cols="12">
        <v-alert type="error" elevation="2" class="rounded-lg">{{ error }}</v-alert>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted, watchEffect } from 'vue';
import { useRouter } from 'vue-router';
import { useProject } from '@/composables/useProject';
import ProjectFilter from '@/components/project/list/ProjectFilter.vue';
import ProjectCard from '@/components/project/list/ProjectCard.vue';

const router = useRouter();
const { project: projects, loading, error, fetchProject } = useProject();

const initialFilters = ref({
  searchQuery: '',
  selectedYear: new Date().getFullYear(),
  currentPage: 1
});

const savedState = sessionStorage.getItem('projectsListState');
if (savedState) {
  const state = JSON.parse(savedState);
  initialFilters.value = {
    searchQuery: state.searchQuery || '',
    selectedYear: Number(state.selectedYear) || new Date().getFullYear(),
    currentPage: Number(state.currentPage) || 1
  };
}

const searchQuery = ref(initialFilters.value.searchQuery);
const selectedYear = ref(initialFilters.value.selectedYear);
const years = ref([]);
const currentPage = ref(initialFilters.value.currentPage);
const itemsPerPage = 6;

const filteredProjects = computed(() => {
  if (!projects.value) return [];

  return projects.value.filter((project) => {
    const projectYearStart = new Date(project.start_date).getFullYear();
    const projectYearEnd = new Date(project.end_date).getFullYear();
    const isYearInRange =
      (Number(selectedYear.value) >= projectYearStart && Number(selectedYear.value) <= projectYearEnd);
    
    const isKeywordMatch = (project.description + project.name + project.coordinator + project.processo_sei)
      .toLowerCase()
      .includes((searchQuery.value || '').toLowerCase());
      
    return isYearInRange && isKeywordMatch;
  });
});

const paginatedProjects = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return filteredProjects.value.slice(start, end);
});

const totalPages = computed(() => {
  return Math.max(1, Math.ceil(filteredProjects.value.length / itemsPerPage));
});

const formatDate = (dateString) => {
  const options = { day: '2-digit', month: '2-digit', year: 'numeric' };
  return new Date(dateString + 'T00:00:00').toLocaleDateString('pt-BR', options);
};

const getProjectStatus = (project) => {
  const start = new Date(project.start_date);
  const end = new Date(project.end_date);
  const today = new Date();
  
  if (today < start) return "Não Iniciado";
  if (today > end) return "Concluído";
  return "Em Andamento";
};

const getStatusColor = (project) => {
  const status = getProjectStatus(project);
  if (status === "Não Iniciado") return "grey";
  if (status === "Em Andamento") return "primary";
  return "success";
};

const getStatusIcon = (project) => {
  const status = getProjectStatus(project);
  if (status === "Não Iniciado") return "mdi-clock-outline";
  if (status === "Em Andamento") return "mdi-progress-clock";
  return "mdi-check-circle-outline";
};

const getRemainingTime = (project) => {
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

const fetchProjects = async () => {
  try {
    await fetchProject();
    years.value = getYearRange();
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
};

const getYearRange = () => {
  if (!projects.value || projects.value.length === 0) 
    return [new Date().getFullYear()];

  const currentYear = new Date().getFullYear();
  let maxEndYear = currentYear;
  let minStartYear = currentYear;

  projects.value.forEach(project => {
    const projectEndDate = new Date(project.end_date + 'T00:00:00');
    const projectStartDate = new Date(project.start_date + 'T00:00:00');

    const projectEndYear = projectEndDate.getFullYear();
    const projectStartYear = projectStartDate.getFullYear();

    maxEndYear = Math.max(maxEndYear, projectEndYear);
    minStartYear = Math.min(minStartYear, projectStartYear);
  });

  return Array.from({ length: maxEndYear - minStartYear + 1 }, (_, i) => minStartYear + i);
};

const goToCreateProject = () => {
  router.push({ name: 'ProjectCreate'}); 
};

const viewProjectDetails = (projectId) => {
  const state = {
    searchQuery: searchQuery.value,
    selectedYear: selectedYear.value,
    currentPage: currentPage.value,
  };
  sessionStorage.setItem('projectsListState', JSON.stringify(state));
  router.push({ name: 'ProjectDetails', params: { id: projectId } });
};

const updateFilters = (filters) => {
  searchQuery.value = filters.searchQuery;
  selectedYear.value = filters.selectedYear;
  currentPage.value = 1;

  const state = {
    searchQuery: filters.searchQuery,
    selectedYear: filters.selectedYear,
    currentPage: currentPage.value,
  };
  sessionStorage.setItem('projectsListState', JSON.stringify(state));
};

onMounted(fetchProjects);
</script>

<style scoped>
.v-card {
  transition: transform 0.3s, box-shadow 0.3s;
}

.v-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1) !important;
}

.project-card {
  cursor: pointer;
}

.h-100 {
  height: 100%;
}

.rounded-lg {
  border-radius: 12px !important;
}
</style>