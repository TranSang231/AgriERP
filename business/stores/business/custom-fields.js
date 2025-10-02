import { defineStore } from 'pinia';
import { getCachedData, createCachedEntry } from '@/utils/caching';

export const useCustomFieldsStore = defineStore('customFields', {
    state: () => ({
        custom_fields: {
            ...createCachedEntry([], 0)
        },
    }),
    persist: {
        storage: persistedState.localStorage,
    },
    getters: {
        allCustomFields: (state) => {
            return getCachedData(state.custom_fields);
        }
    },
    actions: {
        setCustomFields(custom_fields) {
            this.custom_fields = custom_fields;
        }
    },
})