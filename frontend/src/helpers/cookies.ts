import cookie from 'js-cookie';

import { COOKIE_NAME } from '@/constants';

export const getCookie = () => {
    return cookie.get(COOKIE_NAME);
};

export const setCookie = (value: string) => {
    return cookie.set(COOKIE_NAME, value, {
        expires: 1,
        secure: process.env.NODE_ENV === 'production',
        path: '/',
        sameSite: 'strict',
    });
};

export const removeCookie = () => {
    return cookie.remove(COOKIE_NAME);
};

export const isLogged = () => {
    return !!getCookie();
};
