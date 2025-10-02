<template>
  <div class="flex flex-col justify-center pt-20 px-5">
    <BackButton class="mb-5" :historyBack="historyBack"/>
    <ModelForm
      :title="t('Synonym')" 
      :collapsible="true"
      :service="SynonymService"
      :rules="rules"
      :editable="canEdit"
      :default="defaultData"
      :nestedFields="['variants']"
      ref="modelForm"
    >
      <template #default="scope">
        <div class="flex flex-col gap-2">
          <el-form-item :label="t('Reference_as')" prop="reference">
            <el-input
              v-if="scope.editing"
              :disabled="!scope.editing"
              v-model="scope.current.reference"
              :placeholder="t('synonym_reference_placeholder')"
            />
            <span v-else>
              {{ scope.current.reference }}
            </span>
          </el-form-item>
          <TagEditor
            v-if="route.params && route.params.id"
            v-model="scope.current.variants"
            field="value"
            :itemTemplate="variantTemplate"
            :editable="scope.editing"
          />
        </div>
      </template>
    </ModelForm>
  </div>
</template>

<script setup lang="ts">
import { Delete } from '@element-plus/icons-vue';
import { useOauthStore } from '@/stores/oauth';
import SynonymService from '@/services/va/synonym';

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

const rules = {
  name: [
    { required: true, message: t('validate_error_required'), trigger: 'blur' }
  ]
};

const canEdit = computed(() => {
  return oauthStore.hasOneOfScopes(["virtual-assistants:edit"]);
});

const variantTemplate = computed(() => {
  const { id } = route.params;
  if (!id) {
    return {};
  }
  return { synonym_id: id};
});
</script>