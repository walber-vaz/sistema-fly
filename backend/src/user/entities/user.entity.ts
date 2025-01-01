import { UserType } from '../enums';

export class User {
    id?: string;
    firstName: string;
    lastName: string;
    email: string;
    password: string;
    addressId?: string;
    type: UserType = UserType.CUSTOMER;
    isActive: boolean = true;
    phone: string;
}
