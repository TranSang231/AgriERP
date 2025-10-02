<template>
  <div class="flex items-center p-2 border-t">
    <textarea
      v-model="userInput"
      placeholder="Type a message..."
      class="flex-1 resize-none p-2 border rounded"
    ></textarea>
    <el-button
      @click="send"
      class="ml-2 bg-primary text-white p-2 rounded hover:bg-secondary"
      :icon="Position"
    >
    </el-button>
  </div>
</template>

<script setup>
import { Position } from "@element-plus/icons-vue";
import { ref } from "vue";

const emit = defineEmits(["send"]);
const userInput = ref("");

const send = () => {
  const message = userInput.value.trim();
  if (message) {
    emit("send", message);
    userInput.value = ""; 
  }
};
</script>
