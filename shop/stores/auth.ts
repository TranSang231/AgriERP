import { defineStore } from 'pinia'

type Customer = {
  id: number
  email?: string
  name?: string
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: '' as string,
    refreshToken: '' as string,
    user: null as Customer | null,
  }),
  persist: true,
  getters: {
    isAuthenticated: (s) => !!s.accessToken,
  },
  actions: {
    setTokens(access: string, refresh = '') {
      this.accessToken = access
      if (refresh) this.refreshToken = refresh
    },
    clear() {
      this.accessToken = ''
      this.refreshToken = ''
      this.user = null
    },
  }
})


