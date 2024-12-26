import { createFileRoute } from '@tanstack/react-router';

import { ClientsPage } from '@/pages';

export const Route = createFileRoute('/_dashboard/clients/')({
    component: ClientsPage,
});
