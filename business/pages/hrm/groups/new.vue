<template>
    <GroupEditor :defaultData="{
        name: null,
        email: null,
        address: null,
        phone: null,
        sessions: [],
    }" />
</template>

<script setup lang="ts">
definePageMeta({
    layout: 'hrm'
})
</script>
