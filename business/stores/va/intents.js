import { defineStore } from "pinia";
import { createCachedEntry } from '@/utils/caching';

export const useIntentsStore = defineStore('intent', {
    state: () => ({
        current_intent_id: '',
        intents: {
            ...createCachedEntry([], 0)
        },
    }),
    persist: {
        storage: persistedState.localStorage,
    },
    getters: {
        currentIntentId: (state) => {
            return state.current_intent_id;
        },
        allIntents: (state) => {
            return getCachedData(state.intents);
        }
    },
    actions: {
        setCurrentIntent(intent) {
            this.current_intent_id = intent;
        },
        setIntents(intents) {
            this.intents = intents;
        }
    },
})