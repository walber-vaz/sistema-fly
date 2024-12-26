import { zodResolver } from '@hookform/resolvers/zod';
import { useNavigate } from '@tanstack/react-router';
import { Eye, EyeOff } from 'lucide-react';
import { useState } from 'react';
import { useForm } from 'react-hook-form';
import { toast } from 'sonner';

import { Button } from '@/components/ui/button';
import {
    Form,
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { setCookie } from '@/helpers/cookies';
import { cn } from '@/lib/utils';
import { fetchLogin } from '@/services';
import { sanitize } from '@/utils/inputs-sanitize';

import { type LoginSchema, loginSchema } from './schema';
import type { FormLoginProps } from './type';

export const FormLogin = ({ className, ...props }: FormLoginProps) => {
    const [isVisibility, setIsVisibility] = useState(false);
    const form = useForm<LoginSchema>({
        resolver: zodResolver(loginSchema),
        criteriaMode: 'all',
        mode: 'onBlur',
        defaultValues: {
            email: '',
            password: '',
        },
    });
    const navigate = useNavigate();

    const onSubmit = async (data: LoginSchema) => {
        if (!data) return;

        const sanitizedData = {
            email: sanitize(data.email),
            password: sanitize(data.password),
        };

        try {
            const response = await fetchLogin(sanitizedData);
            if (response.access_token) {
                setCookie(response.access_token);
                form.reset();
            }
        } catch (error) {
            toast.error(
                error instanceof Error ? error.message : 'Erro ao fazer login',
            );
        } finally {
            navigate({
                to: '/dashboard',
            });
        }
    };

    return (
        <Form {...form}>
            <form
                onSubmit={form.handleSubmit(onSubmit)}
                className={cn('flex flex-col gap-6', className)}
                {...props}
            >
                <FormField
                    control={form.control}
                    name="email"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel htmlFor="email">Email</FormLabel>
                            <FormControl>
                                <Input
                                    {...field}
                                    type="email"
                                    id="email"
                                    placeholder="Digite seu email"
                                />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />
                <FormField
                    control={form.control}
                    name="password"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel htmlFor="password">Senha</FormLabel>
                            <FormControl>
                                <div className="relative">
                                    {isVisibility ? (
                                        <EyeOff
                                            size={20}
                                            className="absolute right-2 top-2 text-slate-600"
                                            onClick={() =>
                                                setIsVisibility(false)
                                            }
                                        />
                                    ) : (
                                        <Eye
                                            size={20}
                                            className="absolute right-2 top-2 text-slate-600"
                                            onClick={() =>
                                                setIsVisibility(true)
                                            }
                                        />
                                    )}
                                    <Input
                                        {...field}
                                        type={
                                            isVisibility ? 'text' : 'password'
                                        }
                                        id="password"
                                        placeholder="Digite sua senha"
                                    />
                                </div>
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />
                <Button type="submit" disabled={form.formState.isSubmitting}>
                    {form.formState.isSubmitting ? 'Carregando...' : 'Entrar'}
                </Button>
            </form>
        </Form>
    );
};
