<template>
  <div class="flex flex-row w-full gap-2">
    <el-card
      class="w-1/2"
      header-class="py-2"
      body-class="h-full px-1 py-2"
    >
      <template #header>
        <span class="text-white">{{t('Steps')}}</span>
      </template>
      <draggable
        :list="steps"
        group="steps"
        class="flex flex-col w-full h-full p-2 gap-2"
        :itemKey="(element: any) => `${element.type}${element.order}`"
      >
        <template #item="{ element, index }">
          <div class="flex flex-row items-start p-2 gap-2 border shadow border-primary">
            <component
              :is="getComponentFromMap(stepComponentMap, element.type)"
              v-model="steps[index]"
            />
          </div>
        </template>
      </draggable>
    </el-card>
    <div class="flex flex-col gap-2 w-1/2 max-h-screen">
      <el-card
        v-if="intents"
        class="w-full"
        header-class="py-2"
        body-class="h-full px-1 pt-2 max-h-1/3 overflow-scroll"
      >
        <template #header>
          <span class="text-white">{{t('Intents')}}</span>
        </template>
        <draggable
          :list="intents"
          :group="inputDataGroupProps"
          :clone="cloneIntent"
          class="flex flex-col max-h-50 px-2 pb-10 gap-2"
          itemKey="id"
        >
          <template #item="{ element }">
            <div class="flex flex-row items-start p-2 gap-2 border shadow border-primary">
              {{ element.name }}
            </div>
          </template>
        </draggable>
      </el-card>
      <el-card
        v-if="responses"
        class="w-full"
        header-class="py-2"
        body-class="h-full px-1 pt-2 max-h-1/3 overflow-scroll"
      >
        <template #header>
          <span class="text-white">{{t('Responses')}}</span>
        </template>
        <draggable
          :list="responses"
          :group="inputDataGroupProps"
          :clone="cloneResponse"
          class="flex flex-col max-h-50 px-2 pb-10 gap-2"
          itemKey="id"
        >
          <template #item="{ element }">
            <div class="flex flex-row items-start p-2 gap-2 border shadow border-primary">
              {{ element.name }}
            </div>
          </template>
        </draggable>
      </el-card>
    </div>
  </div>
</template>
  
<script setup lang="ts">
import draggable from 'vuedraggable'
import IntentStep from './IntentStep.vue';
import ResponseStep from './ResponseStep.vue';

const props = defineProps({
  editable: {
    type: Boolean,
    default: false
  },
  intents: {
    type: Array<any>,
    defaul: []
  },
  entities: {
    type: Array<any>,
    defaul: []
  },
  responses: {
    type: Array<any>,
    defaul: []
  }
});

const { t } = useI18n();
const model = defineModel()
const steps = ref<Array<any>>(
  model.value
    ? (model.value as Array<any>).sort((a,b) => {
        const ao = a.order? a.order : 0;
        const bo = b.order? b.order : 0;
        return ao - bo;
      })
    : []
);
const inputDataGroupProps = { name: 'steps', pull: 'clone', put: false }

const orderedSteps = computed(() => {
  if(!steps.value) {
    return [];
  }
  return steps.value.map((s: any, index: number) => ({...s, order: index}));
});

const cloneIntent = (intent: any) => {
  const { name } =  intent
  return {
    type: "intent",
    payload: {name}
  }
}

const cloneResponse = (response: any) => {
  const { name } =  response
  return {
    type: "response",
    payload: {name}
  }
}

const stepComponentMap = {
  'intent': IntentStep,
  'response': ResponseStep
}
const getComponentFromMap = <T, K extends keyof T>(map: T, type: K) => {
  return map[type];
}

watch(orderedSteps, (newValue) => {
  model.value = newValue;
})
</script>
  