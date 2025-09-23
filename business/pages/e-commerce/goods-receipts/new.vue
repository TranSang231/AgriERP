<template>
  <EcommerceGoodsReceiptEditor
    :defaultData="{
      supplier_name: null,
      reference_code: null,
      note: null,
      date: null,
      items: []
    }"
  />
</template>

<script setup lang="ts">
import EcommerceGoodsReceiptEditor from "@/components/ecommerce/goods-receipt/Editor.vue";

definePageMeta({
  layout: 'ecommerce'
})
</script>


