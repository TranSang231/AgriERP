<template>
  <EcommerceOrderEditor
    :defaultData="{
      customer_id: null,
      customer_name: null,
      company_name: null,
      tax_code: null,
      payment_method: 0,
      payment_status: 0,
      account_number: null,
      vat_rate: 0.0,
      shipping_fee: 0.0,
      shipping_status: 0,
      date: null,
      items: []
    }"
  />
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'ecommerce'
})
</script>
