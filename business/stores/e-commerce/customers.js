import { defineStore } from "pinia";
import { getCachedData, createCachedEntry } from '@/utils/caching';

export const useCustomersStore = defineStore('ecommerce_customers', {
    state: () => ({
        customers: {
            ...createCachedEntry([], 0)
        }
    }),
    persist: {
        storage: persistedState.localStorage,
    },
    getters: {
        allCustomers: (state) => {
            return getCachedData(state.customers);
        },
        customerName: (state) => {
            return (id) => {
                const data = getCachedData(state.customers)
                const customer =  data.find((o) => o.id === id)
                return customer 
                    ? `${item.first_name ? item.first_name + ' ' : ''}${item.last_name ? item.last_name : ''}`
                    : "";
            }
        },
    },
    actions: {
        setCustomers(customers) {
            this.customers = customers;
        }
    },
});