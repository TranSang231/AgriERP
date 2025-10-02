<template>
  <div class="flex justify-between items-center bg-primary text-white p-2">
    <span class="font-semibold">Amoz</span>
    <div class="flex space-x-4">
      <el-button
        :icon="Delete"
        @click="$emit('clear')"
        circle
      >
      </el-button>
      <el-button
        :icon="Refresh"
        @click="$emit('restart')"
        circle
      >
      </el-button>
      <el-button
        :icon="Close"
        @click="$emit('close')"
        circle
      >
      </el-button>
    </div>
  </div>
</template>

<script setup>
import { Delete, Close, Refresh } from "@element-plus/icons-vue";
defineEmits(["clear", "restart", "close"]);
</script>

<style scoped>
.hover\\:underline:hover {
  text-decoration: underline;
}
</style>
