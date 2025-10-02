import { defineStore } from "pinia";
import { createCachedEntry } from '@/utils/caching';

export const useOfficesStore = defineStore('office', {
    state: () => ({
        current_office_id: '',
        offices: {
            ...createCachedEntry([], 0)
        },
    }),
    persist: {
        storage: persistedState.localStorage,
    },
    getters: {
        currentOfficeId: (state) => {
            return state.current_office_id;
        },
        allOffices: (state) => {
            return getCachedData(state.offices);
        }
    },
    actions: {
        setCurrentOffice(office) {
            this.current_office_id = office;
        },
        setOffices(offices) {
            this.offices = offices;
        }
    },
})