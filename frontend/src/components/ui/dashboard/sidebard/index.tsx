import Logo from '@/assets/images/logo.svg?react';
import { Separator } from '@/components/ui/separator';

import MenuSidebar from './menu';

export const Sidebar = () => {
    return (
        <aside className="fixed hidden min-h-dvh w-full max-w-48 flex-col items-center bg-primary px-3 py-4 lg:flex lg:max-w-52">
            <div className="flex flex-col items-center">
                <Logo className="size-12 text-secondary" />
                <h2 className="text-lg font-semibold text-secondary">
                    Sistema Fly
                </h2>
            </div>
            <Separator className="my-4 bg-slate-50/20" />
            <div className="flex w-full flex-col items-center">
                <MenuSidebar />
            </div>
        </aside>
    );
};
