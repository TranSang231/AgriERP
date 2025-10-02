<template>
    <Dashboard v-if="authenticated" />
    <GettingStarted v-else />
</template>

<script setup>
definePageMeta({
  layout: 'anonymous'
})

import { useOauthStore } from '@/stores/oauth';
const oauthStore = useOauthStore()
const authenticated = computed(() => {
    const { tokenInfo } = oauthStore;
    if (!tokenInfo) return false;
    const { access_token } = tokenInfo;
    if (!access_token) return false;
    return access_token.length > 0;
})
</script>
