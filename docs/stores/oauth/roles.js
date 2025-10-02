import { defineStore } from 'pinia';
import { getCachedData, createCachedEntry } from '@/utils/caching';

export const useRolesStore = defineStore('roles', {
    state: () => ({
        roles: {
            ...createCachedEntry([], 0)
        },
    }),
    persist: {
        storage: persistedState.localStorage,
    },
    getters: {
        allRoles: (state) => {
            return getCachedData(state.roles);
        }
    },
    actions: {
        setRoles(roles) {
            this.roles = roles;
        }
    },
})