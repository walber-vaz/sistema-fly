import {
    AlignLeft,
    Handshake,
    Layers,
    Package,
    Package2,
    Share2,
    Users,
    Wallet,
} from 'lucide-react';

export const links = [
    {
        name: 'Produtos',
        to: '/products',
        icon: Package,
        subLinks: [
            {
                name: 'Categorias',
                to: '/products/categories',
                icon: Layers,
            },
            {
                name: 'Marcas',
                to: '/products/brands',
                icon: AlignLeft,
            },
            {
                name: 'Produtos',
                to: '/products',
                icon: Package2,
            },
        ],
    },
    {
        name: 'Clientes',
        to: '/clients',
        icon: Users,
        subLinks: [
            {
                name: 'Clientes',
                to: '/clients',
                icon: Users,
            },
            {
                name: 'Grupos',
                to: '/clients/groups',
                icon: Share2,
            },
        ],
    },
    {
        name: 'Vendas',
        to: '/sales',
        icon: Wallet,
        subLinks: [
            {
                name: 'Vendas',
                to: '/sales',
                icon: Handshake,
            },
            {
                name: 'Pedidos',
                to: '/sales/orders',
                icon: Wallet,
            },
        ],
    },
];
