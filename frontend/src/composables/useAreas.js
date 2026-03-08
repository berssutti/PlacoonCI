import { ref } from 'vue';
import { areaService } from '@/services/areaService';

export function useAreas() {
    const areas = ref([]);
    const loading = ref(false);
    const error = ref(null);

    const fetchAreas = async () => {
        loading.value = true;
        try {
            const response = await areaService.getAreas();
            areas.value = response.data;
        } catch (err) {
            error.value = 'Erro ao carregar lista de áreas';
            console.error(err);
        } finally {
            loading.value = false;
        }
    };

    const getAreaIdByName = (areaName) => {
        const area = areas.value.find((item) => item.name === areaName);
        return area ? area.id : null;
    };

    const getAreaNameById = (areaId) => {
        const area = areas.value.find((item) => item.id === areaId);
        return area ? area.name : '';
    };

    return {
        areas,
        loading,
        error,
        fetchAreas,
        getAreaIdByName,
        getAreaNameById
    };
}
