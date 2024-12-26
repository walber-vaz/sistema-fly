import dompurify from 'dompurify';

export const sanitize = (dirty: string) => {
    return dompurify.sanitize(dirty);
};
