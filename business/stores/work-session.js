import { defineStore } from "pinia";
import { createCachedEntry } from '@/utils/caching';

export const useWorkSessionsStore = defineStore('work-sessions', {
    state: () => ({
        work_sessions: {
            ...createCachedEntry([], 0)
        },
    }),
    persist: {
        storage: persistedState.localStorage,
    },
    getters: {
        allWorkSessions: (state) => {
            return getCachedData(state.work_sessions);
        }
    },
    actions: {
        setWorkSessions(work_sessions) {
            this.work_sessions = work_sessions;
        }
    },
})