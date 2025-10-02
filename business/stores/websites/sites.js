import { defineStore } from "pinia";
import { getCachedData, createCachedEntry } from '@/utils/caching';

export const useSitesStore = defineStore('website_sites', {
    state: () => ({
        sites: {
            ...createCachedEntry([], 0)
        }
    }),
    persist: {
        storage: persistedState.localStorage,
    },
    getters: {
        allSites: (state) => {
            return getCachedData(state.sites);
        }
    },
    actions: {
        setSites(sites) {
            this.sites = sites;
        }
    },
});