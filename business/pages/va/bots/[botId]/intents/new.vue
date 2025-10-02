<template>
    <VaBotIntentEditor
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
      name: null,
      bot_id: botId
  };
});

</script>