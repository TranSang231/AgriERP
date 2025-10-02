<template>
    <VaBotSynonymEditor
      :defaultData="defaultData"
      :historyBack="true"
    />
  </template>
  
<script setup lang="ts">
definePageMeta({
  layout: 'va'
});
const route = useRoute();

const defaultData = computed(() => {
  const { botId } = route.params;
  return {
    reference: null,
      bot_id: botId
  };
});

</script>