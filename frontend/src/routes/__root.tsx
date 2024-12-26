import { createRootRoute, Outlet } from '@tanstack/react-router';
import React, { Suspense } from 'react';

import { NotFoundPage } from '@/pages';

const loadDevtools = () =>
    Promise.all([import('@tanstack/react-query-devtools')]).then(
        ([reactQueryDevtools]) => {
            return {
                default: () => (
                    <>
                        <reactQueryDevtools.ReactQueryDevtools />
                    </>
                ),
            };
        },
    );

const TanStackDevtools =
    process.env.NODE_ENV === 'production'
        ? () => null
        : React.lazy(loadDevtools);

export const Route = createRootRoute({
    component: () => (
        <>
            <Outlet />
            <Suspense>
                <TanStackDevtools />
            </Suspense>
        </>
    ),
    notFoundComponent: () => <NotFoundPage />,
});
