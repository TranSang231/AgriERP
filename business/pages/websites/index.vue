<template>
    <div class="h-screen w-full pt-20 flex flex-col items-center">
        <p>Todo:</p>
        <ul>
            <li>Write your pages to manage sites, pages, publish pages to sites.</li>
            <li>Create UIs let user deploy and monitoring deployment progress.</li>
            <li>Manage menus, contents in each section of the site.</li>
            <li>Summary of number of websites, line chart for the trend of pages creating/updating.</li>
        </ul>
    </div>
</template>

<script setup lang="ts">
definePageMeta({
    layout: 'websites'
})
</script>

<style scoped>
ul {
    list-style: inherit;
}
</style>