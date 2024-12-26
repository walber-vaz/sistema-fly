import { Menu } from 'lucide-react';
import { useState } from 'react';

import Logo from '@/assets/images/logo.svg?react';
import { Button } from '@/components/ui/button';
import { Separator } from '@/components/ui/separator';
import {
    Sheet,
    SheetContent,
    SheetDescription,
    SheetHeader,
    SheetTitle,
    SheetTrigger,
} from '@/components/ui/sheet';

import MenuSidebar from './menu';

const SidebarMobile = () => {
    const [isOpen, setIsOpen] = useState(false);
    return (
        <Sheet open={isOpen} onOpenChange={setIsOpen}>
            <SheetTrigger asChild>
                <Button variant={'outline'}>
                    <Menu size={24} className="text-primary" />
                </Button>
            </SheetTrigger>
            <SheetContent side={'left'} className="border-primary bg-primary">
                <SheetHeader className="flex flex-col items-center justify-center">
                    <SheetTitle>
                        <Logo className="text-secondary" />
                    </SheetTitle>
                    <SheetDescription className="text-lg font-semibold text-secondary">
                        Sistema Fly
                    </SheetDescription>
                </SheetHeader>
                <Separator className="my-4 bg-slate-50/20" />
                <MenuSidebar isOpen={setIsOpen} />
            </SheetContent>
        </Sheet>
    );
};

export default SidebarMobile;
