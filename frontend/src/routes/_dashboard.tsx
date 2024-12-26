import { createFileRoute, redirect } from '@tanstack/react-router';

import { isLogged } from '@/helpers/cookies';
import { MainLayout } from '@/layout/main-layout';

export const Route = createFileRoute('/_dashboard')({
    component: MainLayout,
    beforeLoad: async () => {
        if (!isLogged()) {
            throw redirect({
                to: '/',
            });
        }
    },
});
