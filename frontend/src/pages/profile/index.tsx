import { Link } from '@tanstack/react-router';
import { User } from 'lucide-react';

import { Separator } from '@/components/ui/separator';
import { useUser } from '@/stores/user';

import FormProfile from './form-profile';

const ProfilePage = () => {
    const { user } = useUser();

    return (
        <div className="mx-auto flex h-[calc(100dvh-8.5rem)] w-full flex-col lg:container lg:flex-row">
            <div className="border-b border-primary/30 text-slate-700 lg:mt-8 lg:border-none">
                <nav>
                    <ul className="flex flex-row items-center justify-start gap-4 py-4 lg:flex-col lg:items-start lg:px-8 lg:py-0">
                        <Link
                            to="/profile"
                            activeProps={{ className: 'text-primary' }}
                            className="flex items-center gap-2"
                        >
                            <User size={24} />
                            Perfil
                        </Link>
                    </ul>
                </nav>
            </div>
            <Separator
                orientation="vertical"
                className="mt-6 hidden bg-primary/30 lg:block"
            />
            <div className="mt-8 flex w-full flex-1 flex-col px-8">
                <div className="flex flex-col items-center justify-start gap-2 lg:flex-row">
                    <div className="flex size-14 items-center justify-center rounded-full border">
                        <User size={30} className="text-slate-700" />
                    </div>
                    <div className="-space-y-2">
                        <p className="text-xl font-bold text-slate-700">
                            {user?.first_name} {user?.surname}
                        </p>
                        <small className="text-sm text-slate-500">
                            {user?.email}
                        </small>
                    </div>
                </div>
                <div className="mt-8 w-full lg:max-w-60">
                    <FormProfile />
                </div>
            </div>
        </div>
    );
};

export default ProfilePage;
