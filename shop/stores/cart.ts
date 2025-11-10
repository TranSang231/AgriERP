import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useCartService } from '~/services/cart'
import { useCustomersService } from '~/services/customers'

export type CartItem = {
  itemId?: number
  productId: number
  name: string
  price: number
  originalPrice?: number
  qty: number
  selected: boolean
  image?: string
}

export const useCartStore = defineStore('cart', () => {
  
  const items = ref<CartItem[]>([])
  const isLoading = ref(false)
  const hasLoaded = ref(false)

  const auth = useAuthStore()

  function getGuestSessionId(): string {
    try {
      if (typeof window === 'undefined') return 'guest'
      const key = 'guest_session_id'
      let id = window.localStorage.getItem(key)
      if (!id) {
        id = Math.random().toString(36).slice(2) + Date.now().toString(36)
        window.localStorage.setItem(key, id)
      }
      return id
    } catch (_) {
      return 'guest'
    }
  }

  const storageKey = computed(() => {
    const userId = auth.user && ((auth.user as any).id || (auth.user as any).email)
    if (userId) return `cart:${userId}`
    const sid = getGuestSessionId()
    return `cart:guest:${sid}`
  })

  function loadFromStorage() {
    try {
      const raw = typeof window !== 'undefined' ? window.localStorage.getItem(storageKey.value) : null
      if (!raw) { items.value = []; return }
      const parsed = JSON.parse(raw)
      if (Array.isArray(parsed)) {
        items.value = parsed as CartItem[]
        sanitizeItemsInPlace()
      }
    } catch (_) {}
  }

  function saveToStorage() {
    try {
      if (typeof window === 'undefined') return
      window.localStorage.setItem(storageKey.value, JSON.stringify(items.value))
    } catch (_) {}
  }

  const { getCart, addToCart, updateCartItem, removeFromCart } = useCartService()
  const { getProfile: fetchProfile } = useCustomersService()

  async function ensureBackendAuthMapping(): Promise<void> {
    if (!auth.user) return
    try {
      await fetchProfile()
    } catch (_) {
    }
  }
  function toDisplayName(name: any): string {
    if (typeof name === 'string') return name
    if (name && typeof name === 'object' && 'origin' in name) return (name as any).origin as string
    return 'Unknown Product'
  }

  function sanitizeItemsInPlace(): void {
    items.value = items.value.map((it: any) => ({
      ...it,
      name: toDisplayName((it as any).name),
      image: it.image || '/placeholder-product.jpg',
    }))
  }

  const count = computed(() => items.value.reduce((acc, item) => acc + item.qty, 0))
  const total = computed(() => items.value.reduce((acc, item) => acc + item.price * item.qty, 0))
  const selectedItems = computed(() => items.value.filter(item => item.selected))
  const selectedCount = computed(() => selectedItems.value.reduce((acc, item) => acc + item.qty, 0))
  const selectedTotal = computed(() => selectedItems.value.reduce((acc, item) => acc + (item.price * item.qty), 0))

  
  async function load() {
    if (isLoading.value) return
    try {
      isLoading.value = true
      loadFromStorage()
      if (auth.user) {
        await ensureBackendAuthMapping()
        const { data, error } = await getCart()
        if (!error?.value && data?.value && Array.isArray(data.value.items)) {
          const backendItems = data.value.items
          if (backendItems.length > 0) {
            items.value = backendItems.map((it: any) => ({
              itemId: it.id,
              productId: it.product?.id,
              name: toDisplayName(it.product?.name),
              price: (it.product?.sale_price ?? it.product?.price ?? 0),
              originalPrice: (it.product?.price ?? it.product?.sale_price ?? 0),
              qty: it.quantity ?? 1,
              selected: true,
              image: it.product?.thumbnail || it.product?.image || '/placeholder-product.jpg'
            }))
          }
        }
      }
      hasLoaded.value = true
    } catch (e) {
    } finally {
      isLoading.value = false
      saveToStorage()
    }
  }

  async function add(product: Omit<CartItem, 'selected' | 'qty'> & { qty?: number }) {
    const quantityToAdd = product.qty || 1
    const normalizedName = toDisplayName((product as any).name)
    
    try {
      if (auth.user) {
        await ensureBackendAuthMapping()
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
              name: normalizedName,
              price: product.price,
              originalPrice: (product as any).originalPrice ?? product.price,
              qty: quantityToAdd,
              selected: true,
              image: product.image || '/placeholder-product.jpg'
            })
          }
          saveToStorage()
          return
        }
      }
    } catch (_) {}
    
    const found = items.value.find(i => i.productId === product.productId)
    if (found) {
      found.qty += quantityToAdd
    } else {
      items.value.push({
        ...product,
        name: normalizedName,
        originalPrice: (product as any).originalPrice ?? product.price,
        qty: quantityToAdd,
        selected: true,
        image: product.image || '/placeholder-product.jpg'
      })
    }
    saveToStorage()
  }

  async function remove(productId: number) {
    const found = items.value.find(i => i.productId === productId)
    if (!found) return
    const backendId = found.itemId
    if (backendId && auth.user) {
      await ensureBackendAuthMapping()
      try {
        const { error } = await removeFromCart(backendId)
      } catch (_) {}
    }
    items.value = items.value.filter(i => i.productId !== productId)
    saveToStorage()
  }

  async function setQty(productId: number, qty: number) {
    const found = items.value.find(i => i.productId === productId)
    if (!found || qty <= 0) return
    const previous = found.qty
    found.qty = qty
    if (found.itemId && auth.user) {
      await ensureBackendAuthMapping()
      try {
        const { error } = await updateCartItem(found.itemId, qty)
        if (error?.value) {
          found.qty = previous
        }
      } catch (_) {
        found.qty = previous
      }
    }
    saveToStorage()
  }

  function clear() {
    items.value = []
    saveToStorage()
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
  async function mergeGuestCartToUserCart() {
    try {
      if (!auth.user) return
      const guestKey = `cart:guest:${getGuestSessionId()}`
      const raw = typeof window !== 'undefined' ? window.localStorage.getItem(guestKey) : null
      const guestItems: CartItem[] = raw ? JSON.parse(raw) : []
      if (!Array.isArray(guestItems) || guestItems.length === 0) return

      const { data, error } = await getCart()
      const backendItems = (!error?.value && data?.value?.items) ? data.value.items : []
      const productIdToBackend = new Map<number, any>()
      for (const it of backendItems) {
        const pid = it?.product?.id
        if (pid) productIdToBackend.set(pid, it)
      }

      for (const g of guestItems as any[]) {
        const pid = g.productId
        const qty = g.qty || 1
        if (!pid) continue
        const existing = productIdToBackend.get(pid)
        if (!existing) {
          try { await addToCart({ product_id: pid, quantity: qty }) } catch (_) {}
        } else {
          const newQty = (existing.quantity || 1) + qty
          try { await updateCartItem(existing.id, newQty) } catch (_) {}
        }
      }

      if (typeof window !== 'undefined') window.localStorage.removeItem(guestKey)

      items.value = []
      await load()
    } catch (_) {}
  }

  watch(
    () => [(auth.user && ((auth.user as any).id || (auth.user as any).email))],
    async (val, oldVal) => {
      const newUserId = val[0]
      const oldUserId = oldVal?.[0]
      
      // User logged in (from no user or different user)
      if (newUserId && newUserId !== oldUserId) {
        // Clear existing items to avoid showing previous user's cart
        items.value = []
        hasLoaded.value = false
        
        // Merge guest cart if switching from guest to logged in
        if (!oldUserId) {
          await mergeGuestCartToUserCart()
        } else {
          // Switching between different user accounts - just load new user's cart
          await load()
        }
      } 
      // User logged out
      else if (!newUserId && oldUserId) {
        // Clear the authenticated user's cart from memory
        items.value = []
        hasLoaded.value = false
        // Load guest cart from localStorage
        loadFromStorage()
      }
    },
    { deep: false }
  )
}, {
  // Disable global persist to avoid sharing cart across accounts
  persist: false,
})