import { defineStore } from 'pinia'

export type CartItem = {
  productId: number
  name: string
  price: number
  qty: number
}

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: [] as CartItem[],
  }),
  persist: true,
  getters: {
    count: (s) => s.items.reduce((a, b) => a + b.qty, 0),
    total: (s) => s.items.reduce((a, b) => a + b.price * b.qty, 0),
  },
  actions: {
    add(item: CartItem) {
      const found = this.items.find(i => i.productId === item.productId)
      if (found) found.qty += item.qty
      else this.items.push({ ...item })
    },
    remove(productId: number) {
      this.items = this.items.filter(i => i.productId !== productId)
    },
    setQty(productId: number, qty: number) {
      const found = this.items.find(i => i.productId === productId)
      if (found) found.qty = qty
    },
    clear() { this.items = [] }
  }
})


