<template>
  <div class="flex flex-col justify-center pt-20 px-5 gap-2">
    <BackButton />
    <p>Todo: Implement the form to create site, manage menus and site content, routes, site deployement. </p>
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
	defaultData: {
		type: Object,
		default: null
	},
});
</script>
