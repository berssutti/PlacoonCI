import axios from 'axios';

const API_URL = 'http://localhost:8000/api/areas/';

export const areaService = {
    getAreas() {
        return axios.get(API_URL);
    }
};
