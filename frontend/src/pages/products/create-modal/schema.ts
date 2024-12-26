import { z } from 'zod';

export const formCreateSchema = z.object({
    name: z.string().nonempty(),
    description: z.string().optional(),
    price: z.string().nonempty(),
    price_sale: z.string().nonempty(),
    stock: z.string({ coerce: true }).nonempty(),
    image_product: z.any().optional(),
    brand_id: z.string().uuid().nonempty(),
    category_id: z.string().uuid().nonempty(),
});
