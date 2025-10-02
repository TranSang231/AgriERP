import { defineStore } from "pinia";
import { getCachedData, createCachedEntry } from '@/utils/caching';

export const useArticleCategoriesStore = defineStore('website_article_categories', {
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