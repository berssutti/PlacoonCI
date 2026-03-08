import { ref } from 'vue';
import { projectService } from '@/services/projectService';

export function useProject() {
    const project = ref(null);
    const loading = ref(false);
    const error = ref(null);

    const fetchProject = async (id = null, year = null) => {
        loading.value = true;
        let response = null;

        try {
            id ? response = await projectService.getProject(id) : response = await projectService.getAllProjects(year);
            project.value = response.data;
        } catch (err) {
            error.value = 'Erro ao carregar projeto';
            console.error(err);
        } finally {
            loading.value = false;
        }
    };

    const availableYears = ref([]);
    const totalProjects = ref(0);

    const fetchAvailableYears = async () => {
        // Don't set global loading since this is often a background/filter operation
        try {
            const response = await projectService.getAvailableYears();
            availableYears.value = response.data.years;
            totalProjects.value = response.data.count;
        } catch (err) {
            console.error('Erro ao carregar anos disponíveis:', err);
            // Fallback to current year if fails
            availableYears.value = [new Date().getFullYear()];
        }
    };

    const deleteProject = async (id) => {
        loading.value = true;

        try {
            await projectService.deleteProject(id);
            if (Array.isArray(project.value)) {
                project.value = project.value.filter(project => project.id !== id);
            }
        } catch (err) {
            error.value = 'Erro ao deletar projeto';
            console.error(err);
        } finally {
            loading.value = false;
        }
    };

    return {
        project,
        loading,
        error,
        fetchProject,
        deleteProject,
        availableYears,
        totalProjects,
        fetchAvailableYears
    };
}