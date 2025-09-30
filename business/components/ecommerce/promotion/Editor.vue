<template>
  <div class="flex flex-col justify-center pt-20 px-5">
    <BackButton class="mb-5" />
    <ModelForm
      :title="$t('Promotion')" 
      :collapsible="true"
      :service="PromotionService"
      :rules="rules"
      :editable="canEdit"
      :default="defaultData"
			:nestedFields="nestedFields"
      contentType="multipart/form-data"
      ref="modelForm"
    >
      <template #default="scope">
        <div class="flex flex-col gap-2">
          <el-form-item :label="t('Name')" prop="name">
            <el-input
              v-if="scope.editing"
              v-model="scope.current.name"
              :placeholder="t('default_place_holder')"
              type="text"
            />
            <span v-else>{{ scope.current.name }}</span>
          </el-form-item>
          <el-form-item :label="t('Start')" prop="start">
            <el-date-picker
              v-if="scope.editing"
              v-model="scope.current.start"
              type="datetime"
              :format="FORMAT.DATE_TIME"
               :value-format="FORMAT.DATE_TIME"
              :placeholder="$t('pick_date_time')"
            />
            <span v-else>{{ utcToLocalDateTime(scope.current.start) }}</span>
          </el-form-item>
          <el-form-item :label="t('End')" prop="end">
            <el-date-picker
              v-if="scope.editing"
              v-model="scope.current.end"
              type="datetime"
              :format="FORMAT.DATE_TIME"
              :value-format="FORMAT.DATE_TIME"
              :placeholder="t('pick_date_time')"
            />
            <span v-else>{{ utcToLocalDateTime(scope.current.end) }}</span>
          </el-form-item>
          <el-form-item :label="t('Type')" prop="type">
            <el-select
              v-if="scope.editing"
              v-model="scope.current.type"
              :placeholder="t('Pick_options')"
            >
              <el-option :label="t('Discount')" value="discount" />
              <el-option :label="t('Voucher')" value="voucher" />
            </el-select>
            <span v-else>{{ scope.current.type }}</span>
          </el-form-item>
          <el-form-item v-if="scope.current.type === 'voucher'" :label="t('Discount')" prop="discount">
            <el-input
              v-if="scope.editing"
              v-model="scope.current.discount"
              :placeholder="t('default_place_holder')"
              type="number"
            />
            <span v-else>{{ scope.current.discount }}</span>
          </el-form-item>
          <el-divider class="my-4"/>
          <span v-if="scope.current.type === 'discount'">{{ t('Products') }}</span>
          <table v-if="scope.current.type === 'discount'">
            <tr>
              <th class="text-left">{{ t('Product') }}</th>
              <th class="text-left">{{ t('Discount') }}</th>
              <th class="text-left">{{ t('Quantity_limit') }}</th>
              <th class="text-left">{{ t('Quantity_limit_by_customer') }}</th>
            </tr>
            <tr v-for="item, index in scope.current.promotion_items">
              <td>
                <el-form-item
                  :prop="`promotion_items[${index}].product`"
                  :rules="rules.first_name"
                  class="flex min-w-80"
                >
                  <el-select
                    v-if="scope.editing"
                    :disabled="!scope.editing"
                    collapse-tags
                    value-key="id"
                    v-model="scope.current.promotion_items[index].product_id" 
                    :placeholder="t('Pick_options')"
                  >
                    <el-option
                      v-for="item in productsStore.allProducts"
                      :key="item.id"
                      :label="item.name?.origin"
                      :value="item.id"
                    />
                  </el-select>
                  <span v-else>
                    {{ productsStore.productName(scope.current.promotion_items[index].product_id) }}
                  </span>
                </el-form-item>
              </td>
              <td>
                <el-form-item
                  :prop="`promotion_items[${index}].discount`"
                  :rules="rules.discount"
                >
                  <el-input
                      v-if="scope.editing"
                      v-model="scope.current.promotion_items[index].discount"
                      :placeholder="$t('default_place_holder')"
                      type="number"
                  />
                  <span v-else>{{scope.current.promotion_items[index].discount}}</span>
                </el-form-item>
              </td>
              <td>
                <el-form-item
                  :prop="`promotion_items[${index}].quantity_limit`"
                  :rules="rules.quantity_limit"
                >
                  <el-input
                      v-if="scope.editing"
                      v-model="scope.current.promotion_items[index].quantity_limit"
                      :placeholder="t('default_place_holder')"
                      type="number"
                  />
                  <span v-else>{{scope.current.promotion_items[index].quantity_limit}}</span>
                </el-form-item>
              </td>
              <td>
                <el-form-item
                  :prop="`promotion_items[${index}].quantity_limit_by_customer`"
                  :rules="rules.quantity_limit_by_customer"
                >
                  <el-input
                      v-if="scope.editing"
                      v-model="scope.current.promotion_items[index].quantity_limit_by_customer"
                      :placeholder="$t('default_place_holder')"
                      type="number"
                  />
                  <span v-else>{{scope.current.promotion_items[index].quantity_limit_by_customer}}</span>
                </el-form-item>
              </td>
            </tr>
          </table>
          <el-button v-if="scope.editing && scope.current.type === 'discount'" :icon="Plus" @click="onAddProduct()" class="self-end px-2"> {{ t("add_new") }} </el-button>
        </div>
      </template>
    </ModelForm>
  </div>
</template>

<script setup>
import { FORMAT, utcToLocalDateTime } from '@/utils/time';
import { Plus, Delete} from "@element-plus/icons-vue";
import ProductService from '@/services/e-commerce/product';
import { useOauthStore } from "@/stores/oauth";
import { useProductsStore } from '@/stores/e-commerce/products';
import PromotionService from '@/services/e-commerce/promotion';
import { useI18n } from 'vue-i18n';
import { computed } from 'vue';

const props = defineProps({
	defaultData: {
		type: Object,
		default: null
	}
});

const { t } = useI18n();
const nestedFields = ["promotion_items"];
const oauthStore = useOauthStore();
const productsStore = useProductsStore();
const modelForm = ref(null);

const onAddProduct = () => {
  if (modelForm.value) {
    console.log("onAddProduct")
    let item = {
      product_id: null,
      discount: null,
      quantity_limit: null,
      quantity_limit_by_customer: null
    }
    if (modelForm.value && modelForm.value.current.id) {
      item = { ...item, promotion_id: modelForm.value.current.id};
    }
    modelForm.value.addItem("promotion_items", item);
  }
}


const rules = {
  name: [
    { required: true, message: t('validate_error_required'), trigger: 'blur' }
  ],
  start: [
    { required: true, message: t('validate_error_required'), trigger: 'blur' }
  ],
  end: [
    { required: true, message: t('validate_error_required'), trigger: 'blur' }
  ]
};

const canEdit = computed(() => {
  return oauthStore.hasOneOfScopes(["ecommerce:products:edit"]);
});

onMounted(() => {
  ProductService.fetch();
});
</script>