import api from './api';

export const projectService = {
    getAllProjects(year = null) {
        const params = {};
        if (year) {
            params.active_year = year;
        }
        return api.get('/projects/', { params });
    },

    getAvailableYears() {
        return api.get('/projects/available-years/');
    },

    getProject(id) {
        return api.get(`/projects/${id}/`);
    },

    createProject(data) {
        return api.post('/projects/', data);
    },

    updateProject(id, data) {
        return api.put(`/projects/${id}/`, data);
    },

    deleteProject(id) {
        return api.delete(`/projects/${id}/`);
    }
};