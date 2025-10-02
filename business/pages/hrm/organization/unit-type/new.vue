<template>
    <UnitTypeEditor :defaultData="{
        name: null,
        description: null
    }" />
</template>

<script setup lang="ts">
import UnitTypeEditor from '~/components/organization/UnitTypeEditor.vue';
definePageMeta({
    layout: 'hrm'
});

</script>
