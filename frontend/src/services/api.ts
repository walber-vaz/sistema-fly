import axios from 'axios';

import { getCookie, removeCookie } from '@/helpers/cookies';

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
});

api.interceptors.request.use(
    (config) => {
        const token = getCookie();

        if (!token && !config.url?.includes('/login')) {
            window.location.href = '/';
            return Promise.reject();
        }

        if (!config.url?.includes('/login')) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error),
);

api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            removeCookie();
            window.location.href = '/';
        }
        return Promise.reject(error);
    },
);

export default api;
