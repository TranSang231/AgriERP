<template>
    <div @click="openModal" class="relative cursor-pointer">
      <slot></slot> <!-- Chèn nội dung mặc định hoặc icon -->
      <span v-if="badge" class="absolute top-0 right-0 rounded-full bg-pink-600 text-white text-xs w-4 h-4 flex items-center justify-center">
        {{ badge }}
      </span>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  const badge = ref(8); // Số thông báo hoặc nội dung badge
  const openModal = () => {
    // Emit event mở modal
    emit('open-modal');
  }
  </script>
  
  <style scoped>

  </style>
  