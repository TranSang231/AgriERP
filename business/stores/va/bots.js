import { defineStore } from "pinia";
import { createCachedEntry } from '@/utils/caching';

export const useBotsStore = defineStore('bots', {
    state: () => ({
        current_bot_id: '',
        bots: {
            ...createCachedEntry([], 0)
        },
    }),
    persist: {
        storage: persistedState.localStorage,
    },
    getters: {
        currentBotId: (state) => {
            return state.current_bot_id;
        },
        allBots: (state) => {
            return getCachedData(state.bots);
        }
    },
    actions: {
        setCurrentBot(bot) {
            this.current_bot_id = bot;
        },
        setBots(bots) {
            this.bots = bots;
        }
    },
})