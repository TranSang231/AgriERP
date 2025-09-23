<script setup lang="ts">
const cart = useCartStore()
const auth = useAuthStore()
const { format } = useCurrency()
const { request } = useApi()
const router = useRouter()

const address = reactive({
  line1: '',
  province_id: '',
  district_id: '',
  ward_id: '',
})
const loading = ref(false)
const err = ref('')

// TODO(checkout-address): Load provinces/districts/wards from
//   GET /provinces, GET /districts?province=, GET /wards?district=
// TODO(checkout-order): Replace mock success with API order creation
//   POST /orders with { items: [{ product, quantity, price }], shipping_address }
async function placeOrder() {
  loading.value = true
  err.value = ''
  try {
    // Mock success flow for UI only - replace with POST /orders
    await new Promise(r => setTimeout(r, 600))
    cart.clear()
    router.push(`/thanks`)
  } catch (e: any) {
    err.value = e?.data?.detail || 'Checkout failed'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="container mx-auto px-4 py-6">
    <h1 class="text-2xl font-semibold mb-4">Checkout</h1>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <section class="md:col-span-2 space-y-4">
        <div>
          <h2 class="font-semibold mb-2">Shipping Address</h2>
          <div class="space-y-3">
            <input v-model="address.line1" placeholder="Address" class="border rounded w-full p-2" />
            <div class="grid grid-cols-3 gap-3">
              <!-- TODO(address-select): Replace text inputs with selects populated by /provinces, /districts, /wards -->
              <input v-model="address.province_id" placeholder="Province ID" class="border rounded p-2" />
              <input v-model="address.district_id" placeholder="District ID" class="border rounded p-2" />
              <input v-model="address.ward_id" placeholder="Ward ID" class="border rounded p-2" />
            </div>
          </div>
        </div>
      </section>
      <aside class="md:col-span-1 border rounded p-4 space-y-2">
        <div class="font-semibold">Tổng đơn</div>
        <div class="text-sm text-gray-600">Items: {{ cart.count }}</div>
        <div class="text-lg">Total: <span class="font-semibold">{{ format(cart.total) }}</span></div>
        <p v-if="err" class="text-red-600 text-sm">{{ err }}</p>
        <button :disabled="loading || cart.count===0" @click="placeOrder" class="mt-2 w-full btn-primary">
          {{ loading ? 'Đang đặt...' : 'Đặt hàng' }}
        </button>
      </aside>
    </div>
  </div>
</template>


