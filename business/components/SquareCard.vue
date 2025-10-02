<template>
  <el-card class="square-card shadow hover" v-loading="loading">
    <template #header>
      <div class="bg-primary text-white flex justify-between items-center w-full h-full">
        <div class="flex items-center ">
          <el-icon color="white">
            <Movable />
          </el-icon>
          <span class="ml-5 text-semibold align-middle">{{ cardTitle }}</span>
        </div>

        <el-icon color="white">
          <VerticalMore />
        </el-icon>
      </div>
    </template>
    <div class="p-4">
      <slot />
    </div>
    <!-- <div class="resize-handle absolute bottom-0 right-0 w-5 h-5 cursor-nwse-resize bg-gray-800 bg-opacity-20 rounded-md"
      @mousedown="startResize"></div> -->
  </el-card>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue';
import Movable from '@/assets/icons/movable.svg'
import VerticalMore from '@/assets/icons/vertical-more.svg'

const props = defineProps({
  cardTitle: {
    type: String,
    required: true,
  },
  loading: {
    type: Boolean,
    required: false,
  }
});

const resizing = ref(false);
const cardElement = ref<HTMLElement | null>(null);
// const initialSize = ref({ width: 960, height: 480 });

// const startResize = (event: MouseEvent) => {
//   resizing.value = true;
//   document.addEventListener('mousemove', resize);
//   document.addEventListener('mouseup', stopResize);
// };

// const resize = (event: MouseEvent) => {
//   if (resizing.value && cardElement.value) {
//     const newWidth = event.clientX - cardElement.value.getBoundingClientRect().left;
//     const newHeight = event.clientY - cardElement.value.getBoundingClientRect().top;
//     initialSize.value.width = Math.max(newWidth, 200); // Minimum width
//     initialSize.value.height = Math.max(newHeight, 150); // Minimum height
//   }
// };

// const stopResize = () => {
//   resizing.value = false;
//   document.removeEventListener('mousemove', resize);
//   document.removeEventListener('mouseup', stopResize);
// };

onMounted(() => {
  cardElement.value = document.querySelector('.resizable-card') as HTMLElement;
});

// onBeforeUnmount(() => {
//   document.removeEventListener('mousemove', resize);
//   document.removeEventListener('mouseup', stopResize);
// });
</script>

<style scoped>
.square-card {
  position: relative;
  max-width: none;
  overflow: auto;
  border: 1px solid #dcdcdc;
}
</style>