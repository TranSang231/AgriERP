<template>
  <div class="flex flex-col justify-center pt-20 px-5">
    <BackButton class="mb-5" />
    <ModelForm
      :title="t('Order')" 
      :collapsible="true"
      :service="OrderService"
      :rules="rules"
      :editable="canEdit"
      :default="defaultData"
			:nestedFields="nestedFields"
      contentType="multipart/form-data"
      ref="modelForm"
    >
      <template #default="scope">
        <div class="flex flex-col gap-2">
        <el-form-item
          :label="t('Customer')"
            prop="customer_id"
            :rules="rules.customer_id"
          >
            <el-select
              v-if="scope.editing"
              :disabled="!scope.editing"
              collapse-tags
              value-key="id"
              v-model="scope.current.customer_id" 
              :placeholder="t('Pick_options')"
              @change="onCustomerChange"
            >
              <el-option
                v-for="item in customersStore.allCustomers"
                :key="item.id"
                :label="`${item.first_name ? item.first_name + ' ': ''}${item.last_name ? item.last_name : ''}`"
                :value="item.id"
              />
            </el-select>
            <span v-else>
              {{ scope.current.customer_name }}
            </span>
          </el-form-item>
          <el-form-item :label="t('Company_name')" prop="company_name">
            <el-input
              v-if="scope.editing"
              v-model="scope.current.company_name"
              :placeholder="t('default_place_holder')"
              type="text"
            />
            <span v-else>{{ scope.current.company_name }}</span>
          </el-form-item>
          <el-form-item :label="t('Tax_code')" prop="tax_code">
            <el-input
              v-if="scope.editing"
              v-model="scope.current.tax_code"
              :placeholder="t('default_place_holder')"
              type="text"
            />
            <span v-else>{{ scope.current.tax_code }}</span>
          </el-form-item>
          <el-form-item
            :label="t('Payment_method')"
            prop="payment_method"
            :rules="rules.payment_method"
          >
            <el-select
              v-if="scope.editing"
              :disabled="!scope.editing"
              collapse-tags
              value-key="id"
              v-model="scope.current.payment_method" 
              :placeholder="t('Pick_options')"
            >
              <el-option
                v-for="item in constantsStore.paymentMethods"
                :key="item.value"
                :label="item.description"
                :value="item.value"
              />
            </el-select>
            <span v-else>
              {{ constantsStore.paymentMethodDescription(scope.current.payment_method) }}
            </span>
          </el-form-item>
          <el-form-item
            :label="t('Payment_status')"
            prop="payment_status"
            :rules="rules.payment_status"
          >
            <el-select
              v-if="scope.editing"
              :disabled="!scope.editing"
              collapse-tags
              value-key="id"
              v-model="scope.current.payment_status" 
              :placeholder="t('Pick_options')"
            >
              <el-option
                v-for="item in constantsStore.paymentStatuses"
                :key="item.value"
                :label="item.description"
                :value="item.value"
              />
            </el-select>
            <span v-else>
              {{ constantsStore.paymentStatusDescription(scope.current.payment_status) }}
            </span>
          </el-form-item>
          <el-form-item
            :label="t('Shipping_status')"
            prop="shipping_status"
            :rules="rules.shipping_status"
          >
            <el-select
              v-if="scope.editing"
              :disabled="!scope.editing"
              collapse-tags
              value-key="id"
              v-model="scope.current.shipping_status" 
              :placeholder="t('Pick_options')"
            >
              <el-option
                v-for="item in constantsStore.shippingStatuses"
                :key="item.value"
                :label="item.description"
                :value="item.value"
              />
            </el-select>
            <span v-else>
              {{ constantsStore.shippingStatusDescription(scope.current.shipping_status) }}
            </span>
          </el-form-item>
          <el-form-item :label="t('Date')" prop="date">
            <el-date-picker
              v-if="scope.editing"
              v-model="scope.current.date"
              type="date"
              :format="FORMAT.DATE"
               :value-format="FORMAT.DATE"
              :placeholder="$t('pick_date_time')"
            />
            <span v-else>{{ utcToLocalDate(scope.current.date) }}</span>
          </el-form-item>
          <el-divider class="my-4"/>
          <span>{{ t('Products') }}</span>
          <table>
            <tr>
              <th class="text-left px-2">{{ t('Product') }}</th>
              <th class="text-left px-2">{{ t('Unit') }}</th>
              <th class="text-right px-5">{{ t('Price') }}</th>
              <th class="text-right px-2">{{ t('Quantity') }}</th>
              <th class="text-right px-2">{{ t('Amount') }}</th>
            </tr>
            <EcommerceOrderItemEditor
              v-for="(item, index) in scope.current.items"
              v-model="scope.current.items[index]"
              :index="index"
              :editable="scope.editing"
              :products="productsStore.allProducts"
              :rules="rules"
            />
          </table>
          <el-button v-if="scope.editing" :icon="Plus" @click="onAddProduct()" class="self-end px-2"> {{ t("add_new") }} </el-button>
        </div>
        <el-divider />
        <div class="flex flex-col items-end gap-2">
          <span class="font-bold">{{t('Total_ammount')}}: {{totalAmount.toLocaleString()}} VND</span>
          <el-form-item :label="t('Shipping_fee')" prop="shipping_fee">
            <el-input
              v-if="scope.editing"
              v-model="scope.current.shipping_fee"
              :placeholder="t('default_place_holder')"
              type="text"
            />
            <span v-else>{{ scope.current.shipping_fee }}</span>
          </el-form-item>
          <span>{{t('VAT_rate') + ":" + vatRate.toString()}}</span>
          <span>{{t('VAT') + ":" + vat.toLocaleString()}} VND</span>
          <span class="font-bold">{{t('Total_to_pay')}}: {{totalToPay.toLocaleString()}} VND</span>
        </div>
      </template>
    </ModelForm>
  </div>
</template>

<script setup>
import { FORMAT, utcToLocalDate } from '@/utils/time';
import { Plus, Delete} from "@element-plus/icons-vue";
import ConstantsService from '@/services/constants';
import ProductService from '@/services/e-commerce/product';
import CustomerService from '@/services/e-commerce/customer';
import { useOauthStore } from "@/stores/oauth";
import { useConstantsStore } from '@/stores/constants';
import { useProductsStore } from '@/stores/e-commerce/products';
import { useCustomersStore } from '@/stores/e-commerce/customers';
import OrderService from '@/services/e-commerce/order';
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
const constantsStore = useConstantsStore();
const productsStore = useProductsStore();
const customersStore = useCustomersStore();
const modelForm = ref(null);

const onAddProduct = () => {
  if (modelForm.value) {
    console.log("onAddProduct")
    let item = {
      product_id: null,
      product_name: null,
      unit: null,
      quantity: 0,
      price: null
    }
    if (modelForm.value && modelForm.value.current.id) {
      item = { ...item, order_id: modelForm.value.current.id};
    }
    modelForm.value.addItem("items", item);
  }
}


const rules = {
  customer_id: [
    { required: true, message: t('validate_error_required'), trigger: 'blur' }
  ],
  product_id: [
    { required: true, message: t('validate_error_required'), trigger: 'blur' }
  ],
  quantity: [
    { required: true, message: t('validate_error_required'), trigger: 'blur' }
  ],
  payment_method: [
    { required: true, message: t('validate_error_required'), trigger: 'blur' }
  ],
  payment_status: [
    { required: true, message: t('validate_error_required'), trigger: 'blur' }
  ],
  shipping_status: [
    { required: true, message: t('validate_error_required'), trigger: 'blur' }
  ]
};

const canEdit = computed(() => {
  return oauthStore.hasOneOfScopes(["ecommerce:orders:edit"]);
});

const totalAmount = computed(() => {
  if (!modelForm.value) {
    return 0.0;
  }
  const items = modelForm.value.current && modelForm.value.current.items
    ? modelForm.value.current.items
    : [];
  return items.reduce((a, c) => {
    let {price, quantity} = c;
    price = price ? price: 0.0;
    quantity = quantity ? quantity: 0.0;
    return a + price*quantity;
  }, 0.0);
});

const vatRate = computed(() => {
  if (!modelForm.value) {
    console.log('return 0');
    return 0.0;
  }
  
  const items = modelForm.value.current && modelForm.value.current.items
    ? modelForm.value.current.items
    : [];
  console.log(items);
  
  const products = items
    .filter((o) => o.product_id)
    .map((o) => productsStore.getProduct(o.product_id));
  console.log(products);
  
  return products.reduce((a, c) => {
    let {tax_rate} = c;
    console.log(c);
    tax_rate = tax_rate ? tax_rate: 0.0;
    return tax_rate > a ? tax_rate: a;
  }, 0.0);
})

const vat = computed(() => {
  return (vatRate.value/100) * totalAmount.value;
})


const totalToPay = computed(() => {
  const t = totalAmount.value;
  const shippingFee = modelForm.value && modelForm.value.current && modelForm.value.current.shipping_fee
    ? modelForm.value.current.shipping_fee
    : 0.0;
  return totalAmount.value + vat.value + shippingFee;
});

const onCustomerChange = (id) => {
  if (modelForm.value) {
    modelForm.value.updateCurrentData(
      "customer_name",
      customersStore.customerName(id)
    );
  }
}

onMounted(() => {
  ConstantsService.fetch([
    "payment_methods",
    "payment_statuses",
    "shipping_statuses"
  ]);
  ProductService.fetch();
  CustomerService.fetch();
});
</script>