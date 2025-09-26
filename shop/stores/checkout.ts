import { defineStore } from 'pinia'
import type { CartItem } from './cart' // Import kiểu dữ liệu để dùng chung

export const useCheckoutStore = defineStore('checkout', {
  state: () => ({
    items: [] as CartItem[],
  }),
  // Rất quan trọng để không mất dữ liệu khi chuyển trang
  persist: true, 
  getters: {
    count: (s) => s.items.reduce((a, b) => a + b.qty, 0),
    total: (s) => s.items.reduce((a, b) => a + b.price * b.qty, 0),
  },
  actions: {
    setItems(items: CartItem[]) {
      this.items = items;
    },
    clear() {
      this.items = [];
    }
  },
})