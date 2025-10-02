<template>
    <transition name="modal">
        <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
            <div class="bg-white p-4 rounded-lg max-w-md mx-auto">
                <div class="grid grid-cols-3 gap-4">
                    <div v-for="(icon, index) in icons" :key="index" class="text-center">
                        <component :is="icon.component" class="w-16 h-16 text-primary mx-auto" />
                        <p class="text-sm">{{ icon.name }}</p>
                    </div>
                </div>
                <button @click="closeModal" class="mt-4 w-full py-2 px-4 bg-primary text-white rounded">Close</button>
            </div>
        </div>
    </transition>
</template>

<script setup>
import { ref, watchEffect } from 'vue';

const props = defineProps({
    show: {
        type: Boolean,
        default: false
    },
    icons: {
        type: Array,
        required: true
    }
});
const emit = defineEmits(['close']);

const closeModal = () => {
    emit('close');
}
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
    transition: opacity 0.5s;
}

.modal-enter-from,
.modal-leave-to {
    opacity: 0;
}
</style>