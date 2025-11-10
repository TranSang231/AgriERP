<template>
  <div class="flex flex-col justify-center pt-20 px-5">
    <BackButton class="mb-5" />
    <ModelForm
      :title="t('Goods_receipt')" 
      :collapsible="true"
      :service="GoodsReceiptService"
      :rules="rules"
      :editable="canEdit && !isApplied"
      :default="defaultData"
      :nestedFields="nestedFields"
      :sendFullOnUpdate="true"
      ref="modelForm"
    >
      <template #default="scope">
        <div class="flex flex-col gap-2">
          <el-form-item :label="t('Supplier')" prop="supplier_name">
            <el-input v-if="scope.editing" v-model="scope.current.supplier_name" :placeholder="t('default_place_holder')" type="text" />
            <span v-else>{{ scope.current.supplier_name }}</span>
          </el-form-item>
          <el-form-item :label="t('Reference_code')" prop="reference_code">
            <el-input v-if="scope.editing" v-model="scope.current.reference_code" :placeholder="t('default_place_holder')" type="text" />
            <span v-else>{{ scope.current.reference_code }}</span>
          </el-form-item>
          <el-form-item :label="t('Date')" prop="date">
            <el-date-picker v-if="scope.editing" v-model="scope.current.date" type="date" :format="FORMAT.DATE" :value-format="FORMAT.DATE" :placeholder="$t('pick_date_time')" />
            <span v-else>{{ utcToLocalDate(scope.current.date) }}</span>
          </el-form-item>
          <el-form-item :label="t('Note')" prop="note">
            <el-input v-if="scope.editing" v-model="scope.current.note" :placeholder="t('default_place_holder')" type="textarea" />
            <span v-else>{{ scope.current.note }}</span>
          </el-form-item>
          <el-divider class="my-4"/>
          <div class="flex flex-row items-center justify-between">
            <span>{{ t('Items') }}</span>
            <div class="flex flex-row gap-2">
              <el-button size="small" :icon="Plus" @click="onCreateProduct">{{ t('New_product') }}</el-button>
              <el-button size="small" :icon="Refresh" @click="onRefreshProducts">{{ t('Refresh') }}</el-button>
            </div>
          </div>
          <table>
            <tr>
              <th class="text-left px-2">{{ t('Product') }}</th>
              <th class="text-left px-2">{{ t('Unit') }}</th>
              <th class="text-right px-2">{{ t('Quantity') }}</th>
              <th class="text-right px-5">{{ t('Unit_cost') }}</th>
              <th class="text-right px-2">{{ t('Amount') }}</th>
              <th v-if="scope.editing" class="text-right px-2">{{ t('Operations') }}</th>
            </tr>
            <tr v-for="(item, index) in scope.current.items" :key="index">
              <td class="px-2">
                <el-select v-if="scope.editing" collapse-tags value-key="id" v-model="scope.current.items[index].product_id" :placeholder="t('Pick_options')" @change="(val) => onProductChange(val, index)">
                  <el-option v-for="p in productsStore.allProducts" :key="p.id" :label="p.name.origin" :value="p.id" />
                </el-select>
                <span v-else>{{ item.product_name || productsStore.productName(item.product_id) }}</span>
              </td>
              <td class="px-2">
                <span v-if="item.unit">{{ item.unit.origin }}</span>
                <span v-else-if="scope.current.items[index].product_id">{{ getProductUnit(scope.current.items[index].product_id) }}</span>
                <span v-else>-</span>
              </td>
              <td class="text-right px-2">
                <el-input v-if="scope.editing" v-model.number="scope.current.items[index].quantity" type="number" min="0" />
                <span v-else>{{ item.quantity }}</span>
              </td>
              <td class="text-right px-5">
                <el-input v-if="scope.editing" v-model.number="scope.current.items[index].unit_cost" type="number" min="0" />
                <span v-else>{{ item.unit_cost }}</span>
              </td>
              <td class="text-right px-2">
                {{ lineAmount(item).toLocaleString() }}
              </td>
              <td v-if="scope.editing" class="text-right px-2">
                <el-button :icon="Delete" size="small" @click="removeItem(index)" />
              </td>
            </tr>
          </table>
          <el-button v-if="scope.editing" :icon="Plus" @click="onAddItem()" class="self-end px-2"> {{ t('add_new') }} </el-button>
        </div>
        <el-divider />
        <div class="flex flex-row items-center justify-between">
          <span class="font-bold">{{ t('Total_ammount') }}: {{ totalAmount.toLocaleString() }} VND</span>
          <div class="flex flex-row gap-2 items-center">
            <!-- Apply Button -->
            <el-button 
              v-if="canEdit && scope.current && scope.current.id && !scope.current.is_applied" 
              type="primary" 
              @click="onApply(scope.current.id)"
            >
              {{ t('Apply') }}
            </el-button>
            
            <!-- Unapply Button -->
            <el-button 
              v-if="canEdit && scope.current && scope.current.id && scope.current.is_applied" 
              type="warning" 
              @click="onUnapply(scope.current.id)"
            >
              {{ t('Unapply') }}
            </el-button>
            
            <!-- Status Tag -->
            <el-tag v-if="scope.current && scope.current.is_applied" type="success">
              {{ t('Applied') }}
            </el-tag>
          </div>
        </div>
      </template>
    </ModelForm>
  </div>
</template>

<script setup>
import { FORMAT, utcToLocalDate } from '@/utils/time';
import { Plus, Delete} from "@element-plus/icons-vue";
import { Refresh } from "@element-plus/icons-vue";
import { useOauthStore } from "@/stores/oauth";
import { useProductsStore } from '@/stores/e-commerce/products';
import GoodsReceiptService from '@/services/e-commerce/goods_receipt';
import ProductService from '@/services/e-commerce/product';
import { ref, computed, onMounted } from 'vue';
import { useI18n } from 'vue-i18n';
import { ElMessageBox } from 'element-plus';

const props = defineProps({
  defaultData: {
    type: Object,
    default: null
  }
});

const { t } = useI18n();
const oauthStore = useOauthStore();
const productsStore = useProductsStore();
const modelForm = ref(null);

const nestedFields = ["items"];

const rules = {
  supplier_name: [
    { required: false }
  ],
  product_id: [
    { required: true, message: t('validate_error_required'), trigger: 'blur' }
  ],
  quantity: [
    { required: true, message: t('validate_error_required'), trigger: 'blur' }
  ]
};

const canEdit = computed(() => {
  return oauthStore.hasOneOfScopes(["ecommerce:goods-receipts:edit", "ecommerce:orders:edit"]);
});

const isApplied = computed(() => {
  return modelForm.value && modelForm.value.current && modelForm.value.current.is_applied;
});

const onAddItem = () => {
  if (modelForm.value) {
    let item = {
      product_id: null,
      quantity: 0,
      unit_cost: 0
    };
    if (modelForm.value && modelForm.value.current.id) {
      item = { ...item, receipt_id: modelForm.value.current.id };
    }
    modelForm.value.addItem("items", item);
  }
};

const removeItem = (index) => {
  if (modelForm.value) {
    modelForm.value.removeItemAt("items", index);
  }
}

const onProductChange = (id, index) => {
  // Auto-fill unit from product
  const product = productsStore.allProducts.find(p => p.id === id);
  if (product && product.unit && modelForm.value) {
    modelForm.value.current.items[index].unit_id = product.unit.id;
  }
}

const getProductUnit = (productId) => {
  const product = productsStore.allProducts.find(p => p.id === productId);
  return product && product.unit ? product.unit.origin : '-';
}

const lineAmount = (item) => {
  const q = item.quantity ? item.quantity : 0.0;
  const p = item.unit_cost ? item.unit_cost : 0.0;
  return q * p;
}

const totalAmount = computed(() => {
  if (!modelForm.value) {
    return 0.0;
  }
  const items = modelForm.value.current && modelForm.value.current.items
    ? modelForm.value.current.items
    : [];
  return items.reduce((a, c) => {
    return a + lineAmount(c);
  }, 0.0);
});

const onApply = async (id) => {
  await GoodsReceiptService.apply(id);
  // refresh
  location.reload();
}

const onUnapply = async (id) => {
  try {
    await ElMessageBox.confirm(
      t('Unapply_goods_receipt_confirm_message', 'This will reverse all stock changes made by this receipt. Are you sure you want to continue?'),
      t('Confirm_unapply', 'Confirm Unapply'),
      {
        confirmButtonText: t('Yes'),
        cancelButtonText: t('No'),
        type: 'warning',
      }
    );
    
    await GoodsReceiptService.unapply(id);
    // refresh
    location.reload();
  } catch (e) {
    if (e === 'cancel') {
      // User cancelled
      return;
    }
    throw e;
  }
}

onMounted(() => {
  // load products for dropdown
  ProductService.fetch();
});

const onCreateProduct = () => {
  window.open('/e-commerce/products/new', '_blank');
}

const onRefreshProducts = () => {
  ProductService.fetch(true);
}
</script>


