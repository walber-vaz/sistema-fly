interface IUser {
    first_name: string;
    surname: string;
    email: string;
    phone_number: string;
    created_at: string;
    updated_at: string;
}

interface IUserUpdate {
    first_name?: string;
    surname?: string;
    email?: string;
    phone_number?: string;
}

export type { IUser, IUserUpdate };
