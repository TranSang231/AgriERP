<template>
  <div class="flex flex-col justify-center pt-20 px-5">
    <BackButton class="mb-5" :historyBack="historyBack"/>
    <ModelForm
      :title="t('Name')" 
      :collapsible="true"
      :service="EntityService"
      :rules="rules"
      :editable="canEdit"
      :default="defaultData"
    >
      <template #default="scope">
        <div class="flex flex-col gap-2">
          <el-form-item :label="t('Name')" prop="name">
            <el-input
              v-if="scope.editing"
              v-model="scope.current.name"
              :placeholder="t('Variable_name_placeholder')"
            />
            <span v-else>{{ scope.current.name }}</span>
          </el-form-item>
          <el-form-item
            :label="t('Slot_data_type')"
            prop="slot_data_type"
          >
            <el-select
              v-if="scope.editing"
              :disabled="!scope.editing"
              collapse-tags
              value-key="id"
              v-model="scope.current.slot_data_type" 
              :placeholder="t('Pick_options')"
            >
              <el-option
                v-for="item in constantsStore.nluDataTypes"
                :key="item.value"
                :label="item.description"
                :value="item.value"
              />
            </el-select>
            <span v-else>
              {{ constantsStore.nluDataTypeDescription(scope.current.slot_data_type) }}
            </span>
          </el-form-item>
        </div>
      </template>
    </ModelForm>
  </div>
</template>

<script setup lang="ts">
import { useOauthStore } from "@/stores/oauth";
import { useConstantsStore } from '@/stores/constants';
import ConstantsService from '@/services/constants';
import EntityService from "@/services/va/entity";

import { useI18n } from "vue-i18n";
import { computed } from "vue";

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
const oauthStore = useOauthStore();
const constantsStore = useConstantsStore();

const rules = {
  name: [
    { required: true, message: t('validate_error_required'), trigger: 'blur' }
  ]
};

const canEdit = computed(() => {
  return oauthStore.hasOneOfScopes(["virtual-assistants:edit"]);
});

onMounted(() => {
  ConstantsService.fetch("nlu_data_types");
});
</script>