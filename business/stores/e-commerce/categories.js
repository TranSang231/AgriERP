import { defineStore } from "pinia";
import { getCachedData, createCachedEntry } from '@/utils/caching';

export const useProductCategoriesStore = defineStore('ecommerce_product_categories', {
    state: () => ({
        categories: {
            ...createCachedEntry([], 0)
        }
    }),
    persist: {
        storage: persistedState.localStorage,
    },
    getters: {
        allCategories: (state) => {
            return getCachedData(state.categories);
        }
    },
    actions: {
        setCategories(categories) {
            this.categories = categories;
        }
    },
});