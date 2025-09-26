import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue' // Import ref và computed từ Vue
import { useCartService } from '~/services/cart'

// Định nghĩa kiểu dữ liệu cho một item trong giỏ hàng
export type CartItem = {
  // id của CartItem ở backend, dùng để PATCH/DELETE
  itemId?: number
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
  const isLoading = ref(false)
  const hasLoaded = ref(false)

  // --- SERVICES ---
  const { getCart, addToCart, updateCartItem, removeFromCart } = useCartService()

  // --- GETTERS ---
  // Các getter giờ là các computed property
  const count = computed(() => items.value.reduce((acc, item) => acc + item.qty, 0))
  const total = computed(() => items.value.reduce((acc, item) => acc + item.price * item.qty, 0))
  
  const selectedItems = computed(() => items.value.filter(item => item.selected))
  const selectedCount = computed(() => selectedItems.value.reduce((acc, item) => acc + item.qty, 0))
  const selectedTotal = computed(() => selectedItems.value.reduce((acc, item) => acc + (item.price * item.qty), 0))

  // --- ACTIONS ---
  // Các action giờ là các function thông thường
  async function load() {
    if (isLoading.value) return
    try {
      isLoading.value = true
      const { data, error } = await getCart()
      if (error?.value) throw error.value
      const cart = data.value
      if (cart && Array.isArray(cart.items)) {
        items.value = cart.items.map((it: any) => ({
          itemId: it.id,
          productId: it.product?.id,
          name: it.product?.name,
          price: (it.product?.sale_price ?? it.product?.price ?? 0),
          qty: it.quantity ?? 1,
          selected: true,
        }))
      } else {
        items.value = []
      }
      hasLoaded.value = true
    } catch (e) {
      // giữ im lặng, tránh phá UX nếu backend chưa sẵn sàng
    } finally {
      isLoading.value = false
    }
  }

  async function add(product: Omit<CartItem, 'selected' | 'qty'> & { qty?: number }) {
    const quantityToAdd = product.qty || 1
    // Gọi backend để thêm vào cart
    try {
      const { data, error } = await addToCart({ product_id: product.productId, quantity: quantityToAdd })
      if (!error?.value && data?.value) {
        const it: any = data.value
        const found = items.value.find(i => i.productId === product.productId)
        if (found) {
          found.qty += quantityToAdd
          found.itemId = found.itemId ?? it.id
        } else {
          items.value.push({
            itemId: it.id,
            productId: product.productId,
            name: product.name,
            price: product.price,
            qty: quantityToAdd,
            selected: true,
          })
        }
        return
      }
    } catch (_) {}
    // Fallback local nếu gọi API lỗi
    const found = items.value.find(i => i.productId === product.productId)
    if (found) {
      found.qty += quantityToAdd
    } else {
      items.value.push({ ...product, qty: quantityToAdd, selected: true })
    }
  }

  async function remove(productId: number) {
    const found = items.value.find(i => i.productId === productId)
    if (!found) return
    const backendId = found.itemId
    if (backendId) {
      try {
        const { error } = await removeFromCart(backendId)
        // ignore error, vẫn xóa local để UX mượt
      } catch (_) {}
    }
    items.value = items.value.filter(i => i.productId !== productId)
  }

  async function setQty(productId: number, qty: number) {
    const found = items.value.find(i => i.productId === productId)
    if (!found || qty <= 0) return
    const previous = found.qty
    found.qty = qty
    if (found.itemId) {
      try {
        const { error } = await updateCartItem(found.itemId, qty)
        if (error?.value) {
          // hoàn tác nếu lỗi
          found.qty = previous
        }
      } catch (_) {
        found.qty = previous
      }
    }
  }

  function clear() {
    // API không định nghĩa clear hàng loạt, xóa local để UX nhanh
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
    isLoading,
    hasLoaded,
    count,
    total,
    selectedItems,
    selectedCount,
    selectedTotal,
    load,
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