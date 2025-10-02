<template>
  <div class="flex flex-col justify-center pt-20 px-5 gap-2">
    <BackButton />
    <el-tabs type="border-card" class="w-full my-3" v-model="tab">
      <el-tab-pane :lazy=true :label="t('General')" name="general">
        <ModelForm
          :title="t('Name')"
          :collapsible="true"
          :editable="canEdit"
          :service="BotService"
          lookupField="botId"
          :nestedFields="['config', 'config.policies']"
          :default="defaultData"
          :rules="rules"
          ref="modelForm"
        >
          <template #default="scope">
            <div class="flex flex-col gap-2">
              <el-form-item :label="t('Name')" prop="name">
                <el-input
                  :disabled="!scope.editing"
                  v-model="scope.current.name"
                  :placeholder="t('default_place_holder')"
                />
              </el-form-item>
              <el-form-item :label="t('Server_output_folder')" prop="output_folder">
                <el-input
                  :disabled="!scope.editing"
                  v-model="scope.current.output_folder"
                  :placeholder="t('default_place_holder')"
                />
              </el-form-item>
              <el-form-item :label="t('Config')" prop="config" class="flex flex-col">
                <VaBotConfigEditor
                  v-model="scope.current.config"
                  :editable="scope.editing"
                />
              </el-form-item>
            </div>
          </template>
        </ModelForm>
      </el-tab-pane>
      <el-tab-pane v-if="route.params.botId" :lazy=true :label="t('Intents')" name="intents">
        <PaginationTable
          :pageSize="5"
          :canDeleteItems="canEdit"
          :canEditItems="canEdit"	
          :canAddItems="canEdit"
          :multipleSelect="canEdit"
          :allowExportToExcel="true"
          :allowExportToJson="true"
          :searchable="true"
          :service="IntentService"
          :filter="filter"
          prefix="intents"
        >
          <el-table-column
            prop="name"
            :label="t('Name')"
            min-width="120"
          />
          <el-table-column
            prop="created_at"
            :label="t('Created_at')"
            min-width="180"
          >
            <template #default="scope">
              {{ utcToLocalDateTime(scope.row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column
            prop="updated_at"
            :label="t('Updated_at')"
            min-width="180"
          >
            <template #default="scope">
              {{ utcToLocalDateTime(scope.row.updated_at) }}
            </template>
          </el-table-column>
        </PaginationTable>
      </el-tab-pane>
      <el-tab-pane v-if="route.params.botId" :lazy=true :label="t('Entities')" name="entities">
        <PaginationTable
          :pageSize="5"
          :canDeleteItems="canEdit"
          :canEditItems="canEdit"	
          :canAddItems="canEdit"
          :multipleSelect="canEdit"
          :allowExportToExcel="true"
          :allowExportToJson="true"
          :searchable="true"
          :service="EntityService"
          :filter="filter"
          prefix="entities"
        >
          <el-table-column
            prop="name"
            :label="t('Name')"
            min-width="120"
          />
          <el-table-column
            prop="slot_data_type"
            :label="t('Slot_data_type')"
          >
            <template #default="scope">
              {{ constantsStore.nluDataTypeDescription(scope.row.slot_data_type)}}
            </template>
          </el-table-column>
          <el-table-column
            prop="created_at"
            :label="t('Created_at')"
            min-width="180"
          >
            <template #default="scope">
              {{ utcToLocalDateTime(scope.row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column
            prop="updated_at"
            :label="t('Updated_at')"
            min-width="180"
          >
            <template #default="scope">
              {{ utcToLocalDateTime(scope.row.updated_at) }}
            </template>
          </el-table-column>
        </PaginationTable>
      </el-tab-pane>
      <el-tab-pane v-if="route.params.botId" :lazy=true :label="t('Synonyms')" name="synonyms">
        <PaginationTable
          :pageSize="5"
          :canDeleteItems="canEdit"
          :canEditItems="canEdit"	
          :canAddItems="canEdit"
          :multipleSelect="canEdit"
          :allowExportToExcel="true"
          :allowExportToJson="true"
          :searchable="true"
          :service="SynonymService"
          :filter="filter"
          prefix="synonyms"
        >
          <el-table-column
            prop="reference"
            :label="t('Reference_as')"
            min-width="120"
          />
          <el-table-column
            prop="created_at"
            :label="t('Created_at')"
            min-width="180"
          >
            <template #default="scope">
              {{ utcToLocalDateTime(scope.row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column
            prop="updated_at"
            :label="t('Updated_at')"
            min-width="180"
          >
            <template #default="scope">
              {{ utcToLocalDateTime(scope.row.updated_at) }}
            </template>
          </el-table-column>
        </PaginationTable>
      </el-tab-pane>
      <el-tab-pane v-if="route.params.botId" :lazy=true :label="t('Responses')" name="responses">
        <PaginationTable
          :pageSize="5"
          :canDeleteItems="canEdit"
          :canEditItems="canEdit"	
          :canAddItems="canEdit"
          :multipleSelect="canEdit"
          :allowExportToExcel="true"
          :allowExportToJson="true"
          :searchable="true"
          :service="ResponseService"
          :filter="filter"
          prefix="responses"
        >
          <el-table-column
            prop="name"
            :label="t('Name')"
            min-width="120"
          />
          <el-table-column
            prop="created_at"
            :label="t('Created_at')"
            min-width="180"
          >
            <template #default="scope">
              {{ utcToLocalDateTime(scope.row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column
            prop="updated_at"
            :label="t('Updated_at')"
            min-width="180"
          >
            <template #default="scope">
              {{ utcToLocalDateTime(scope.row.updated_at) }}
            </template>
          </el-table-column>
        </PaginationTable>
      </el-tab-pane>
      <el-tab-pane v-if="route.params.botId" :lazy=true :label="t('Utterances')" name="utterances">
        <PaginationTable
          :pageSize="5"
          :canDeleteItems="canEdit"
          :canEditItems="canEdit"	
          :canAddItems="canEdit"
          :multipleSelect="canEdit"
          :allowExportToExcel="true"
          :allowExportToJson="true"
          :searchable="true"
          :service="UtteranceService"
          :filter="filter"
          prefix="utterances"
        >
          <el-table-column
            prop="text"
            :label="t('Utterance_text')"
            min-width="120"
          />
          <el-table-column
            prop="created_at"
            :label="t('Created_at')"
            min-width="180"
          >
            <template #default="scope">
              {{ utcToLocalDateTime(scope.row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column
            prop="updated_at"
            :label="t('Updated_at')"
            min-width="180"
          >
            <template #default="scope">
              {{ utcToLocalDateTime(scope.row.updated_at) }}
            </template>
          </el-table-column>
        </PaginationTable>
      </el-tab-pane>
      <el-tab-pane v-if="route.params.botId" :lazy=true :label="t('Stories')" name="stories">
        <PaginationTable
          :pageSize="5"
          :canDeleteItems="canEdit"
          :canEditItems="canEdit"	
          :canAddItems="canEdit"
          :multipleSelect="canEdit"
          :allowExportToExcel="true"
          :allowExportToJson="true"
          :searchable="true"
          :service="StoryService"
          :filter="filter"
          prefix="stories"
        >
          <el-table-column
            prop="name"
            :label="t('Name')"
            min-width="120"
          />
          <el-table-column
            prop="created_at"
            :label="t('Created_at')"
            min-width="180"
          >
            <template #default="scope">
              {{ utcToLocalDateTime(scope.row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column
            prop="updated_at"
            :label="t('Updated_at')"
            min-width="180"
          >
            <template #default="scope">
              {{ utcToLocalDateTime(scope.row.updated_at) }}
            </template>
          </el-table-column>
        </PaginationTable>
      </el-tab-pane>
      <el-tab-pane v-if="route.params.botId" :lazy=true :label="t('Rules')" name="rules">
        <PaginationTable
          :pageSize="5"
          :canDeleteItems="canEdit"
          :canEditItems="canEdit"	
          :canAddItems="canEdit"
          :multipleSelect="canEdit"
          :allowExportToExcel="true"
          :allowExportToJson="true"
          :searchable="true"
          :service="RuleService"
          :filter="filter"
          prefix="rules"
        >
          <el-table-column
            prop="name"
            :label="t('Name')"
            min-width="120"
          />
          <el-table-column
            prop="created_at"
            :label="t('Created_at')"
            min-width="180"
          >
            <template #default="scope">
              {{ utcToLocalDateTime(scope.row.created_at) }}
            </template>
          </el-table-column>
          <el-table-column
            prop="updated_at"
            :label="t('Updated_at')"
            min-width="180"
          >
            <template #default="scope">
              {{ utcToLocalDateTime(scope.row.updated_at) }}
            </template>
          </el-table-column>
        </PaginationTable>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { utcToLocalDateTime } from "@/utils/time";
import { useOauthStore } from '@/stores/oauth'
import { useConstantsStore } from '@/stores/constants';
import OAuthService from '@/services/oauth';
import ConstantsService from '@/services/constants';
import BotService from '@/services/va/bot';
import IntentService from '@/services/va/intent';
import EntityService from '@/services/va/entity';
import ResponseService from '@/services/va/response';
import UtteranceService from '@/services/va/utterance';
import SynonymService from '@/services/va/synonym';
import StoryService from '@/services/va/story';
import RuleService from '@/services/va/rule';

const props = defineProps({
	defaultData: {
		type: Object,
		default: null
	},
});

const { t } = useI18n();
const route = useRoute();
const oauthStore = useOauthStore();
const constantsStore = useConstantsStore();
const tab = ref<string>(route.query.tab ? route.query.tab as string : 'general')
const modelForm = ref<any>(null);

const rules = {
  name: [
    { required: true, message: t('validate_error_required'), trigger: 'blur' }
  ]
};

const fetchData = () => {
  ConstantsService.fetch("nlu_data_types");
  OAuthService.fetchScopes();
};

const canEdit = computed(() => {
  return oauthStore.hasOneOfScopes(["virtual-assistants:edit"]);
})

const filter = computed(() => {
  const { botId } = route.params;
  if (!botId) {
    return {}
  }
  return { bot__id: botId };
})

watch(tab, (newValue) => {
  // Update the query parameter without redender components.
  const queryParams = new URLSearchParams(window.location.search);
  queryParams.set('tab', newValue);
  history.replaceState(null, '', "?"+queryParams.toString());
});

onMounted(() => {
    fetchData();
});
</script>
