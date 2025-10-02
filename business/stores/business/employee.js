import { defineStore } from 'pinia';
import { getCachedData, createCachedEntry } from '@/utils/caching';

export const useEmployeesStore = defineStore('employees', {
    state: () => ({
        employees: {
            ...createCachedEntry([], 0)
        },
        employees_by_office: {
            ...createCachedEntry([], 0)
        },
    }),
    persist: {
        storage: persistedState.localStorage,
    },
    getters: {
        allEmployees: (state) => {
            return getCachedData(state.employees);
        },
        allEmployeesByOffice: (state) => {
            return getCachedData(state.employees_by_office);
        },
    },
    actions: {
        setEmployees(employees) {
            this.employees = employees;
        },
        setEmployeesByOffice(employees_by_office) {
            this.employees_by_office = employees_by_office;
        },
    },
})