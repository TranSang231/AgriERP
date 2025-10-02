<template>
    <div class="flex flex-col w-full min-h-screen bg-white align-center justify-between">
        <TopbarNav />
        <slot />
        <Chatbot/>
        <footer class="w-full self-end">
            <FooterContent />
        </footer>
    </div>
</template>

<script setup>
import Chatbot from '~/components/chatbot/Chatbot.vue'
</script>