import axios from 'axios';

import { IProducts } from '@/interface/IProducts';

import api from './api';

type ProductsProps = {
    page?: number;
};

const fetchAllProducts = async ({ page }: ProductsProps) => {
    try {
        const response = await api.get<IProducts>('/products/list/', {
            params: {
                page,
            },
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

export default fetchAllProducts;
