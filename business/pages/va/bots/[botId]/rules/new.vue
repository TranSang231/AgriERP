<template>
    <VaBotRuleEditor
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
    conversation_start: true,
    wait_for_user_input: true,
    bot_id: botId
  };
});

</script>