<template>
  <SettingsEditor
      v-if="constantsStore.nluConfigTemplate"
      v-model="model"
      :settingsDescription="constantsStore.nluConfigTemplate"
      :editable="editable"
  />
</template>
  
<script setup lang="ts">
import { useConstantsStore } from '@/stores/constants';
import ConstantsService from '@/services/constants';
const props = defineProps({
  editable: {
    type: Boolean,
    default: false
  }
});
  
const constantsStore = useConstantsStore();
const model = defineModel()

onMounted(() => {
  ConstantsService.fetch("nlu_config_template");
});
</script>
  