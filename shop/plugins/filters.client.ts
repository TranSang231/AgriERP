import { defineNuxtPlugin } from 'nuxt/app'
import { useCurrency } from '~/composables/useCurrency'

export default defineNuxtPlugin(() => {
  const { format } = useCurrency()
  return {
    provide: {
      currency: format
    }
  }
})


