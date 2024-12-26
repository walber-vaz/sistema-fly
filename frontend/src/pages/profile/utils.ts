import { IUser, IUserUpdate } from '@/interface/IUser';
import { normalizePhoneNumber } from '@/utils/formatters';

import { ProfileSchema } from './schema';

export const hasChanges = (
    values: Partial<ProfileSchema>,
    originalValues: Partial<IUser>,
) => {
    const changedFields: Partial<IUserUpdate> = {};

    type UserUpdateField = keyof IUserUpdate;

    (Object.keys(values) as UserUpdateField[]).forEach((key) => {
        const newValue = values[key as keyof typeof values];
        const originalValue =
            originalValues[key as keyof typeof originalValues];

        // Special handling for phone number
        if (key === 'phone_number') {
            const normalizedNew = normalizePhoneNumber(newValue);
            const normalizedOriginal = normalizePhoneNumber(originalValue);

            if (normalizedNew !== normalizedOriginal) {
                changedFields[key] = newValue;
            }
        } else {
            // Handle other fields normally
            if (newValue !== originalValue) {
                changedFields[key] = newValue;
            }
        }
    });

    const hasChanges = Object.keys(changedFields).length > 0;

    return {
        changedFields,
        hasChanges,
    };
};
