<template>
  <div class="flex flex-col justify-center pt-20 px-5">
    <BackButton class="mb-5" :historyBack="historyBack"/>
    <ModelForm
      :title="t('Story')" 
      :collapsible="true"
      :service="StoryService"
      :rules="rules"
      :editable="canEdit"
      :default="defaultData"
      :nestedFields="['stories']"
      ref="modelForm"
    >
      <template #default="scope">
        <div class="flex flex-col gap-2">
          <el-form-item :label="t('Name')" prop="name">
            <el-input
              v-if="scope.editing"
              v-model="scope.current.name"
              :placeholder="t('default_place_holder')"
            />
            <span v-else>{{ scope.current.name }}</span>
          </el-form-item>
          <el-form-item
            prop="steps"
            class="flex flex-col items-start content-start"
            label-width="10px"
          >
            <span class="w-full">{{ t('Story_steps_guideline') }}</span>
            <StepsEditor
              v-model="scope.current.steps"
              :intents="intents"
              :entities="entities"
              :responses="responses"
            />
          </el-form-item>
        </div>
      </template>
    </ModelForm>
  </div>
</template>

<script setup lang="ts">
import { useOauthStore } from '@/stores/oauth';
import IntentService from '@/services/va/intent';
import EntityService from '@/services/va/entity';
import ResponseService from '@/services/va/response';
import StoryService from '@/services/va/story';
import StepsEditor from './steps/Editor.vue';

const props = defineProps({
	defaultData: {
		type: Object,
		default: null
	},
  pathPrefix: {
    type: String,
    default: null,
  },
  historyBack: {
    type: Boolean,
    default: false
  }
});

const { t } = useI18n();
const route = useRoute();
const oauthStore = useOauthStore();
const modelForm = ref(null);
const intents = ref<any>([]);
const entities = ref<any>([]);
const responses = ref<any>([])

const rules = {
  name: [
    { required: true, message: t('validate_error_required'), trigger: 'blur' }
  ]
};

const canEdit = computed(() => {
  return oauthStore.hasOneOfScopes(["virtual-assistants:edit"]);
});

const fetchData = () => {
  const { botId } = route.params;
  if (!botId) {
    return;
  }
  IntentService.getIntentsByBot(botId)
    .then((response: any) => {
      intents.value = response
    })
    .catch((error: any) => {
      console.error(error);
    });
  EntityService.getEntitiesByBot(botId)
    .then((response: any) => {
      entities.value = response
    })
    .catch((error: any) => {
      console.error(error);
    });
  ResponseService.getResponsesByBot(botId)
    .then((response: any) => {
      responses.value = response
    })
    .catch((error: any) => {
      console.error(error);
    });
}

onMounted(() => {
  fetchData();
});
</script>