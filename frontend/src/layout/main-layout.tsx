import { useQuery } from '@tanstack/react-query';
import { Outlet, useNavigate, useRouterState } from '@tanstack/react-router';
import { useEffect } from 'react';

import { Avatar } from '@/components/ui/dashboard/avatar';
import { Sidebar } from '@/components/ui/dashboard/sidebard';
import SidebarMobile from '@/components/ui/dashboard/sidebard/sidebar-mobile';
import { isLogged } from '@/helpers/cookies';
import fetchDataUser from '@/services/fetch-data-user';
import { useUser } from '@/stores/user';
import { titlePageLocation } from '@/utils/title-pathname';

export const MainLayout = () => {
    const { user, setUser } = useUser();
    const { data: userQuery } = useQuery({
        queryKey: ['user'],
        queryFn: fetchDataUser,
        enabled: !!user || isLogged(),
    });
    const navigate = useNavigate();
    const { location } = useRouterState();

    useEffect(() => {
        if (userQuery) {
            setUser(userQuery);
        }
    }, [userQuery, user, setUser]);

    useEffect(() => {
        const checkAuthentication = () => {
            if (!isLogged()) {
                navigate({ to: '/' });
            }
        };

        checkAuthentication();

        const intervalId = setInterval(checkAuthentication, 1000);

        const handleStorageChange = () => {
            checkAuthentication();
        };

        const handleVisibilityChange = () => {
            if (document.visibilityState === 'visible') {
                checkAuthentication();
            }
        };

        window.addEventListener('storage', handleStorageChange);
        document.addEventListener('visibilitychange', handleVisibilityChange);

        return () => {
            clearInterval(intervalId);
            window.removeEventListener('storage', handleStorageChange);
            document.removeEventListener(
                'visibilitychange',
                handleVisibilityChange,
            );
        };
    }, [navigate]);

    return (
        <main className="flex w-full">
            <Sidebar />
            <section className="ml-0 flex min-h-dvh w-full flex-1 flex-col lg:ml-52">
                <div className="flex w-full items-center justify-between border-b border-slate-200/70 p-4">
                    <div className="lg:hidden">
                        <SidebarMobile />
                    </div>
                    <h1 className="ml-auto text-xl font-bold text-zinc-600 lg:ml-0 lg:text-2xl">
                        {titlePageLocation(location)}
                    </h1>
                    <div className="ml-auto hidden lg:block">
                        <Avatar />
                    </div>
                </div>
                <div className="p-4">
                    <Outlet />
                </div>
            </section>
        </main>
    );
};
