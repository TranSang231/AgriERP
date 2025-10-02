<template>
  <VaBotEditor
    :defaultData="defaultData"
  />
</template>

<script setup lang="ts">
definePageMeta({
layout: 'websites'
})

const defaultData = {
  name: null,
  config: "recipe: default.v1\nassistant_id: example_bot\nlanguage: en\npipeline:\n# will be selected by the Suggested Config feature\npolicies:\n- name: MemoizationPolicy\n- name: TEDPolicy\n  max_history: 5\n  epochs: 10",
  output_folder: null
}
</script>
