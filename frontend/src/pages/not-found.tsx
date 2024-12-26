import { useNavigate } from '@tanstack/react-router';
import { useEffect, useState } from 'react';

import Logo from '@/assets/images/logo.svg?react';
import { isLogged } from '@/helpers/cookies';

const NotFoundPage = () => {
    const [time, setTime] = useState(5);
    const navigate = useNavigate();

    useEffect(() => {
        if (isLogged()) {
            const interval = setInterval(() => {
                setTime((prev) => prev - 1);
            }, 1000);

            if (time === 0) {
                navigate({ to: '/dashboard' });
            }

            return () => clearInterval(interval);
        }
    }, [time, navigate]);

    return (
        <main className="flex h-dvh items-center justify-center">
            <section className="flex flex-col items-center justify-center gap-2">
                <div className="flex flex-col items-center gap-2">
                    <Logo className="size-16 text-primary" />
                    <h1 className="text-3xl font-bold">Sistema Fly</h1>
                </div>
                <div className="text-center">
                    <h1 className="text-4xl font-bold">404</h1>
                    <p className="text-lg">Pagina não encontrada</p>
                </div>
                {isLogged() && (
                    <div className="text-center">
                        <p className="text-lg">
                            Você será redirecionado para a página inicial em{' '}
                            {time} segundos
                        </p>
                    </div>
                )}
                {!isLogged() && (
                    <div className="text-center">
                        <p className="text-lg">
                            <a
                                href="/"
                                className="text-primary hover:underline"
                            >
                                Clique aqui
                            </a>{' '}
                            para voltar a página inicial
                        </p>
                    </div>
                )}
            </section>
        </main>
    );
};

export default NotFoundPage;
