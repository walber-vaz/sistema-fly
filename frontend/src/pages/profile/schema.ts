import { z } from 'zod';

export const profileSchema = z.object({
    first_name: z
        .string({
            required_error: 'O campo nome é obrigatório',
        })
        .optional(),
    surname: z
        .string({
            required_error: 'O campo sobrenome é obrigatório',
        })
        .optional(),
    email: z
        .string({
            required_error: 'O campo email é obrigatório',
        })
        .email({
            message: 'O email informado é inválido',
        })
        .optional(),
    phone_number: z
        .string({
            required_error: 'O campo telefone é obrigatório',
        })
        .min(12, {
            message: 'O telefone informado é inválido',
        })
        .optional(),
});
export type ProfileSchema = z.infer<typeof profileSchema>;
