<template>
  <slot v-if="allScopes && oauthStore.hasAllScopes(allScopes)"></slot>
  <slot v-else-if="oneOfScopes && oauthStore.hasOneOfScopes(oneOfScopes)"></slot>
</template>

<script setup lang="ts">
import { useOauthStore } from '@/stores/oauth';
const props = defineProps({
  allScopes: {
    type: [Array, null],
    default: null
  },
  oneOfScopes: {
    type: [Array, null],
    default: null
  },
});

const oauthStore = useOauthStore();
</script>
