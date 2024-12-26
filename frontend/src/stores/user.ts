import { create } from 'zustand';

import type { IUser } from '@/interface/IUser';

interface States {
    user: IUser | null;
}

interface Actions {
    setUser: (user: IUser) => void;
}

export const useUser = create<States & Actions>((set) => ({
    user: null,
    setUser: (user) => set({ user }),
}));
