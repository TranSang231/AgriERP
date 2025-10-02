<template>
    <RoleEditor
      :defaultData="{
        name: null,
        description: null,
        scope: null
      }"
    />
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'hrm'
})
</script>
