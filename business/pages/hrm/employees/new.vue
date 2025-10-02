<template>
    <EmployeeEditor
      :defaultData="{
        first_name: null,
        last_name: null,
        work_mail: null,
        personal_mail: null,
        gender: 'female',
        status: 1
      }"
    />
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'hrm'
})
</script>
