<template>
  <div class="p-2 h-64 overflow-y-auto">
    <div
      v-for="(msg, index) in messages"
      :key="index"
      :class="getClass(msg.type)"
      v-html="msg.text"
    ></div>
    <!-- <span>{{ msg.text }}</span> -->
  </div>
</template>

<script setup>
import { computed, toRefs } from "vue";

const props = defineProps({
  messages: {
    type: Array,
    default: () => [],
  },
});

const getClass = (type) => {
  return type === "user"
    ? "bg-blue-100 p-2 rounded text-right my-1"
    : "bg-gray-100 p-2 rounded text-left my-1";
};
</script>
