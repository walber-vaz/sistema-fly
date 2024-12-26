import { ParsedLocation } from '@tanstack/react-router';

export const titlePageLocation = (location: ParsedLocation) => {
    const title = location.pathname.split('/').pop();
    return title ? title.charAt(0).toUpperCase() + title.slice(1) : '';
};
