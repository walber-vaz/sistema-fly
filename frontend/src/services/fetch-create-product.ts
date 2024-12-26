import axios from 'axios';

import { IProductCreateResponse } from '@/interface/IProducts';

import api from './api';

export type LoginData = {
    name: string;
    description?: string;
    price: string;
    price_sale: string;
    stock: number;
    brand_id?: string;
    category_id?: string;
    image_product?: File;
};

const fetchProductCreate = async (loginData: LoginData) => {
    try {
        const formData = new FormData();
        const params = new URLSearchParams();
        params.append('name', loginData.name);
        params.append('description', loginData.description || '');
        params.append('price', loginData.price);
        params.append('price_sale', loginData.price_sale);
        params.append('stock', loginData.stock.toString());
        params.append('brand_id', loginData.brand_id || '');
        params.append('category_id', loginData.category_id || '');

        if (loginData.image_product) {
            formData.append('image_product', loginData.image_product);
        }

        const response = await api.post<IProductCreateResponse>(
            '/products/create/',
            formData,
            {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
                params,
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

export default fetchProductCreate;
