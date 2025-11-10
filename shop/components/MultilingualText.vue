<template>
  <span>{{ localize(content) }}</span>
</template>

<script setup lang="ts">
import { useLocalize } from '~/composables/useLocalize'

interface Props {
  content: {
    origin: string;
    translates?: Array<{
      language: string;
      value: string;
    }>;
  } | string | null | undefined;
}

const props = defineProps<Props>()
const { localize } = useLocalize()
</script>
