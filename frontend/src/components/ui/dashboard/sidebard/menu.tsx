import { Link } from '@tanstack/react-router';
import { Home, LogOut, User } from 'lucide-react';

import {
    Accordion,
    AccordionContent,
    AccordionItem,
    AccordionTrigger,
} from '@/components/ui/accordion';
import { Separator } from '@/components/ui/separator';
import { handleLogout } from '@/utils/logout';

import { links } from './links';

type MenuSidebarProps = {
    isOpen?: (value: boolean) => void;
};

const MenuSidebar = ({ isOpen }: MenuSidebarProps) => {
    return (
        <Accordion type="single" collapsible className="w-full">
            <div className="flex flex-1 items-center justify-between py-4 text-left text-sm font-medium transition-all hover:underline">
                <Link
                    onClick={() => isOpen && isOpen(false)}
                    to="/dashboard"
                    activeProps={{
                        className: 'underline',
                    }}
                    className="flex w-full items-center space-x-4 text-secondary"
                >
                    <Home className="mr-2 size-6 text-secondary" />
                    Início
                </Link>
            </div>
            <Separator className="bg-slate-50/20" />
            {links.map((link) => (
                <AccordionItem value={link.name} key={link.to}>
                    <AccordionTrigger>
                        <Link
                            onClick={() => isOpen && isOpen(false)}
                            to={link.to}
                            activeProps={{
                                className: 'underline',
                            }}
                            className="flex w-4/5 items-center space-x-4 text-secondary"
                        >
                            <link.icon className="mr-2 size-6 text-secondary" />
                            {link.name}
                        </Link>
                    </AccordionTrigger>
                    <AccordionContent>
                        <div className="p-4">
                            {link.subLinks &&
                                link.subLinks.map((subLink) => (
                                    <Link
                                        onClick={() => isOpen && isOpen(false)}
                                        key={subLink.to}
                                        activeProps={{
                                            className: 'underline',
                                        }}
                                        to={subLink.to}
                                        className="flex py-2 pl-4 text-secondary hover:underline"
                                    >
                                        <subLink.icon className="mr-2 size-6 text-secondary" />
                                        {subLink.name}
                                    </Link>
                                ))}
                        </div>
                    </AccordionContent>
                </AccordionItem>
            ))}
            <AccordionItem value="Perfil" className="lg:hidden">
                <AccordionTrigger>
                    <Link
                        onClick={() => isOpen && isOpen(false)}
                        to="/profile"
                        activeProps={{
                            className: 'underline',
                        }}
                        className="flex w-4/5 items-center space-x-4 text-secondary"
                    >
                        <User className="mr-2 size-6 text-secondary" />
                        Perfil
                    </Link>
                </AccordionTrigger>
                <AccordionContent>
                    <div className="p-4">
                        <Link
                            onClick={() => isOpen && isOpen(false)}
                            to="/profile"
                            className="flex py-2 pl-4 text-secondary hover:underline"
                        >
                            <User className="mr-2 size-6 text-secondary" />
                            Perfil
                        </Link>
                        <button
                            type="button"
                            className="flex py-2 pl-4 text-secondary hover:underline"
                            onClick={handleLogout}
                        >
                            <LogOut className="mr-2 size-6 text-secondary" />
                            Sair
                        </button>
                    </div>
                </AccordionContent>
            </AccordionItem>
        </Accordion>
    );
};

export default MenuSidebar;
