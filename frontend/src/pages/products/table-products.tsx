import { useQuery } from '@tanstack/react-query';
import { Link } from '@tanstack/react-router';
import { Plus } from 'lucide-react';
import { useState } from 'react';
import { useMedia } from 'react-use';

import { Button } from '@/components/ui/button';
import {
    Pagination,
    PaginationContent,
    PaginationEllipsis,
    PaginationItem,
    PaginationLink,
    PaginationNext,
    PaginationPrevious,
} from '@/components/ui/pagination';
import {
    Table,
    TableBody,
    TableCell,
    TableFooter,
    TableHead,
    TableHeader,
    TableRow,
} from '@/components/ui/table';
import { cn } from '@/lib/utils';
import { fetchAllProducts } from '@/services';

import ModalCreateProduct from './create-modal';

export const TableProducts = () => {
    const [page, setPage] = useState<number | undefined>(undefined);
    const isDesktop = useMedia('(min-width: 768px)');

    const { data: products } = useQuery({
        queryKey: ['products', { page }],
        queryFn: async () => {
            return fetchAllProducts({ page });
        },
    });

    const handlePageChange = (newPage?: number) => {
        setPage(newPage);
    };

    return (
        <div className="flex w-full flex-col gap-4">
            <div className="my-6 flex items-center justify-between">
                {isDesktop ? (
                    <ModalCreateProduct />
                ) : (
                    <Link to={'/products/create'} className="ml-auto">
                        <Button>
                            <Plus className="size-5" />
                            Adicionar
                        </Button>
                    </Link>
                )}
            </div>
            <Table>
                <TableHeader>
                    <TableRow>
                        <TableHead>Nome</TableHead>
                        <TableHead>Preço</TableHead>
                        <TableHead>Estoque</TableHead>
                        <TableHead className="hidden lg:table-cell">
                            Cod. de Barras
                        </TableHead>
                        <TableHead className="hidden lg:table-cell">
                            Código
                        </TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {products?.data.map((product) => (
                        <TableRow key={product.id}>
                            <TableCell>
                                <div className="flex flex-col items-start gap-2 lg:flex-row lg:items-center">
                                    <img
                                        src={product.image_url}
                                        alt={product.name}
                                        className="size-12 object-cover object-center"
                                    />
                                    {product.name}
                                </div>
                            </TableCell>
                            <TableCell>{product.price_sale}</TableCell>
                            <TableCell>{product.stock}</TableCell>
                            <TableCell className="hidden lg:table-cell">
                                {product.barcode}
                            </TableCell>
                            <TableCell className="hidden lg:table-cell">
                                {product.code_product}
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
                <TableFooter>
                    <TableRow>
                        <TableCell colSpan={5}>
                            <Pagination>
                                <PaginationContent>
                                    <PaginationItem
                                        aria-disabled={!products?.previous_page}
                                        className={cn('opacity-50', {
                                            'cursor-not-allowed':
                                                !products?.previous_page,
                                        })}
                                    >
                                        <PaginationPrevious
                                            onClick={
                                                products?.previous_page
                                                    ? () =>
                                                          handlePageChange(
                                                              // eslint-disable-next-line max-len
                                                              products?.previous_page,
                                                          )
                                                    : undefined
                                            }
                                            aria-disabled={
                                                !products?.previous_page
                                            }
                                        />
                                    </PaginationItem>
                                    <PaginationItem>
                                        <PaginationLink
                                            onClick={
                                                (products?.total_pages ?? 0) > 1
                                                    ? () =>
                                                          handlePageChange(
                                                              // eslint-disable-next-line max-len
                                                              products?.next_page,
                                                          )
                                                    : undefined
                                            }
                                        >
                                            {products?.page}
                                        </PaginationLink>
                                    </PaginationItem>
                                    {(products?.total_pages ?? 0) > 1 && (
                                        <>
                                            <PaginationItem>
                                                <PaginationLink
                                                    onClick={() =>
                                                        handlePageChange(
                                                            products?.next_page,
                                                        )
                                                    }
                                                >
                                                    {products?.next_page}
                                                </PaginationLink>
                                            </PaginationItem>
                                            <PaginationItem>
                                                <PaginationEllipsis />
                                            </PaginationItem>
                                        </>
                                    )}
                                    <PaginationItem>
                                        <PaginationNext
                                            onClick={
                                                products?.has_next
                                                    ? () =>
                                                          handlePageChange(
                                                              // eslint-disable-next-line max-len
                                                              products?.next_page,
                                                          )
                                                    : undefined
                                            }
                                            aria-disabled={
                                                !products?.next_page ||
                                                products?.page ===
                                                    products?.total_pages
                                            }
                                            className={cn('opacity-50', {
                                                'cursor-not-allowed':
                                                    !products?.next_page ||
                                                    products?.page ===
                                                        products?.total_pages,
                                            })}
                                        />
                                    </PaginationItem>
                                </PaginationContent>
                            </Pagination>
                        </TableCell>
                    </TableRow>
                </TableFooter>
            </Table>
        </div>
    );
};
