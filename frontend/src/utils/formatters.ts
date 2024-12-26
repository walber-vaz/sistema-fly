export const formatPhoneNumber = (value: string | undefined): string => {
    if (!value) {
        return '';
    }
    const ddd = value.slice(1, 3);
    const firstPart = value.slice(3, 8);
    const secondPart = value.slice(8, 12);
    return `(${ddd}) ${firstPart}-${secondPart}`;
};

export const formatPhoneNumberInput = (value: string | undefined): string => {
    if (!value) {
        return '';
    }
    const cleaned = value.replace(/\D/g, '');
    if (cleaned.length > 11) {
        return formatPhoneNumber(cleaned);
    }

    const match = cleaned.match(/^(\d{2})(\d{5})(\d{4})$/);
    if (match) {
        return `(${match[1]}) ${match[2]}-${match[3]}`;
    }
    return cleaned;
};

export const formatCpf = (value: string) => {
    if (!value) {
        return value;
    }
    const firstPart = value.slice(0, 3);
    const secondPart = value.slice(3, 6);
    const thirdPart = value.slice(6, 9);
    const fourthPart = value.slice(9, 11);
    return `${firstPart}.${secondPart}.${thirdPart}-${fourthPart}`;
};

export const formatPhoneNumberOnChange = (value: string) => {
    const numbers = value.replace(/\D/g, '');

    // Format the number
    if (numbers.length <= 2) {
        return `(${numbers}`;
    }
    if (numbers.length <= 7) {
        return `(${numbers.slice(0, 2)}) ${numbers.slice(2)}`;
    }
    if (numbers.length <= 11) {
        return `(${numbers.slice(0, 2)}) ${numbers.slice(2, 7)}-${numbers.slice(7)}`;
    }
    return `(${numbers.slice(0, 2)}) ${numbers.slice(2, 7)}-${numbers.slice(7, 11)}`;
};

export const normalizePhoneNumber = (phone: string | undefined) => {
    if (!phone) return '';
    const number = phone.replace(/\D/g, '');
    return `0${number}`;
};
