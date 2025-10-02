<template>
  <Codemirror
    v-model:value="model"
    :options="cmOptions"
    height="400px"
    width="100%"
    :border="true"
    @ready="onReady"
  />
</template>

<script setup lang="ts">
import type { Editor, EditorConfiguration } from "codemirror";
import Codemirror from "codemirror-editor-vue3";
import "codemirror/mode/yaml/yaml.js"
import "codemirror/theme/dracula.css"

const model = defineModel();

const cmOptions: EditorConfiguration = reactive({
  mode: "text/x-yaml",
  theme: "dracula",
  readOnly: false,
  lineNumbers: true,
  lineWiseCopyCut: true,
  gutters: ["CodeMirror-lint-markers"],
  lint: true,
});
const cminstance = ref<Editor | null>(null);
const onReady = (cm: Editor) => {
  cminstance.value = cm;
};
</script>
