<template>
  <el-input-tag
    v-model="tags"
    :placeholder="placeholder || t('default_tags_placeholder')"
    :disabled="!editable"
  />
</template>

<script setup lang="ts">
const props = defineProps({
  field: {
    type: String,
    default: "snow"
  },
  itemTemplate: {
    type: Object,
    default: {}
  },
  placeholder: {
    type: String,
    default: null
  },
  editable: {
    type: Boolean,
    default: false
  }
})

const { t } = useI18n()
const model = defineModel();

const arrayToTags = (array: any[], field: string) => {
  if (!array || array.length === 0 || !field) {
    return [];
  }
  return array.map((o: any) => o[field]);
}

const tagsToArray = (tags: string[], objects: any[], field: string, itemTemplate:any) => {
  if (!tags || tags.length === 0) {
    return [];
  }
  return tags.map((t) => {
    const o = objects.find((o: any) => o[field] == t);
    return o ? o : { ...itemTemplate, [field]: t};
  })
}

const tags = ref<string[]>(arrayToTags(model.value as any[], props.field));

watch(tags, (newValue) => {
  model.value = tagsToArray(newValue, model.value as any[], props.field, props.itemTemplate);
})

</script>
