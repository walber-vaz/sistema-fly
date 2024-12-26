export interface IProducts {
    data: IProduct[];
    total: number;
    page: number;
    per_page: number;
    total_pages: number;
    has_next: boolean;
    has_previous: boolean;
    next_page: number;
    previous_page: number;
    detail?: string;
}

export interface IProduct {
    id: string;
    name: string;
    description: string;
    price: string;
    price_sale: string;
    stock: number;
    image_url: string;
    brand_name: string;
    category_name: string;
    barcode: number;
    code_product: string;
    created_at: string;
    updated_at: string;
}

export interface IProductCreateResponse {
    name: string;
    category: string;
    brand: string;
    price_sale: string;
    code_product: string;
    barcode: number;
    image_url: string;
    created_at: string;
}

export interface IProductCreate {
    name: string;
    description?: string;
    price: string;
    price_sale: string;
    stock: number;
    image_product?: File;
    brand_id: string;
    category_id: string;
}
