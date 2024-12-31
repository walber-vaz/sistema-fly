import { PrismaClient } from '@prisma/client';
import { hashPassword } from '../src/helpers/password-hash';

const prisma = new PrismaClient();

async function main() {
    const permissions = await Promise.all([
        prisma.permission.create({
            data: {
                name: 'CREATE_USER',
                description: 'Create a new user',
            },
        }),
        prisma.permission.create({
            data: {
                name: 'UPDATE_USER',
                description: 'Update an existing user',
            },
        }),
        prisma.permission.create({
            data: {
                name: 'DELETE_USER',
                description: 'Delete an existing user',
            },
        }),
    ]);

    const adminRole = await prisma.role.create({
        data: {
            name: 'admin',
            description: 'System administrator',
            permissions: {
                connect: permissions.map((permission) => ({
                    id: permission.id,
                })),
            },
        },
    });

    const address = await prisma.address.create({
        data: {
            city: 'São Miguel do Guamá',
            number: '68',
            state: 'PA',
            street: 'Rua 1',
            zip: '68660-000',
            complement: 'Prox. a geleira',
        },
    });

    const hashedPassword = await hashPassword(
        'K2VAVQKJJ%JORdU2vr9Llv6Q6wG5#XE!',
    );

    const admin = await prisma.user.create({
        data: {
            email: 'wvs.walber@gmail.com',
            firstName: 'Walber',
            lastName: 'Silva',
            password: hashedPassword,
            userType: 'ADMIN',
            addressId: address.id,
            roles: {
                connect: {
                    id: adminRole.id,
                },
            },
            permissions: {
                create: permissions.map((permission) => ({
                    permission: {
                        connect: {
                            id: permission.id,
                        },
                    },
                    granted: true,
                })),
            },
        },
    });

    await prisma.company.create({
        data: {
            name: 'WS Softwares',
            userId: admin.id,
            addressId: address.id,
        },
    });

    await prisma.role.create({
        data: {
            name: 'customer',
            description: 'Customer',
        },
    });

    console.log('Seed completed');
}

main()
    .catch((e) => {
        console.error(e);
        process.exit(1);
    })
    .finally(async () => {
        await prisma.$disconnect();
    });
