import { defineStore } from "pinia";
import { createCachedEntry } from '@/utils/caching';

export const useUnitsStore = defineStore('units', {
    state: () => ({
        units: {
            ...createCachedEntry([], 0)
        }
    }),
    persist: {
        storage: persistedState.localStorage,
    },
    getters: {
        allUnits: (state) => {
            return getCachedData(state.units);
        },
    },
    actions: {
        setUnits(units) {
            this.units = units;
        },
    },
})