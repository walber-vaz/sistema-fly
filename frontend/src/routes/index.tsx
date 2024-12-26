import { createFileRoute, redirect } from '@tanstack/react-router';

import { isLogged } from '@/helpers/cookies';
import { LoginPage } from '@/pages';

export const Route = createFileRoute('/')({
    component: LoginPage,
    beforeLoad: async () => {
        if (isLogged()) {
            throw redirect({
                to: '/dashboard',
            });
        }
    },
});
