import { defineStore } from "pinia";
import { createCachedEntry } from '@/utils/caching';

export const useUnitTypesStore = defineStore('unit-types', {
    state: () => ({
        unitTypes: {
            ...createCachedEntry([], 0)
        },
    }),
    persist: {
        storage: persistedState.localStorage,
    },
    getters: {
        allUnitTypes: (state) => {
            return getCachedData(state.unitTypes);
        }
    },
    actions: {
        setUnitTypes(unitTypes) {
            this.unitTypes = unitTypes;
        }
    },
})