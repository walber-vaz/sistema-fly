import { createFileRoute } from '@tanstack/react-router';

import { ProductPageCreate } from '@/pages';

export const Route = createFileRoute('/_dashboard/products/create')({
    component: ProductPageCreate,
});
