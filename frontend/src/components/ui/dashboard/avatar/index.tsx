import { Link } from '@tanstack/react-router';
import { LogOut, User } from 'lucide-react';

import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuLabel,
    DropdownMenuSeparator,
    DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { useUser } from '@/stores/user';
import { handleLogout } from '@/utils/logout';

export const Avatar = () => {
    const { user } = useUser();

    return (
        <div className="flex items-center justify-center space-x-2 lg:space-x-4">
            <span className="select-none text-sm text-zinc-600 lg:text-base">
                {user?.first_name} {user?.surname}
            </span>
            <DropdownMenu>
                <DropdownMenuTrigger asChild>
                    <button className="flex items-center rounded-full border p-2 focus:outline-primary">
                        <User className="text-zinc-600" size={24} />
                    </button>
                </DropdownMenuTrigger>
                <DropdownMenuContent className="w-28" align="end">
                    <DropdownMenuLabel className="text-zinc-600">
                        Minha Conta
                    </DropdownMenuLabel>
                    <DropdownMenuSeparator />
                    <DropdownMenuItem asChild>
                        <Link
                            to="/profile"
                            className="w-full cursor-pointer text-zinc-600"
                        >
                            <User className="text-zinc-600" />
                            Perfil
                        </Link>
                    </DropdownMenuItem>
                    <DropdownMenuItem asChild>
                        <button
                            type="button"
                            className="w-full cursor-pointer text-zinc-600"
                            onClick={handleLogout}
                        >
                            <LogOut className="text-zinc-600" />
                            Sair
                        </button>
                    </DropdownMenuItem>
                </DropdownMenuContent>
            </DropdownMenu>
        </div>
    );
};
