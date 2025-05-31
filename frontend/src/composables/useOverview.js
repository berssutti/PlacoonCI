import { ref } from 'vue';
import axios from 'axios';

export function useOverview() {
  const overview = ref(null);
  const loading = ref(false);
  const error = ref(null);

  const fetchOverview = async (year) => {
    loading.value = true;
    error.value = null;

    try {
      const response = await axios.get(`http://localhost:8000/api/projects/overview/?year=${year}`);
      overview.value = response.data;
    } catch (err) {
      error.value = err.message || 'Erro ao carregar dados da visão geral';
      console.error('Error fetching overview:', err);
    } finally {
      loading.value = false;
    }
  };

  return {
    overview,
    loading,
    error,
    fetchOverview
  };
} 