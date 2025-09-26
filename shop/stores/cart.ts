import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue' // Import ref và computed từ Vue

// Định nghĩa kiểu dữ liệu cho một item trong giỏ hàng
export type CartItem = {
  productId: number
  name: string
  price: number
  qty: number
  selected: boolean 
}

// SỬ DỤNG CÚ PHÁP SETUP STORE ĐỂ KIỂM SOÁT REACTIVITY TỐT HƠN
export const useCartStore = defineStore('cart', () => {
  // --- STATE ---
  // Sử dụng ref() để đảm bảo items luôn là một đối tượng reactive
  const items = ref<CartItem[]>([])

  // --- GETTERS ---
  // Các getter giờ là các computed property
  const count = computed(() => items.value.reduce((acc, item) => acc + item.qty, 0))
  const total = computed(() => items.value.reduce((acc, item) => acc + item.price * item.qty, 0))
  
  const selectedItems = computed(() => items.value.filter(item => item.selected))
  const selectedCount = computed(() => selectedItems.value.reduce((acc, item) => acc + item.qty, 0))
  const selectedTotal = computed(() => selectedItems.value.reduce((acc, item) => acc + (item.price * item.qty), 0))

  // --- ACTIONS ---
  // Các action giờ là các function thông thường
  function add(product: Omit<CartItem, 'selected' | 'qty'> & { qty?: number }) {
    const found = items.value.find(i => i.productId === product.productId)
    const quantityToAdd = product.qty || 1;
    
    if (found) {
      found.qty += quantityToAdd
    } else {
      items.value.push({ ...product, qty: quantityToAdd, selected: true })
    }
  }

  function remove(productId: number) {
    items.value = items.value.filter(i => i.productId !== productId)
  }

  function setQty(productId: number, qty: number) {
    const found = items.value.find(i => i.productId === productId)
    if (found && qty > 0) {
      found.qty = qty
    }
  }

  function clear() {
    items.value = []
  }

  function toggleItemSelected(productId: number) {
    const found = items.value.find(i => i.productId === productId);
    if (found) {
      found.selected = !found.selected;
    }
  }

  function toggleSelectAll(select: boolean) {
    items.value.forEach(item => item.selected = select);
  }

  // Trả về tất cả các state, getter, action cần thiết
  return {
    items,
    count,
    total,
    selectedItems,
    selectedCount,
    selectedTotal,
    add,
    remove,
    setQty,
    clear,
    toggleItemSelected,
    toggleSelectAll,
  }
}, {
  // Cấu hình persist vẫn giữ nguyên
  persist: true,
})