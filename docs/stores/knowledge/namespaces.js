import { defineStore } from "pinia";
import { getCachedData, createCachedEntry } from '@/utils/caching';

export const useNamespacesStore = defineStore('knowledge_namespaces', {
    state: () => ({
        namespaces: {
            ...createCachedEntry([], 0)
        }
    }),
    persist: {
        storage: persistedState.localStorage,
    },
    getters: {
        allNamespaces: (state) => {
            return getCachedData(state.namespaces);
        }
    },
    actions: {
        setNamespaces(namespaces) {
            this.namespaces = namespaces;
        }
    },
});