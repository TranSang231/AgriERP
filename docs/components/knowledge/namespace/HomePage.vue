<template>
  <div class="flex flex-col justify-center pt-20 px-5">
    <div v-if="data && data.content" class="min-h-[200px] p-3" v-html="data.content" />
  </div>
</template>

<script setup>
const props = defineProps({
  data: {
    type: Object,
    default: null
  }
});

</script>