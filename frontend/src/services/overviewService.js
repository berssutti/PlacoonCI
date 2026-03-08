import axios from 'axios';

const API_URL = 'http://localhost:8000/api/projects/overview/';

export const overviewService = {
    getOverview(year) {
        return axios.get(`${API_URL}?year=${year}`);
    }
};
