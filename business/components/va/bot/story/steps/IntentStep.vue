<template>
  <div class="flex flex-row w-full gap-2">
    <span>{{ t('Intent') }}:</span>
    <span>{{ (model as any).payload.name || '' }}</span>
  </div>
    
  </template>
    
<script setup lang="ts">

const { t } = useI18n();
const model = defineModel();

</script>
    