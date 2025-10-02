<template>
  <div>
    <!-- Profile Button -->
    <div
      class="profile_div fixed bottom-10 right-10 cursor-pointer"
      @click="showModal"
    >
      <IconAmoz class="imgProfile rounded-full w-16 h-16 shadow-lg" />
    </div>
    <!-- Chatbot Modal -->
    <div
      v-show="isModalVisible"
      class="fixed bottom-5 right-5 w-80 bg-white shadow-lg rounded-lg"
    >
      <ChatbotHeader
        @clear="clearChat"
        @restart="restartChat"
        @close="closeModal"
      />
      <ChatbotBody :messages="messages" />
      <ChatbotFooter @send="sendMessage" />
      <div
        v-if="warnMessage"
        class="text-yellow-600 p-2 bg-yellow-100 rounded-md mt-2"
      >
        {{ warnMessage }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import IconAmoz from '~/assets/icons/amoz.svg';
import ChatbotHeader from '@/components/chatbot/ChatbotHeader.vue';
import ChatbotBody from '@/components/chatbot/ChatbotBody.vue';
import ChatbotFooter from '@/components/chatbot/ChatbotFooter.vue';
import { io } from 'socket.io-client';
import { useNluStore } from '@/stores/va/nlu';
import NLUService from '@/services/va/nlu';
import { v4 as uuid } from "uuid";

const nluStore = useNluStore();

const isModalVisible = ref(false);
const showModal = () => {
  isModalVisible.value = true;
};
const closeModal = () => {
  isModalVisible.value = false;
};
const socket = ref(null);
const sessionId = ref(uuid().replace(/-/g, ""));
const senderId = ref(`anonymous_${uuid()}`);
const messages = ref([]);
const warnMessage = ref("");

// Function to send user message to Rasa server
const sendMessage = async (message) => {
  if (!message || !socket.value || !socket.value.connected) {
    return;
  }
  const trimMessage = message.trim();
  if (trimMessage.length > 0) {
    messages.value.push({ text: trimMessage, type: "user" });
    console.log('sendMessage:', trimMessage)
    socket.value.emit(
      'user_uttered',
      {
        message: trimMessage,
        sender_id: senderId.value,
        session_id: sessionId.value
      }
    );
  }
};

const clearChat = () => {
  messages.value = [];
  warnMessage.value = null;
};

const restartChat = () => {
  try {
    clearChat();
    if (socket.value && socket.value.connected) {
      socket.value.emit("restart", { session_id: sessionId });
    }
  } catch (error) {
    warnMessage.value = "Error restarting chat. Please try again.";
    console.error("Error restarting chat:", error);
  }
};

const onMessageRecived = (message) => {
  if (message) {
    const { text, image, channel, buttons, accessory } = message;
      // Todo: handle channel, buttons, accessory later
      if (text && text.length > 0) {
        messages.value.push({
        text: text,
        type: "bot",
      });
      if (text && text.length > 0) {
        messages.value.push({
          text: `<img src="${res.image}" alt="Image" class="w-32 h-32" />`,
          type: "bot",
        });
      }
    }
  }
};

const connectSocket = async (host) => {
  console.log('connectSocket');
  if(socket.value && socket.value.connected) {
    socket.value.disconnect();
  }
  const s = io(host, {
    query: {
      // EIO: 4,
      transport: "websocket",
      session_persistence: true,
    },
    transports: ["websocket"],
    timeout: 5000,
    // perMessageDeflate: false,
  });
  s.on('connect_error', (error) => {
    warnMessage.value = "Unable to connect to chatbot.";
  });
  s.on('connect', () => {
    warnMessage.value = null;
    socket.value.emit('session_request', { session_id: sessionId.value });
  });

  s.on('disconnect', () => {
    console.log('Disconnected from Rasa Socket.IO server');
  });

  s.on('bot_uttered', onMessageRecived);
  socket.value = s;
}

watch(
  () => nluStore.nluHost,
  (newValue) => {
    if (newValue && newValue.length > 0) {
      connectSocket(newValue);
    }
  }
)

onMounted(() => {
  NLUService.fetchHost();
  if(nluStore && nluStore.nluHost && nluStore.nluHost.length > 0) {
    connectSocket(nluStore.nluHost);
  }
});

onUnmounted(() => {
  if (socket.value && socket.value.connected) {
    socket.value.disconnect();
  }
});
</script>

<style scoped>
/* Profile avatar styling */
.profile_div img {
  transition: transform 0.3s ease;
}
.profile_div img:hover {
  transform: scale(1.1);
}

/* Warning message styling */
.text-yellow-600 {
  color: #d97706;
}

.bg-yellow-100 {
  background-color: #fef3c7;
}
</style>
