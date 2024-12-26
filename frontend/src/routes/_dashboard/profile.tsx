import { createFileRoute } from '@tanstack/react-router';

import { ProfilePage } from '@/pages';

export const Route = createFileRoute('/_dashboard/profile')({
    component: ProfilePage,
});
