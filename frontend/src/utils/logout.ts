import { removeCookie } from '@/helpers/cookies';

export const handleLogout = () => {
    removeCookie();
    window.location.href = '/';
};
