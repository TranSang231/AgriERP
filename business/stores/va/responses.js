import { defineStore } from "pinia";
import { createCachedEntry } from '@/utils/caching';

export const useResponsesStore = defineStore('responses', {
    state: () => ({
        current_response_id: '',
        responses: {
            ...createCachedEntry([], 0)
        },
    }),
    persist: {
        storage: persistedState.localStorage,
    },
    getters: {
        currentResponseId: (state) => {
            return state.current_response_id;
        },
        allResponses: (state) => {
            return getCachedData(state.responses);
        }
    },
    responses: {
        setCurrentResponse(response) {
            this.current_response_id = response;
        },
        setResponses(responses) {
            this.responses = responses;
        }
    },
})