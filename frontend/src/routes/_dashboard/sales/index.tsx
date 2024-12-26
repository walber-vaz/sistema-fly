import { createFileRoute } from '@tanstack/react-router';

import { SalesPage } from '@/pages';

export const Route = createFileRoute('/_dashboard/sales/')({
    component: SalesPage,
});
