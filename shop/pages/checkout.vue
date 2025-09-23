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

async function placeOrder() {
  loading.value = true
  err.value = ''
  try {
    // Create order minimal payload
    const payload = {
      items: cart.items.map(i => ({ product: i.productId, quantity: i.qty, price: i.price })),
      shipping_address: address,
    }
    const { data, error } = await request(`/orders`, { method: 'POST', body: payload })
    if (error.value) throw error.value
    cart.clear()
    router.push(`/orders/${(data.value as any).id}`)
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
              <input v-model="address.province_id" placeholder="Province ID" class="border rounded p-2" />
              <input v-model="address.district_id" placeholder="District ID" class="border rounded p-2" />
              <input v-model="address.ward_id" placeholder="Ward ID" class="border rounded p-2" />
            </div>
          </div>
        </div>
      </section>
      <aside class="md:col-span-1 border rounded p-4 space-y-2">
        <div class="font-semibold">Order Summary</div>
        <div class="text-sm text-gray-600">Items: {{ cart.count }}</div>
        <div class="text-lg">Total: <span class="font-semibold">{{ format(cart.total) }}</span></div>
        <p v-if="err" class="text-red-600 text-sm">{{ err }}</p>
        <button :disabled="loading || cart.count===0" @click="placeOrder" class="mt-2 w-full bg-black text-white rounded px-4 py-2">
          {{ loading ? 'Placing...' : 'Place Order' }}
        </button>
      </aside>
    </div>
  </div>
</template>


