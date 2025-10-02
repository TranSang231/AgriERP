import { defineStore } from "pinia";
import { createCachedEntry } from '@/utils/caching';

export const useGroupsStore = defineStore('group', {
    state: () => ({
        groups: {
            ...createCachedEntry([], 0)
        },
    }),
    persist: {
        storage: persistedState.localStorage,
    },
    getters: {
        allGroups: (state) => {
            return getCachedData(state.groups);
        }
    },
    actions: {
        setGroups(groups) {
            this.groups = groups;
        }
    },
})