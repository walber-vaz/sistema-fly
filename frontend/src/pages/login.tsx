import Logo from '@/assets/images/logo.svg?react';
import { FormLogin } from '@/components/ui/login/form';

const LoginPage = () => {
    return (
        <main className="grid min-h-dvh lg:grid-cols-2">
            <section className="flex flex-col gap-4 p-6 md:p-10">
                <div className="flex flex-1 items-center justify-center">
                    <div className="w-full max-w-xs">
                        <FormLogin />
                    </div>
                </div>
            </section>
            <section className="hidden bg-primary lg:block">
                <div className="flex h-dvh flex-col items-center justify-center">
                    <Logo className="size-24 text-secondary" />
                    <h1 className="text-5xl font-bold text-white">
                        Sistema Fly
                    </h1>
                    <p className="text-secondary/60">
                        Seu sistema de gerenciamento de produtos, vendas e
                        clientes.
                    </p>
                </div>
            </section>
        </main>
    );
};

export default LoginPage;
