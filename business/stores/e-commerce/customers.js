import { defineStore } from "pinia";
import { getCachedData, createCachedEntry } from '@/utils/caching';

export const useCustomersStore = defineStore('ecommerce_customers', {
    state: () => ({
        customers: {
            ...createCachedEntry([], 0)
        },
        currentCustomer: null,
        loading: false,
        error: null
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
                const customer = data.find((o) => o.id === id)
                return customer 
                    ? `${customer.first_name ? customer.first_name + ' ' : ''}${customer.last_name ? customer.last_name : ''}`
                    : "";
            }
        },
        getCustomerById: (state) => {
            return (id) => {
                const data = getCachedData(state.customers)
                return data.find((customer) => customer.id === id) || null;
            }
        },
        activeCustomers: (state) => {
            const data = getCachedData(state.customers)
            return data.filter(customer => customer.status === 1);
        },
        inactiveCustomers: (state) => {
            const data = getCachedData(state.customers)
            return data.filter(customer => customer.status === 0);
        },
        customersByGender: (state) => {
            return (gender) => {
                const data = getCachedData(state.customers)
                return data.filter(customer => customer.gender === gender);
            }
        }
    },
    actions: {
        setCustomers(customers) {
            this.customers = customers;
        },
        setCurrentCustomer(customer) {
            this.currentCustomer = customer;
        },
        setLoading(loading) {
            this.loading = loading;
        },
        setError(error) {
            this.error = error;
        },
        addCustomer(customer) {
            const data = getCachedData(this.customers);
            this.customers = createCachedEntry([...data, customer], Date.now());
        },
        updateCustomer(updatedCustomer) {
            const data = getCachedData(this.customers);
            const index = data.findIndex(customer => customer.id === updatedCustomer.id);
            if (index !== -1) {
                data[index] = updatedCustomer;
                this.customers = createCachedEntry(data, Date.now());
            }
        },
        removeCustomer(customerId) {
            const data = getCachedData(this.customers);
            const filteredData = data.filter(customer => customer.id !== customerId);
            this.customers = createCachedEntry(filteredData, Date.now());
        },
        clearError() {
            this.error = null;
        },
        clearCurrentCustomer() {
            this.currentCustomer = null;
        }
    },
});