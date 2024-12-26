import axios from 'axios';

import type { ILoginResponse } from '@/interface/ILoginResponse';

import api from './api';

export type LoginData = {
    email: string;
    password: string;
};

const fetchLogin = async (loginData: LoginData) => {
    try {
        const params = new URLSearchParams();
        params.append('username', loginData.email);
        params.append('password', loginData.password);

        const response = await api.post<ILoginResponse>(
            '/auth/login/',
            params.toString(),
            {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
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

export default fetchLogin;
