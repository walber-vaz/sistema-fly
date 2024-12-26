import { zodResolver } from '@hookform/resolvers/zod';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useEffect, useMemo, useState } from 'react';
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
import { cn } from '@/lib/utils';
import { fetchUpdateDateUser } from '@/services';
import { useUser } from '@/stores/user';
import {
    formatPhoneNumber,
    formatPhoneNumberOnChange,
    normalizePhoneNumber,
} from '@/utils/formatters';

import { type ProfileSchema, profileSchema } from './schema';
import { hasChanges } from './utils';

const FormProfile = () => {
    const { user } = useUser();
    const [isEditing, setIsEditing] = useState(false);

    const queryClient = useQueryClient();
    const { mutateAsync: updateUser } = useMutation({
        mutationFn: (data: ProfileSchema) => {
            return fetchUpdateDateUser(data);
        },
        onSuccess: (response) => {
            queryClient.invalidateQueries({
                queryKey: ['user'],
            });
            toast.success(response.message);
            setIsEditing(false);
        },
        onError: (error) => {
            if (error instanceof Error) {
                toast.error(error.message);
            } else {
                toast.error('Ops! Algo deu errado, tente novamente!');
            }
        },
    });

    const initialValues = useMemo(
        () => ({
            first_name: user?.first_name ?? '',
            surname: user?.surname ?? '',
            email: user?.email ?? '',
            phone_number: formatPhoneNumber(user?.phone_number) ?? '',
        }),
        [user?.first_name, user?.surname, user?.email, user?.phone_number],
    );
    const form = useForm<ProfileSchema>({
        resolver: zodResolver(profileSchema),
        criteriaMode: 'all',
        mode: 'onBlur',
        defaultValues: initialValues,
    });

    useEffect(() => {
        form.reset(initialValues);
    }, [form, initialValues]);

    const onSubmit = async (values: ProfileSchema) => {
        const { hasChanges: isHasChanges, changedFields } = hasChanges(
            values,
            initialValues,
        );

        if (!isHasChanges) {
            form.setError('root', {
                type: 'manual',
                message: 'Não há alterações para salvar',
            });
            toast.info('Não há alterações para salvar');
            setIsEditing(false);
            return;
        }

        if (changedFields.phone_number) {
            changedFields.phone_number = normalizePhoneNumber(
                changedFields.phone_number,
            );
        }
        await updateUser(changedFields);
    };

    const handleEditToggle = () => {
        if (isEditing) {
            form.reset(initialValues);
        }
        setIsEditing((prev) => !prev);
    };

    return (
        <Form {...form}>
            <form
                onSubmit={form.handleSubmit(onSubmit)}
                className="w-full space-y-6"
            >
                <FormField
                    control={form.control}
                    name="first_name"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel
                                htmlFor={field.name}
                                className="text-slate-700"
                            >
                                Nome
                            </FormLabel>
                            <FormControl>
                                <Input
                                    placeholder="Nome"
                                    type="text"
                                    disabled={!isEditing}
                                    className="text-slate-700"
                                    {...field}
                                />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />
                <FormField
                    control={form.control}
                    name="surname"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel
                                htmlFor={field.name}
                                className="text-slate-700"
                            >
                                Sobrenome
                            </FormLabel>
                            <FormControl>
                                <Input
                                    placeholder="Sobrenome"
                                    type="text"
                                    disabled={!isEditing}
                                    className="text-slate-700"
                                    {...field}
                                />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />
                <FormField
                    control={form.control}
                    name="email"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel
                                htmlFor={field.name}
                                className="text-slate-700"
                            >
                                Email
                            </FormLabel>
                            <FormControl>
                                <Input
                                    placeholder="E-mail"
                                    type="email"
                                    disabled={!isEditing}
                                    className="text-slate-700"
                                    {...field}
                                />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />
                <FormField
                    control={form.control}
                    name="phone_number"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel
                                htmlFor={field.name}
                                className="text-slate-700"
                            >
                                Telefone
                            </FormLabel>
                            <FormControl>
                                <Input
                                    placeholder="Telefone"
                                    type="text"
                                    disabled={!isEditing}
                                    className="text-slate-700"
                                    {...field}
                                    onChange={(e) => {
                                        const formatted =
                                            formatPhoneNumberOnChange(
                                                e.target.value,
                                            );
                                        field.onChange(formatted);
                                    }}
                                    maxLength={16}
                                    pattern="\(\d{2}\) \d{5}-\d{4}"
                                />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />
                <div className="flex flex-col gap-4 md:flex-row">
                    <Button
                        type="button"
                        onClick={handleEditToggle}
                        className={cn(
                            'cursor-pointer bg-primary text-white',
                            form.formState.isSubmitting && 'cursor-not-allowed',
                        )}
                        disabled={form.formState.isSubmitting}
                    >
                        {isEditing ? 'Cancelar' : 'Editar'}
                    </Button>
                    <Button
                        className={cn(
                            'cursor-pointer border-primary',
                            !isEditing && 'cursor-not-allowed text-primary',
                        )}
                        variant={isEditing ? 'default' : 'outline'}
                        type="submit"
                        disabled={
                            !form.formState.isValid ||
                            form.formState.isSubmitting ||
                            !isEditing
                        }
                    >
                        Salvar
                    </Button>
                </div>
            </form>
        </Form>
    );
};

export default FormProfile;
