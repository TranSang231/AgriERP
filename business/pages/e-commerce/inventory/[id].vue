<template>
  <div class="pt-24 p-6 bg-gray-50 min-h-screen">
    <!-- Header -->
    <div class="mb-8">
      <div class="flex items-center justify-between">
        <div>
          <div class="flex items-center gap-4 mb-4">
            <el-button @click="$router.back()" type="text">
              <el-icon><ArrowLeft /></el-icon>
              {{ t('Back') }}
            </el-button>
            <h1 class="text-3xl font-bold text-gray-900">{{ t('Inventory_Details') }}</h1>
          </div>
          <p class="text-gray-600">{{ t('Product_inventory_history_and_details') }}</p>
        </div>
        <div class="flex gap-2">
          <el-button type="primary" @click="adjustStock">
            <el-icon><Edit /></el-icon>
            {{ t('Adjust_Stock') }}
          </el-button>
          <el-button type="success" @click="addStock">
            <el-icon><Plus /></el-icon>
            {{ t('Add_Stock') }}
          </el-button>
        </div>
      </div>
    </div>

    <!-- Product Info Card -->
    <el-card class="mb-6" v-if="productInfo">
      <div class="flex items-start gap-6">
        <div class="w-32 h-32 bg-gray-200 rounded-lg flex items-center justify-center">
          <el-image
            v-if="productInfo?.product?.thumbnail"
            :src="getImageUrl(productInfo?.product?.thumbnail)"
            fit="cover"
            class="w-full h-full rounded-lg"
          />
          <el-icon v-else class="text-gray-400 text-4xl"><Picture /></el-icon>
        </div>
        
        <div class="flex-1">
          <h2 class="text-2xl font-bold text-gray-900 mb-2">
            {{ productInfo?.product?.name?.origin || productInfo?.product?.name }}
          </h2>
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
            <div>
              <p class="text-sm text-gray-600">{{ t('SKU') }}</p>
              <p class="font-medium">{{ productInfo.product?.sku || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-600">{{ t('Unit') }}</p>
              <p class="font-medium">{{ productInfo?.product?.unit?.origin || productInfo?.product?.unit || '-' }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-600">{{ t('Unit_Price') }}</p>
              <p class="font-medium">{{ formatCurrency(productInfo.product?.price || 0) }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-600">{{ t('Categories') }}</p>
              <div class="flex flex-wrap gap-1">
                <el-tag
                  v-for="category in productInfo.product?.categories"
                  :key="category.id"
                  size="small"
                  type="primary"
                >
                  {{ category.name?.origin || category.name }}
                </el-tag>
              </div>
            </div>
          </div>
        </div>
      </div>
    </el-card>

    <!-- Current Stock Status -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
      <!-- Current Stock -->
      <el-card>
        <div class="text-center">
          <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <el-icon :size="32" class="text-blue-600"><Box /></el-icon>
          </div>
          <h3 class="text-2xl font-bold text-gray-900 mb-2">
            {{ productInfo?.current_quantity || 0 }}
          </h3>
          <p class="text-gray-600">{{ t('Current_Stock') }}</p>
        </div>
      </el-card>

      <!-- Min Stock -->
      <el-card>
        <div class="text-center">
          <div class="w-16 h-16 bg-yellow-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <el-icon :size="32" class="text-yellow-600"><Warning /></el-icon>
          </div>
          <h3 class="text-2xl font-bold text-gray-900 mb-2">
            {{ productInfo?.min_quantity || 0 }}
          </h3>
          <p class="text-gray-600">{{ t('Min_Stock') }}</p>
        </div>
      </el-card>

      <!-- Stock Value -->
      <el-card>
        <div class="text-center">
          <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <el-icon :size="32" class="text-green-600"><Money /></el-icon>
          </div>
          <h3 class="text-2xl font-bold text-gray-900 mb-2">
            {{ formatCurrency((productInfo?.product?.price || 0) * (productInfo?.current_quantity || 0)) }}
          </h3>
          <p class="text-gray-600">{{ t('Stock_Value') }}</p>
        </div>
      </el-card>
    </div>

    <!-- Filters -->
    <el-card class="mb-6">
      <div class="flex flex-wrap items-center gap-4">
        <el-date-picker
          v-model="dateRange"
          type="daterange"
          :range-separator="t('to')"
          :start-placeholder="t('Start_date')"
          :end-placeholder="t('End_date')"
          format="DD/MM/YYYY"
          value-format="YYYY-MM-DD"
          @change="handleDateChange"
        />
        
        <el-select
          v-model="transactionType"
          :placeholder="t('All_Transaction_Types')"
          clearable
          style="width: 200px"
          @change="handleFilterChange"
        >
          <el-option :label="t('Stock_In')" value="in" />
          <el-option :label="t('Stock_Out')" value="out" />
          <el-option :label="t('Adjustment')" value="adjust" />
          <el-option :label="t('Reserve')" value="reserve" />
          <el-option :label="t('Unreserve')" value="unreserve" />
        </el-select>

        <el-button @click="refreshData">
          <el-icon><Refresh /></el-icon>
          {{ t('Refresh') }}
        </el-button>
      </div>
    </el-card>

    <!-- Transaction History -->
    <el-card>
      <template #header>
        <h3 class="text-lg font-semibold text-white">{{ t('Transaction_History') }}</h3>
      </template>

      <el-table
        :data="transactionHistory"
        v-loading="loading"
        stripe
        style="width: 100%"
      >
        <el-table-column prop="created_at" :label="t('Date')" width="150">
          <template #default="scope">
            {{ formatDateTime(scope.row.created_at) }}
          </template>
        </el-table-column>

        <el-table-column prop="type" :label="t('Type')" width="120">
          <template #default="scope">
            <el-tag :type="getTransactionTypeTag(scope.row.transaction_type)">
              {{ getTransactionTypeText(scope.row.transaction_type) }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="quantity" :label="t('Quantity')" width="150">
          <template #default="scope">
            <span 
              class="font-bold"
              :class="scope.row.transaction_type === 'in' ? 'text-green-600' : scope.row.transaction_type === 'out' ? 'text-red-600' : 'text-blue-600'"
            >
              {{ scope.row.transaction_type === 'in' ? '+' : scope.row.transaction_type === 'out' ? '-' : '±' }}{{ Math.abs(scope.row.quantity) }}
            </span>
          </template>
        </el-table-column>

        <el-table-column prop="reference" :label="t('Reference')" min-width="200">
          <template #default="scope">
            <div>
              <p class="font-medium text-sm">{{ scope.row.reference_number || '-' }}</p>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="reason" :label="t('Reason')" min-width="200">
          <template #default="scope">
            {{ scope.row.reason || '-' }}
          </template>
        </el-table-column>

        <el-table-column prop="user" :label="t('User')" width="150">
          <template #default="scope">
            {{ scope.row.user?.name || '-' }}
          </template>
        </el-table-column>
      </el-table>

      <!-- Pagination -->
      <div class="flex justify-center mt-6">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="totalItems"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>

    <!-- Adjust Stock Dialog -->
    <el-dialog
      v-model="adjustStockDialogVisible"
      :title="t('Adjust_Stock')"
      width="500px"
    >
      <el-form :model="adjustForm" label-width="120px">
        <el-form-item :label="t('Product')">
          <el-input :value="productInfo?.product?.name?.origin || productInfo?.product?.name" disabled />
        </el-form-item>
        <el-form-item :label="t('Current_Stock')">
          <el-input :value="productInfo?.current_quantity || 0" disabled />
        </el-form-item>
        <el-form-item :label="t('Adjustment_Type')" required>
          <el-select v-model="adjustForm.type" style="width: 100%">
            <el-option :label="t('Add_Stock')" value="add" />
            <el-option :label="t('Remove_Stock')" value="remove" />
            <el-option :label="t('Set_Stock')" value="set" />
          </el-select>
        </el-form-item>
        <el-form-item :label="t('Quantity')" required>
          <el-input-number
            v-model="adjustForm.quantity"
            :min="adjustForm.type === 'remove' ? 1 : 0"
            :max="adjustForm.type === 'add' ? 999999 : productInfo?.current_quantity"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item :label="t('Reason')">
          <el-input
            v-model="adjustForm.reason"
            type="textarea"
            :rows="3"
            :placeholder="t('Enter_reason_for_adjustment')"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="adjustStockDialogVisible = false">{{ t('Cancel') }}</el-button>
        <el-button type="primary" @click="confirmAdjustStock" :loading="adjusting">
          {{ t('Confirm') }}
        </el-button>
      </template>
    </el-dialog>

    <!-- Add Stock Dialog -->
    <el-dialog
      v-model="addStockDialogVisible"
      :title="t('Add_Stock')"
      width="500px"
    >
      <el-form :model="addStockForm" label-width="120px">
        <el-form-item :label="t('Product')">
          <el-input :value="productInfo?.product?.name?.origin || productInfo?.product?.name" disabled />
        </el-form-item>
        <el-form-item :label="t('Current_Stock')">
          <el-input :value="productInfo?.current_quantity || 0" disabled />
        </el-form-item>
        <el-form-item :label="t('Quantity_to_Add')" required>
          <el-input-number
            v-model="addStockForm.quantity"
            :min="1"
            :max="999999"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item :label="t('Reference')">
          <el-input
            v-model="addStockForm.reference"
            :placeholder="t('Purchase_order_number_or_reference')"
          />
        </el-form-item>
        <el-form-item :label="t('Notes')">
          <el-input
            v-model="addStockForm.notes"
            type="textarea"
            :rows="3"
            :placeholder="t('Additional_notes')"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="addStockDialogVisible = false">{{ t('Cancel') }}</el-button>
        <el-button type="primary" @click="confirmAddStock" :loading="adding">
          {{ t('Confirm') }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRoute } from 'vue-router';
import {
  ArrowLeft,
  Edit,
  Plus,
  Picture,
  Box,
  Warning,
  Money,
  Refresh
} from '@element-plus/icons-vue';
import InventoryService from '@/services/e-commerce/inventory';
import { formatDateTime } from '~/utils/time';
import { ElMessage } from 'element-plus';

definePageMeta({
  layout: 'ecommerce'
});

const { t } = useI18n();
const route = useRoute();

// Types
interface ProductInfo {
  id: string | string[];
  product: {
    id: string | string[];
    name: { origin: string } | string;
    sku: string;
    thumbnail: string;
    price: number;
    unit: { origin: string } | string;
    categories: Array<{ id: number; name: { origin: string } | string }>;
  };
  current_quantity: number;
  min_quantity: number;
  max_quantity: number;
  updated_at: string;
}

interface TransactionHistoryItem {
  id: number;
  type: string;
  quantity: number;
  balance_after: number;
  reference_type: string;
  reference_id: string;
  reason: string;
  user: { name: string };
  created_at: string;
}

// Reactive data
const loading = ref(false);
const productInfo = ref<ProductInfo | null>(null);
const transactionHistory = ref<TransactionHistoryItem[]>([]);

// Filters
const dateRange = ref([]);
const transactionType = ref('');

// Pagination
const currentPage = ref(1);
const pageSize = ref(20);
const totalItems = ref(0);

// Dialogs
const adjustStockDialogVisible = ref(false);
const addStockDialogVisible = ref(false);
const adjusting = ref(false);
const adding = ref(false);

// Forms
const adjustForm = ref({
  type: 'add',
  quantity: 0,
  reason: ''
});

const addStockForm = ref({
  quantity: 0,
  reference: '',
  notes: ''
});

// Methods
const formatCurrency = (amount: number) => {
  return new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND'
  }).format(amount);
};

const getImageUrl = (thumbnail: string | null): string | null => {
  if (!thumbnail) return null;
  
  if (thumbnail.startsWith('http://') || thumbnail.startsWith('https://')) {
    return thumbnail;
  }
  
  const runtimeConfig = useRuntimeConfig();
  const baseUrl = runtimeConfig.public.defaultHost;
  return `${baseUrl}${thumbnail.startsWith('/') ? '' : '/'}${thumbnail}`;
};

const getTransactionTypeTag = (type: string) => {
  const typeMap: Record<string, string> = {
    'in': 'success',
    'out': 'danger',
    'adjust': 'warning',
    'reserve': 'info',
    'unreserve': 'info'
  };
  return typeMap[type] || 'info';
};

const getTransactionTypeText = (type: string) => {
  const typeMap: Record<string, string> = {
    'in': t('Stock_In'),
    'out': t('Stock_Out'),
    'adjust': t('Adjustment'),
    'reserve': t('Reserve'),
    'unreserve': t('Unreserve')
  };
  return typeMap[type] || type;
};

const loadProductInfo = async () => {
  const productId = route.params.id;
  try {
    const response = await InventoryService.getInventoryItem(productId);
    productInfo.value = response;
  } catch (error) {
    console.error('Error loading product info:', error);
    ElMessage.error(t('Failed_to_load_product_info'));
    // Fallback to mock data
    productInfo.value = {
      id: productId,
      product: {
        id: productId,
        name: { origin: 'iPhone 15 Pro' },
        sku: 'IPH15P-001',
        thumbnail: '/images/products/iphone15.jpg',
        price: 29990000,
        unit: { origin: 'Cái' },
        categories: [{ id: 1, name: { origin: 'Điện thoại' } }]
      },
      current_quantity: 15,
      min_quantity: 10,
      max_quantity: 100,
      updated_at: '2024-01-15T10:30:00Z'
    };
  }
};

const loadTransactionHistory = async () => {
  loading.value = true;
  try {
    const productId = route.params.id;
    const params = {
      transaction_type: transactionType.value,
      start_date: dateRange.value?.[0],
      end_date: dateRange.value?.[1]
    };
    
    // Call the history endpoint
    const response = await InventoryService.getInventoryHistory(productId, params);
    console.log('Transaction history response:', response);
    
    // Handle response - API returns array directly
    if (Array.isArray(response)) {
      transactionHistory.value = response;
    } else if (response && response.data && Array.isArray(response.data)) {
      transactionHistory.value = response.data;
    } else {
      transactionHistory.value = [];
    }
    
    totalItems.value = transactionHistory.value.length;
    
    console.log('Transaction history loaded:', transactionHistory.value.length, 'items');
  } catch (error) {
    console.error('Error loading transaction history:', error);
    // Don't show error message if it's just a 404 (no history yet)
    if (!error.response || error.response.status !== 404) {
      ElMessage.error(t('Failed_to_load_transaction_history'));
    }
    // Set empty array on error
    transactionHistory.value = [];
    totalItems.value = 0;
  } finally {
    loading.value = false;
  }
};

const handleDateChange = () => {
  currentPage.value = 1;
  loadTransactionHistory();
};

const handleFilterChange = () => {
  currentPage.value = 1;
  loadTransactionHistory();
};

const handleSizeChange = (size: number) => {
  pageSize.value = size;
  currentPage.value = 1;
  loadTransactionHistory();
};

const handleCurrentChange = (page: number) => {
  currentPage.value = page;
  loadTransactionHistory();
};

const adjustStock = () => {
  adjustForm.value = {
    type: 'add',
    quantity: 0,
    reason: ''
  };
  adjustStockDialogVisible.value = true;
};

const addStock = () => {
  addStockForm.value = {
    quantity: 0,
    reference: '',
    notes: ''
  };
  addStockDialogVisible.value = true;
};

const confirmAdjustStock = async () => {
  if (!adjustForm.value.quantity || adjustForm.value.quantity <= 0) {
    ElMessage.warning(t('Please_enter_valid_quantity'));
    return;
  }

  adjusting.value = true;
  try {
    if (!productInfo.value) {
      ElMessage.error(t('Product_info_not_available'));
      return;
    }
    await InventoryService.updateInventoryQuantity(
      productInfo.value.id,
      adjustForm.value.quantity,
      adjustForm.value.type
    );
    
    ElMessage.success(t('Stock_adjusted_successfully'));
    adjustStockDialogVisible.value = false;
    await Promise.all([
      loadProductInfo(),
      loadTransactionHistory()
    ]);
  } catch (error) {
    console.error('Error adjusting stock:', error);
    ElMessage.error(t('Failed_to_adjust_stock'));
  } finally {
    adjusting.value = false;
  }
};

const confirmAddStock = async () => {
  if (!addStockForm.value.quantity || addStockForm.value.quantity <= 0) {
    ElMessage.warning(t('Please_enter_valid_quantity'));
    return;
  }

  adding.value = true;
  try {
    if (!productInfo.value) {
      ElMessage.error(t('Product_info_not_available'));
      return;
    }
    await InventoryService.updateInventoryQuantity(
      productInfo.value.id,
      addStockForm.value.quantity,
      'add'
    );
    
    ElMessage.success(t('Stock_added_successfully'));
    addStockDialogVisible.value = false;
    await Promise.all([
      loadProductInfo(),
      loadTransactionHistory()
    ]);
  } catch (error) {
    console.error('Error adding stock:', error);
    ElMessage.error(t('Failed_to_add_stock'));
  } finally {
    adding.value = false;
  }
};

const refreshData = async () => {
  await Promise.all([
    loadProductInfo(),
    loadTransactionHistory()
  ]);
};

// Lifecycle
onMounted(() => {
  refreshData();
});
</script>

<style scoped>
.el-card {
  border-radius: 12px;
  border: 1px solid #e5e7eb;
}

.el-card:hover {
  border-color: #d1d5db;
}
</style>
