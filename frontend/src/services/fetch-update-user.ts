import axios from 'axios';

import type { IUserUpdate } from '@/interface/IUser';

import api from './api';

type Response = {
    message: string;
    detail?: string;
};

const fetchUpdateUser = async (data: IUserUpdate) => {
    try {
        const response = await api.patch<Response>('/users/update/', data);

        return response.data;
    } catch (error) {
        if (axios.isAxiosError(error) && error.response) {
            throw new Error(error.response.data.detail);
        } else {
            throw new Error('An unknown error occurred');
        }
    }
};

export default fetchUpdateUser;
