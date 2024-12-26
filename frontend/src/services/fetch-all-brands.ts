import axios from 'axios';

import { IBrands } from '@/interface/IBrand';

import api from './api';

const fetchAllBrands = async () => {
    try {
        const response = await api.get<IBrands>('/products/brands/list/', {
            headers: {
                'Content-Type': 'application/json',
            },
        });

        return response.data;
    } catch (error) {
        if (axios.isAxiosError(error) && error.response) {
            throw new Error(error.response.data.detail);
        } else {
            throw new Error(
                'Ops! Tivemos um problema. Tente novamente mais tarde.',
            );
        }
    }
};

export default fetchAllBrands;
