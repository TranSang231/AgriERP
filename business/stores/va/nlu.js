import { defineStore } from 'pinia'
import { createCachedEntry } from '@/utils/caching'

export const useNluStore = defineStore('nlu', {
  state: () => ({
    host: {
      ...createCachedEntry('', 0)
    },
  }),
  persist: {
    storage: persistedState.localStorage,
  },
  getters: {
    nluHost: (state) => {
      return state.host.data;
    }
  },
  actions: {
    setHost(host) {
      this.host = host;
    }
  }
})
