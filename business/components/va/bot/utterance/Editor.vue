<template>
  <div class="flex flex-col justify-center pt-20 px-5">
    <BackButton class="mb-5" :historyBack="historyBack"/>
    <ModelForm
      :title="t('Utterance')" 
      :collapsible="true"
      :service="UtteranceService"
      :rules="utteranceRules"
      :editable="canEdit"
      :default="defaultData"
      :nestedFields="['entities']"
      ref="modelForm"
    >
      <template #default="scope">
        <div class="flex flex-col gap-2">
          <el-form-item :label="t('Utterance_text')" prop="text">
            <SelectableInput
              v-if="scope.editing"
              :highlight="highlight"
              :highlightEnabled="true"
              highlight-style="text-primary"
              v-model="scope.current.text"
              :placeholder="t('Variable_name_placeholder')"
              @selectText="onTextSelected"
            />
            <span v-else>{{ scope.current.text }}</span>
          </el-form-item>
          <el-form-item
            v-if="intents && intents.length>0"
            :label="t('Intent')"
            prop="slot_data_type"
          >
            <el-select
              v-if="scope.editing"
              :disabled="!scope.editing"
              collapse-tags
              value-key="id"
              v-model="scope.current.intent_id" 
              :placeholder="t('Pick_options')"
            >
              <el-option
                v-for="item in intents"
                :key="item.id"
                :label="item.name"
                :value="item.id"
              />
            </el-select>
            <span v-else>
              {{ intentName(scope.current.intent_id) }}
            </span>
          </el-form-item>
          <span class="italic">{{t('Guide_to_add_entity')}}</span>
          <el-table
            :data="scope.current.entities"
            stripe
            border
            table-layout="auto"
          >
            <el-table-column prop="name" :label="t('Entity')">
              <template #default="data">
                <el-select
                  v-if="entities"
                  :disabled="!scope.editing"
                  filterable
                  collapse-tags
                  value-key="id"
                  v-model="scope.current.entities[data.$index].entity_id"
                  :placeholder="t('Pick_options')"
                >
                  <el-option
                      v-for="item in entities"
                      :key="item.id"
                      :label="item.name"
                      :value="item.id"
                  />
                </el-select>
              </template>
            </el-table-column>
            <el-table-column prop="text" :label="t('Word_or_phrase')">
              <template #default="data">
                <span>{{data.row.text || ''}}</span>
              </template>
            </el-table-column>
            <el-table-column prop="start" :label="t('Start')">
              <template #default="data">
                <span>{{data.row.start || ''}}</span>
              </template>
            </el-table-column>
            <el-table-column prop="end" :label="t('End')">
              <template #default="data">
                <span>{{data.row.end || ''}}</span>
              </template>
            </el-table-column>
            <el-table-column
              v-if="scope.editing"
              :label="t('Operations')"
              :min-width="80"
            >
              <template #default="data">
                <el-button :icon="Delete" size="small" @click="removeEntity(data.$index)" />
              </template>
            </el-table-column>
          </el-table>
        </div>
      </template>
    </ModelForm>
    <el-dialog
      v-model="entityFormVisible"
      :title="t('Add_entity')"
      align-center
    >
      <el-form
        :model="entiy"
        :rules="entityRules"
        label-width="auto"
      >
        <el-form-item v-if="entiy.text" :label="t('Word_or_phrase')" prop="text">
          <span>{{ entiy.text }}</span>
        </el-form-item>
        <el-form-item v-if="entiy.start" :label="t('Start')" prop="start">
          <span>{{ entiy.start }}</span>
        </el-form-item>
        <el-form-item v-if="entiy.end" :label="t('End')" prop="end">
          <span>{{ entiy.end }}</span>
        </el-form-item>
        <el-form-item
          v-if="entities && entities.length>0"
          :label="t('Entity')"
          prop="entity_id"
        >
          <el-select
            collapse-tags
            value-key="id"
            v-model="entiy.entity_id" 
            :placeholder="t('Pick_options')"
          >
            <el-option
              v-for="item in entities"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="entityFormVisible = false">{{t('Cancel')}}</el-button>
          <el-button type="primary" @click="addEntity">
            {{t('Add')}}
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { Delete } from '@element-plus/icons-vue';
import { generateRandomHexColor } from '@/utils/color';
import { useOauthStore } from '@/stores/oauth';
import IntentService from '@/services/va/intent';
import EntityService from '@/services/va/entity';
import UtteranceService from '@/services/va/utterance';

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
const entiy = ref({
  utterance_id: route.params.id || null,
  entity_id: null,
  text: null,
  start: 0,
  end: 0,
  style:"background-color:#fff05e"
});
const entityFormVisible = ref(false);

const utteranceRules = {
  name: [
    { required: true, message: t('validate_error_required'), trigger: 'blur' }
  ]
};

const entityRules = {
  entity_id: [
    { required: true, message: t('validate_error_required'), trigger: 'blur' }
  ],
  start: [
    { required: true, message: t('validate_error_required'), trigger: 'blur' }
  ],
  end: [
    { required: true, message: t('validate_error_required'), trigger: 'blur' }
  ]
};

const text = computed(() => {
  if (!modelForm.value || !modelForm.value.current) {
    return null;
  }
  return modelForm.value.current.text;
});

const highlight = computed(() => {
  if (!modelForm.value || !modelForm.value.current) {
    return [];
  }
  const { entities } = modelForm.value.current;
  if (!entities) {
    return [];
  }
  return entities.map((o: any) => {
    const { start, end, style } = o;
    return {start, end, style};
  });
});

const canEdit = computed(() => {
  return oauthStore.hasOneOfScopes(["virtual-assistants:edit"]);
});

const intentName = (id:any) => {
  if (!intents.value || intents.value.lenth ===0) {
    return '';
  }
  const intent = intents.value.find((o:any) => o.id == id);
  return intent? intent.name : '';
}

const onTextSelected = ({text, start, end}) => {
  entiy.value = {
    utterance_id: route.params.id || null,
    entity_id: null,
    text,
    start,
    end,
    style: `background-color:${generateRandomHexColor()}`
  };
  entityFormVisible.value = true;
}

const addEntity = () => {
  if (modelForm.value) {
    modelForm.value.addItem("entities", _cloneDeep(entiy.value));
  }
  entityFormVisible.value = false;
}

const removeEntity = (index: number) => {
  if (modelForm.value) {
    modelForm.value.removeItemAt("entities", index);
  }
}

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
    })
}

const validateEntities = (u: string) => {
  if (!modelForm.value || !modelForm.value.current) {
    return;
  }
  const t = u || '';
  const length = t.length;
  const { entities } = modelForm.value.current;
  console.log(entities);
  if (!entities || entities.length === 0) {
    return;
  }
  const filtered = entities.filter((o: any) => {
    const { text, start, end } = o;
    return (end <= length) && t.includes(text)
  });
  console.log(filtered);
  if (filtered.length < entities.length) {
    modelForm.value.updateCurrentData('entities', filtered);
  }
}

watch(text, (newValue) => {
  validateEntities(newValue as string);
});

onMounted(() => {
  fetchData();
});
</script>