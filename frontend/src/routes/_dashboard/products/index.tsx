import { createFileRoute } from '@tanstack/react-router';

import { ProductsPage } from '@/pages';

export const Route = createFileRoute('/_dashboard/products/')({
    component: ProductsPage,
});
