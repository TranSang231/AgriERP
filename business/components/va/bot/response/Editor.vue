<template>
  <div class="flex flex-col justify-center pt-20 px-5 gap-2">
    <BackButton :historyBack="historyBack"/>
    <ModelForm
      :title="t('Name')"
      :collapsible="true"
      :editable="canEdit"
      :service="ResponseService"
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
              :placeholder="t('Variable_name_placeholder')"
            />
          </el-form-item>
          <el-form-item :label="t('Reply')" prop="text">
            <el-input
              :disabled="!scope.editing"
              v-model="scope.current.text"
              :placeholder="t('default_place_holder')"
            />
          </el-form-item>
        </div>
      </template>
    </ModelForm>
  </div>
</template>

<script setup lang="ts">
import { useOauthStore } from '@/stores/oauth'
import OAuthService from '@/services/oauth';
import ConstantsService from '@/services/constants';
import ResponseService from '@/services/va/response';

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
