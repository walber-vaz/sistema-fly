import axios from 'axios';

import { ICategories } from '@/interface/ICategory';

import api from './api';

const fetchAllCategories = async () => {
    try {
        const response = await api.get<ICategories>(
            '/products/categories/list/',
            {
                headers: {
                    'Content-Type': 'application/json',
                },
            },
        );

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

export default fetchAllCategories;
