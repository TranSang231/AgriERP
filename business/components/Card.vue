<template>
    <div class="block w-full bg-white rounded-lg drop-shadow-md overflow-hidden">
        <div class="bg-primary p-4 border-b border-gray-200">
            <slot name="header">
                <h2 class="text-lg font-bold">{{ title }}</h2>
            </slot>
        </div>
        <div class="p-4">
            <slot>
                <p>{{ content }}</p>
            </slot>
        </div>
    </div>
</template>

<script setup lang="ts">

const props = defineProps({
    title: {
        type: String,
        default: 'Card Title'
    },
    content: {
        type: String,
        default: 'This is the default content of the card. Provide your own content using slots.'
    }
});
</script>

<style scoped>
.custom-card {
    max-width: 400px;
    margin: auto;
}

.custom-card-header {
    background-color: #f9f9f9;
}

.custom-card-body {
    background-color: #ffffff;
}
</style>