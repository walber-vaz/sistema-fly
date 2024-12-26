import { z } from 'zod';

export const loginSchema = z.object({
    email: z
        .string({
            invalid_type_error: 'E-mail inválido',
            required_error: 'E-mail e obrigatório',
        })
        .email({
            message: 'E-mail inválido',
        })
        .nonempty({
            message: 'E-mail e obrigatório',
        }),
    password: z
        .string()
        .min(8, {
            message: 'Senha deve ter no mínimo 8 caracteres',
        })
        .nonempty({
            message: 'Senha e obrigatória',
        }),
});

export type LoginSchema = z.infer<typeof loginSchema>;
