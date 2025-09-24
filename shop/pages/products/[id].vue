<script setup lang="ts">
const cart = useCartStore()
const { format } = useCurrency()
const route = useRoute()
// TODO(product-detail): Fetch product detail from API
// - Endpoint: GET /products/{id}
// - Replace mock below with:
//   const { request } = useApi()
//   const { data: product } = await request(`/products/${route.params.id}`)
const product = ref({ id: Number(route.params.id), name: 'Sản phẩm demo', price: 99000 })

// TODO(product-gallery): Render images (thumbnail + gallery) from product.images
// TODO(product-categories): Show categories chips with links to filtered listing
// TODO(product-unit): Display unit info and stock level

function addToCart() {
  if (!product.value) return
  cart.add({ productId: product.value.id, name: product.value.name, price: product.value.price, qty: 1 })
}
</script>

<template>
  <div class="container mx-auto px-4 py-6" v-if="product">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
      <div>
        <div class="bg-gray-100 aspect-square" />
      </div>
      <div>
        <h1 class="text-2xl font-semibold">{{ product.name }}</h1>
        <p class="text-xl mt-3">{{ format(product.price) }}</p>
        <button @click="addToCart" class="mt-6 bg-black text-white rounded px-4 py-2">Add to cart</button>
      </div>
    </div>
  </div>
</template>


