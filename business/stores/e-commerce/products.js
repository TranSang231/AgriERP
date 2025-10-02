import { defineStore } from "pinia";
import { getCachedData, createCachedEntry } from '@/utils/caching';

export const useProductsStore = defineStore('ecommerce_products', {
    state: () => ({
        products: {
            ...createCachedEntry([], 0)
        }
    }),
    persist: {
        storage: persistedState.localStorage,
    },
    getters: {
        allProducts: (state) => {
            return getCachedData(state.products);
        },
        getProduct: (state) => {
            return (id) => {
                const data = getCachedData(state.products)
                return  data.find((o) => o.id === id);
            }
        },
        productName: (state) => {
            return (id) => {
                const data = getCachedData(state.products)
                const product =  data.find((o) => o.id === id)
                return product ? product.name.origin: "";
            }
        },
    },
    actions: {
        setProducts(products) {
            this.products = products;
        }
    },
});