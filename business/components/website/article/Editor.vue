<template>
  <div class="flex flex-col justify-center pt-20 px-5">
    <BackButton class="mb-5" />
    <p>Todo: Implement the form to write and publish an articles. </p>
  </div>
</template>

<script setup>
const props = defineProps({
	defaultData: {
		type: Object,
		default: null
	}
});

</script>