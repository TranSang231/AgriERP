import { defineStore } from "pinia";
import { createCachedEntry } from '@/utils/caching';

export const useModelsStore = defineStore('model', {
    state: () => ({
        current_model_id: '',
        models: {
            ...createCachedEntry([], 0)
        },
    }),
    persist: {
        storage: persistedState.localStorage,
    },
    getters: {
        currentModelId: (state) => {
            return state.current_model_id;
        },
        allModels: (state) => {
            return getCachedData(state.models);
        }
    },
    actions: {
        setCurrentModel(model) {
            this.current_model_id = model;
        },
        setModels(models) {
            this.models = models;
        }
    },
})