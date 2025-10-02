<template>
    <OfficeEditor :defaultData="{
        name: null,
        email: null,
        address: null,
        phone: null,
        established_date: formatDateTime(Date.now()),
        sessions: [],
    }" />
</template>

<script setup lang="ts">
import { formatDateTime } from '@/utils/time';
definePageMeta({
    layout: 'hrm'
})
</script>
