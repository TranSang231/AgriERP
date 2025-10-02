<template>
  <EcommercePromotionEditor
    :defaultData="{
      name: null,
      start: null,
      end: null,
      type: 'discount',
      discount: null,
      promotion_items: [
        {
          product_id: null,
          discount: null,
          quantity_limit: null,
          quantity_limit_by_customer: null
        }
      ]
    }"
  />
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'ecommerce'
})
</script>
