import { IUser } from '@/interface/IUser';

import api from './api';

const fetchDataUser = async () => {
    const response = await api.get<IUser>('/auth/me/', {
        headers: {
            'Content-Type': 'application/json',
        },
    });

    if (response.status !== 200) {
        throw new Error('Ops! Ocorreu um erro ao buscar os dados do usuário.');
    }

    return response.data;
};

export default fetchDataUser;
