import { defineStore } from 'pinia'
import { createCachedEntry } from '@/utils/caching'

export const useChatStore = defineStore('chat', {
  state: () => ({
    selectedBot: null,
    currentConversationId: '',
    conversations: {
      ...createCachedEntry([], 0)
    },
    messages: {
      ...createCachedEntry([], 0)
    },
    userInput: ''
  }),
  persist: {
    storage: persistedState.localStorage,
  },
  getters: {
    allConversations: (state) => {
      return state.conversations.data;
    },
    allMessages: (state) => {
      return state.messages.data;
    },
    currentConversation: (state) => {
      return state.conversations.data.find(conv => conv.id === state.currentConversationId) || null;
    }
  },
  actions: {
    setSelectedBot(bot) {
      this.selectedBot = bot;
    },
    setConversations(conversations) {
      this.conversations.data = conversations;
    },
    setMessages(messages) {
      this.messages.data = messages;
    },
    setCurrentConversationId(id) {
      this.currentConversationId = id;
    },
    addMessage(message) {
      this.messages.data.push(message);
    }
  }
})
