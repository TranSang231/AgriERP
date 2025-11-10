<template>
  <div class="flex flex-row w-full justify-center pt-20">
    <div class="w-full max-w-7xl">
      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <!-- Total Products -->
        <el-card class="hover:shadow-lg transition-shadow">
          <div class="flex items-center">
            <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
              <el-icon :size="24" class="text-blue-600">
                <Box />
              </el-icon>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">{{ t('Total_Products') }}</p>
              <p class="text-2xl font-bold text-gray-900">{{ inventoryStats.total_products || 0 }}</p>
            </div>
          </div>
        </el-card>

        <!-- Total Stock Value -->
        <el-card class="hover:shadow-lg transition-shadow">
          <div class="flex items-center">
            <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
              <el-icon :size="24" class="text-green-600">
                <Money />
              </el-icon>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">{{ t('Total_Stock_Value') }}</p>
              <p class="text-2xl font-bold text-gray-900">{{ formatCurrency(inventoryStats.total_value || 0) }}</p>
            </div>
          </div>
        </el-card>

        <!-- Low Stock Items -->
        <el-card class="hover:shadow-lg transition-shadow">
          <div class="flex items-center">
            <div class="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center">
              <el-icon :size="24" class="text-yellow-600">
                <Warning />
              </el-icon>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">{{ t('Low_Stock_Items') }}</p>
              <p class="text-2xl font-bold text-gray-900">{{ inventoryStats.low_stock_count || 0 }}</p>
            </div>
          </div>
        </el-card>

        <!-- Out of Stock -->
        <el-card class="hover:shadow-lg transition-shadow">
          <div class="flex items-center">
            <div class="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center">
              <el-icon :size="24" class="text-red-600">
                <Close />
              </el-icon>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">{{ t('Out_of_Stock') }}</p>
              <p class="text-2xl font-bold text-gray-900">{{ inventoryStats.out_of_stock_count || 0 }}</p>
            </div>
          </div>
        </el-card>
      </div>

      <!-- Filters and Actions -->
      <el-card class="mb-6">
        <div class="flex flex-wrap items-center justify-between gap-4">
          <div class="flex flex-wrap items-center gap-4">
            <!-- Search -->
            <el-input
              v-model="searchQuery"
              :placeholder="t('Search_products')"
              clearable
              style="width: 300px"
              @input="handleSearch"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>

            <!-- Category Filter -->
            <el-select
              v-model="selectedCategory"
              :placeholder="t('All_Categories')"
              clearable
              style="width: 200px"
              @change="handleFilterChange"
            >
              <el-option
                v-for="category in categories"
                :key="category.id"
                :label="category.name?.origin || category.name"
                :value="category.id"
              />
            </el-select>

            <!-- Stock Status Filter -->
            <el-select
              v-model="stockStatusFilter"
              :placeholder="t('All_Stock_Status')"
              clearable
              style="width: 200px"
              @change="handleFilterChange"
            >
              <el-option 
                :label="inventoryStats.config?.in_stock_label || t('In_Stock')" 
                value="in_stock" 
              />
              <el-option 
                :label="inventoryStats.config?.low_stock_label || t('Low_Stock')" 
                value="low_stock" 
              />
              <el-option 
                :label="inventoryStats.config?.out_of_stock_label || t('Out_of_Stock')" 
                value="out_of_stock" 
              />
            </el-select>
          </div>

          <div class="flex items-center gap-2">
            <el-button @click="showConfigDialog">
              <el-icon><Setting /></el-icon>
              {{ t('Settings') }}
            </el-button>
            <el-button type="primary" @click="refreshData">
              <el-icon><Refresh /></el-icon>
              {{ t('Refresh') }}
            </el-button>
            <el-button type="success" @click="exportToExcel">
              <el-icon><Download /></el-icon>
              {{ t('Export_Excel') }}
            </el-button>
          </div>
        </div>
      </el-card>

      <!-- Inventory Table -->
      <el-card>
        <template #header>
          <div class="flex justify-between items-center">
            <h3 class="text-lg font-semibold text-white">{{ t('Inventory_List') }}</h3>
            <div class="flex items-center gap-2">
              <el-button size="small" @click="showLowStockOnly = !showLowStockOnly">
                <el-icon><Warning /></el-icon>
                {{ showLowStockOnly ? t('Show_All') : t('Show_Low_Stock_Only') }}
              </el-button>
            </div>
          </div>
        </template>

        <el-table
          :data="filteredInventory"
          v-loading="loading"
          stripe
          style="width: 100%"
          @row-click="handleRowClick"
          class="cursor-pointer"
        >
          <el-table-column prop="thumbnail" :label="t('Image')" width="80">
            <template #default="scope">
              <el-image
                v-if="scope.row.product?.thumbnail"
                :src="getImageUrl(scope.row.product.thumbnail)"
                fit="cover"
                style="width: 50px; height: 50px"
                class="rounded"
              />
              <div v-else class="w-12 h-12 bg-gray-200 rounded flex items-center justify-center">
                <el-icon class="text-gray-400"><Picture /></el-icon>
              </div>
            </template>
          </el-table-column>

          <el-table-column prop="product.name" :label="t('Product_Name')" min-width="200">
            <template #default="scope">
              <div>
                <p class="font-medium">{{ scope.row.product?.name?.origin || scope.row.product?.name }}</p>
                <p class="text-sm text-gray-500">{{ scope.row.product?.sku || '-' }}</p>
              </div>
            </template>
          </el-table-column>

          <el-table-column prop="product.unit" :label="t('Unit')" width="100">
            <template #default="scope">
              {{ scope.row.product?.unit?.origin || scope.row.product?.unit || '-' }}
            </template>
          </el-table-column>

          <el-table-column prop="current_quantity" :label="t('Current_Stock')" width="120" sortable>
            <template #default="scope">
              <div class="text-center">
                <span 
                  class="font-bold"
                  :class="getStockStatusClass(scope.row.current_quantity, scope.row.min_quantity)"
                >
                  {{ scope.row.current_quantity || 0 }}
                </span>
              </div>
            </template>
          </el-table-column>

          <el-table-column prop="min_quantity" :label="t('Min_Stock')" width="100">
            <template #default="scope">
              {{ scope.row.min_quantity || 0 }}
            </template>
          </el-table-column>

          <el-table-column prop="max_quantity" :label="t('Max_Stock')" width="100">
            <template #default="scope">
              {{ scope.row.max_quantity || '-' }}
            </template>
          </el-table-column>

          <el-table-column prop="product.price" :label="t('Unit_Price')" width="120">
            <template #default="scope">
              {{ formatCurrency(scope.row.product?.price || 0) }}
            </template>
          </el-table-column>

          <el-table-column :label="t('Stock_Value')" width="120">
            <template #default="scope">
              {{ formatCurrency((scope.row.product?.price || 0) * (scope.row.current_quantity || 0)) }}
            </template>
          </el-table-column>

          <el-table-column :label="t('Status')" width="120">
            <template #default="scope">
              <el-tag :type="getStockStatusType(scope.row.current_quantity, scope.row.min_quantity)">
                {{ getStockStatusText(scope.row.current_quantity, scope.row.min_quantity) }}
              </el-tag>
            </template>
          </el-table-column>

          <el-table-column prop="last_updated" :label="t('Last_Updated')" width="150">
            <template #default="scope">
              {{ formatDateTime(scope.row.updated_at) }}
            </template>
          </el-table-column>

          <el-table-column :label="t('Actions')" width="200" fixed="right">
            <template #default="scope">
              <div class="flex gap-2">
                <el-button size="small" type="primary" @click.stop="viewDetails(scope.row)">
                  <el-icon><View /></el-icon>
                </el-button>
                <el-button size="small" type="success" @click.stop="adjustStock(scope.row)">
                  <el-icon><Edit /></el-icon>
                </el-button>
                <el-button size="small" type="warning" @click.stop="editThresholds(scope.row)">
                  <el-icon><Setting /></el-icon>
                </el-button>
              </div>
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
            <el-input :value="adjustForm.productName" disabled />
          </el-form-item>
          <el-form-item :label="t('Current_Stock')">
            <el-input :value="adjustForm.currentQuantity" disabled />
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
              :max="adjustForm.type === 'add' ? 999999 : adjustForm.currentQuantity"
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

      <!-- Edit Thresholds Dialog -->
      <el-dialog
        v-model="editThresholdsDialogVisible"
        :title="t('Edit_Stock_Thresholds')"
        width="500px"
      >
        <el-form :model="thresholdsForm" label-width="150px">
          <el-form-item :label="t('Product')">
            <el-input :value="thresholdsForm.productName" disabled />
          </el-form-item>
          <el-form-item :label="t('Current_Stock')">
            <el-input :value="thresholdsForm.currentQuantity" disabled />
          </el-form-item>
          <el-form-item :label="t('Minimum_Stock')" required>
            <el-input-number
              v-model="thresholdsForm.min_quantity"
              :min="0"
              :precision="2"
              style="width: 100%"
            />
            <span class="text-xs text-gray-500 mt-1 block">
              Alert when stock falls below this level
            </span>
          </el-form-item>
          <el-form-item :label="t('Maximum_Stock')">
            <el-input-number
              v-model="thresholdsForm.max_quantity"
              :min="thresholdsForm.min_quantity || 0"
              :precision="2"
              style="width: 100%"
            />
            <span class="text-xs text-gray-500 mt-1 block">
              Target maximum stock level (optional)
            </span>
          </el-form-item>
        </el-form>
        <template #footer>
          <el-button @click="editThresholdsDialogVisible = false">{{ t('Cancel') }}</el-button>
          <el-button type="primary" @click="confirmEditThresholds" :loading="updatingThresholds">
            {{ t('Save') }}
          </el-button>
        </template>
      </el-dialog>

      <!-- Configuration Dialog -->
      <el-dialog
        v-model="configDialogVisible"
        title="Inventory Configuration"
        width="700px"
      >
        <el-form :model="configForm" label-width="200px" v-loading="loadingConfig">
          <el-divider content-position="left">Stock Thresholds</el-divider>
          
          <el-form-item label="Low Stock Threshold Type">
            <el-select v-model="configForm.low_stock_threshold_type" style="width: 100%">
              <el-option label="Use Min Quantity" value="min_quantity" />
              <el-option label="Percentage of Max" value="percentage" />
              <el-option label="Fixed Value" value="fixed" />
            </el-select>
            <span class="text-xs text-gray-500 mt-1 block">
              How to determine when stock is low
            </span>
          </el-form-item>

          <el-form-item 
            label="Low Stock Threshold Value"
            v-if="configForm.low_stock_threshold_type !== 'min_quantity'"
          >
            <el-input-number
              v-model="configForm.low_stock_threshold_value"
              :min="0"
              :precision="2"
              style="width: 100%"
            />
            <span class="text-xs text-gray-500 mt-1 block">
              {{ configForm.low_stock_threshold_type === 'percentage' ? 'Percentage (e.g., 20 for 20%)' : 'Fixed quantity for all products' }}
            </span>
          </el-form-item>

          <el-form-item label="Out of Stock Threshold">
            <el-input-number
              v-model="configForm.out_of_stock_threshold"
              :min="-999"
              :precision="2"
              style="width: 100%"
            />
            <span class="text-xs text-gray-500 mt-1 block">
              Below this value is considered out of stock (usually 0)
            </span>
          </el-form-item>

          <el-divider content-position="left">Display Labels</el-divider>

          <el-form-item label="In Stock Label">
            <el-input v-model="configForm.in_stock_label" placeholder="In Stock" />
          </el-form-item>

          <el-form-item label="Low Stock Label">
            <el-input v-model="configForm.low_stock_label" placeholder="Low Stock" />
          </el-form-item>

          <el-form-item label="Out of Stock Label">
            <el-input v-model="configForm.out_of_stock_label" placeholder="Out of Stock" />
          </el-form-item>

          <el-divider content-position="left">Stock Movement Settings</el-divider>

          <el-form-item label="Allow Negative Stock">
            <el-switch v-model="configForm.allow_negative_stock" />
            <span class="text-xs text-gray-500 ml-2">
              Enable backorders (allow stock below zero)
            </span>
          </el-form-item>

          <el-form-item label="Require Reason">
            <el-switch v-model="configForm.require_transaction_reason" />
            <span class="text-xs text-gray-500 ml-2">
              Require reason for manual adjustments
            </span>
          </el-form-item>

          <el-form-item label="Require Reference">
            <el-switch v-model="configForm.require_transaction_reference" />
            <span class="text-xs text-gray-500 ml-2">
              Require reference number for adjustments
            </span>
          </el-form-item>

          <el-divider content-position="left">Auto Reorder Settings</el-divider>

          <el-form-item label="Enable Auto Reorder">
            <el-switch v-model="configForm.enable_auto_reorder" />
            <span class="text-xs text-gray-500 ml-2">
              Automatically create purchase orders when stock is low
            </span>
          </el-form-item>

          <el-form-item 
            label="Reorder Quantity Type"
            v-if="configForm.enable_auto_reorder"
          >
            <el-select v-model="configForm.auto_reorder_quantity_type" style="width: 100%">
              <el-option label="Fill to Max Quantity" value="max_quantity" />
              <el-option label="Fixed Reorder Quantity" value="fixed" />
              <el-option label="Multiple of Min Quantity" value="multiple" />
            </el-select>
          </el-form-item>

          <el-form-item 
            label="Reorder Quantity Value"
            v-if="configForm.enable_auto_reorder && configForm.auto_reorder_quantity_type !== 'max_quantity'"
          >
            <el-input-number
              v-model="configForm.auto_reorder_quantity_value"
              :min="0"
              :precision="2"
              style="width: 100%"
            />
          </el-form-item>

          <el-divider content-position="left">Reservation Settings</el-divider>

          <el-form-item label="Auto Reserve on Order">
            <el-switch v-model="configForm.auto_reserve_on_order" />
            <span class="text-xs text-gray-500 ml-2">
              Automatically reserve stock when order is placed
            </span>
          </el-form-item>

          <el-form-item label="Reservation Expiry (hours)">
            <el-input-number
              v-model="configForm.reservation_expiry_hours"
              :min="1"
              :max="168"
              style="width: 100%"
            />
            <span class="text-xs text-gray-500 mt-1 block">
              Hours before unreleased reservations expire
            </span>
          </el-form-item>
        </el-form>

        <template #footer>
          <el-button @click="configDialogVisible = false">Cancel</el-button>
          <el-button @click="resetConfigToDefault" :loading="savingConfig">Reset to Default</el-button>
          <el-button type="primary" @click="saveConfig" :loading="savingConfig">
            Save Configuration
          </el-button>
        </template>
      </el-dialog>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { useRouter } from 'vue-router';
import {
  Box,
  Money,
  Warning,
  Close,
  Search,
  Refresh,
  Download,
  Picture,
  View,
  Edit,
  Setting
} from '@element-plus/icons-vue';
import InventoryService from '@/services/e-commerce/inventory';
import ProductCategoryService from '@/services/e-commerce/category';
import { useProductCategoriesStore } from '@/stores/e-commerce/categories';
import { formatDateTime } from '~/utils/time';
import { ElMessage } from 'element-plus';

definePageMeta({
  layout: 'ecommerce'
});

const { t } = useI18n();
const router = useRouter();

// Reactive data
const loading = ref(false);
const inventoryData = ref([]);
const categories = ref([]);
const inventoryStats = ref({
  total_products: 0,
  total_value: 0,
  low_stock_count: 0,
  out_of_stock_count: 0,
  config: {
    out_of_stock_threshold: 0,
    low_stock_threshold_type: 'min_quantity',
    in_stock_label: 'In Stock',
    low_stock_label: 'Low Stock',
    out_of_stock_label: 'Out of Stock'
  }
});

// Filters
const searchQuery = ref('');
const selectedCategory = ref('');
const stockStatusFilter = ref('');
const showLowStockOnly = ref(false);

// Pagination
const currentPage = ref(1);
const pageSize = ref(20);
const totalItems = ref(0);

// Adjust Stock Dialog
const adjustStockDialogVisible = ref(false);
const adjusting = ref(false);
const adjustForm = ref({
  productId: null,
  productName: '',
  currentQuantity: 0,
  type: 'add',
  quantity: 0,
  reason: ''
});

// Edit Thresholds Dialog
const editThresholdsDialogVisible = ref(false);
const updatingThresholds = ref(false);
const thresholdsForm = ref({
  inventoryId: null,
  productName: '',
  currentQuantity: 0,
  min_quantity: 0,
  max_quantity: null
});

// Configuration Dialog
const configDialogVisible = ref(false);
const loadingConfig = ref(false);
const savingConfig = ref(false);
const configForm = ref({
  low_stock_threshold_type: 'min_quantity',
  low_stock_threshold_value: 0,
  out_of_stock_threshold: 0,
  enable_auto_reorder: false,
  auto_reorder_quantity_type: 'max_quantity',
  auto_reorder_quantity_value: 0,
  allow_negative_stock: false,
  require_transaction_reason: false,
  require_transaction_reference: false,
  in_stock_label: 'In Stock',
  low_stock_label: 'Low Stock',
  out_of_stock_label: 'Out of Stock',
  auto_reserve_on_order: true,
  reservation_expiry_hours: 24,
  enable_multi_warehouse: false
});

// Computed properties
const filteredInventory = computed(() => {
  let filtered = inventoryData.value;

  // Search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(item => 
      item.product?.name?.origin?.toLowerCase().includes(query) ||
      item.product?.name?.toLowerCase().includes(query) ||
      item.product?.sku?.toLowerCase().includes(query)
    );
  }

  // Category filter
  if (selectedCategory.value) {
    filtered = filtered.filter(item => 
      item.product?.categories?.some(cat => cat.id === selectedCategory.value)
    );
  }

  // Stock status filter
  if (stockStatusFilter.value) {
    filtered = filtered.filter(item => {
      const current = item.current_quantity || 0;
      const min = item.min_quantity || 0;
      const threshold = inventoryStats.value.config?.out_of_stock_threshold || 0;
      
      switch (stockStatusFilter.value) {
        case 'in_stock':
          return current > min;
        case 'low_stock':
          return current > threshold && current <= min;
        case 'out_of_stock':
          return current <= threshold;
        default:
          return true;
      }
    });
  }

  // Low stock only filter
  if (showLowStockOnly.value) {
    filtered = filtered.filter(item => {
      const current = item.current_quantity || 0;
      const min = item.min_quantity || 0;
      const threshold = inventoryStats.value.config?.out_of_stock_threshold || 0;
      return current > threshold && current <= min;
    });
  }

  return filtered;
});

// Methods
const formatCurrency = (amount) => {
  return new Intl.NumberFormat('vi-VN', {
    style: 'currency',
    currency: 'VND'
  }).format(amount);
};

const getImageUrl = (thumbnail) => {
  if (!thumbnail) return null;
  
  if (thumbnail.startsWith('http://') || thumbnail.startsWith('https://')) {
    return thumbnail;
  }
  
  const runtimeConfig = useRuntimeConfig();
  const baseUrl = runtimeConfig.public.defaultHost;
  return `${baseUrl}${thumbnail.startsWith('/') ? '' : '/'}${thumbnail}`;
};

const getStockStatusClass = (current, min) => {
  const threshold = inventoryStats.value.config?.out_of_stock_threshold || 0;
  
  if (current <= threshold) return 'text-red-600';
  if (current <= min) return 'text-yellow-600';
  return 'text-green-600';
};

const getStockStatusType = (current, min) => {
  const threshold = inventoryStats.value.config?.out_of_stock_threshold || 0;
  
  if (current <= threshold) return 'danger';
  if (current <= min) return 'warning';
  return 'success';
};

const getStockStatusText = (current, min) => {
  const config = inventoryStats.value.config;
  const threshold = config.out_of_stock_threshold || 0;
  
  if (current <= threshold) return config.out_of_stock_label || t('Out_of_Stock');
  if (current <= min) return config.low_stock_label || t('Low_Stock');
  return config.in_stock_label || t('In_Stock');
};

const loadInventoryData = async () => {
  loading.value = true;
  try {
    const params = {
      page: currentPage.value,
      limit: pageSize.value,
      search: searchQuery.value,
      stock_status: stockStatusFilter.value
    };
    if (selectedCategory.value) {
      params.category_id = selectedCategory.value;
    }
    
    const response = await InventoryService.getInventoryItems(params);
    // Handle both paginated and non-paginated responses
    if (response.results) {
      inventoryData.value = response.results;
      totalItems.value = response.count || response.results.length;
    } else if (Array.isArray(response)) {
      inventoryData.value = response;
      totalItems.value = response.length;
    } else {
      inventoryData.value = response.data || [];
      totalItems.value = response.total || 0;
    }
  } catch (error) {
    console.error('Error loading inventory data:', error);
    ElMessage.error(t('Failed_to_load_inventory_data'));
    // Fallback to mock data
    inventoryData.value = generateMockData();
    totalItems.value = inventoryData.value.length;
  } finally {
    loading.value = false;
  }
};

const loadCategories = async () => {
  try {
    const store = useProductCategoriesStore();
    await ProductCategoryService.fetch();
    categories.value = store.allCategories || [];
  } catch (error) {
    console.error('Error loading categories:', error);
  }
};

const loadInventoryStats = async () => {
  try {
    console.log('Loading inventory stats...');
    const stats = await InventoryService.getInventoryStats();
    console.log('Received stats:', stats);
    inventoryStats.value = {
      total_products: stats.total_products || 0,
      total_value: stats.total_value || 0,
      low_stock_count: stats.low_stock_count || 0,
      out_of_stock_count: stats.out_of_stock_count || 0,
      config: stats.config || inventoryStats.value.config
    };
  } catch (error) {
    console.error('Error loading inventory stats:', error);
    console.log('Current inventoryData.value:', inventoryData.value);
    // Fallback: calculate from loaded data if available
    const dataArray = Array.isArray(inventoryData.value) && inventoryData.value.length > 0 
      ? inventoryData.value 
      : [];
    
    console.log('Fallback dataArray length:', dataArray.length);
    
    if (dataArray.length > 0) {
      const threshold = inventoryStats.value.config?.out_of_stock_threshold || 0;
      const calculatedStats = {
        total_products: dataArray.length,
        total_value: dataArray.reduce((sum, item) => 
          sum + ((item.product?.price || 0) * (item.current_quantity || 0)), 0),
        low_stock_count: dataArray.filter(item => 
          (item.current_quantity || 0) > threshold && 
          (item.current_quantity || 0) <= (item.min_quantity || 0)).length,
        out_of_stock_count: dataArray.filter(item => 
          (item.current_quantity || 0) <= threshold).length,
        config: inventoryStats.value.config
      };
      console.log('Calculated fallback stats:', calculatedStats);
      inventoryStats.value = calculatedStats;
    } else {
      // No data at all - keep zeros but preserve config
      console.log('No data available, setting stats to zero');
      inventoryStats.value = {
        total_products: 0,
        total_value: 0,
        low_stock_count: 0,
        out_of_stock_count: 0,
        config: inventoryStats.value.config
      };
    }
  }
};

const generateMockData = () => {
  return [
    {
      id: 1,
      product: {
        id: 1,
        name: { origin: 'iPhone 15 Pro' },
        sku: 'IPH15P-001',
        thumbnail: '/images/products/iphone15.jpg',
        price: 29990000,
        unit: { origin: 'Cái' },
        categories: [{ id: 1, name: 'Điện thoại' }]
      },
      current_quantity: 15,
      min_quantity: 10,
      max_quantity: 100,
      updated_at: '2024-01-15T10:30:00Z'
    },
    {
      id: 2,
      product: {
        id: 2,
        name: { origin: 'Samsung Galaxy S24' },
        sku: 'SGS24-001',
        thumbnail: '/images/products/galaxy-s24.jpg',
        price: 24990000,
        unit: { origin: 'Cái' },
        categories: [{ id: 1, name: 'Điện thoại' }]
      },
      current_quantity: 5,
      min_quantity: 10,
      max_quantity: 80,
      updated_at: '2024-01-14T15:20:00Z'
    },
    {
      id: 3,
      product: {
        id: 3,
        name: { origin: 'MacBook Pro M3' },
        sku: 'MBP-M3-001',
        thumbnail: '/images/products/macbook-pro.jpg',
        price: 45990000,
        unit: { origin: 'Cái' },
        categories: [{ id: 2, name: 'Laptop' }]
      },
      current_quantity: 0,
      min_quantity: 5,
      max_quantity: 50,
      updated_at: '2024-01-13T09:15:00Z'
    },
    {
      id: 4,
      product: {
        id: 4,
        name: { origin: 'iPad Air 5' },
        sku: 'IPA5-001',
        thumbnail: '/images/products/ipad-air.jpg',
        price: 18990000,
        unit: { origin: 'Cái' },
        categories: [{ id: 3, name: 'Tablet' }]
      },
      current_quantity: 25,
      min_quantity: 8,
      max_quantity: 60,
      updated_at: '2024-01-16T08:45:00Z'
    },
    {
      id: 5,
      product: {
        id: 5,
        name: { origin: 'AirPods Pro 2' },
        sku: 'APP2-001',
        thumbnail: '/images/products/airpods-pro.jpg',
        price: 5990000,
        unit: { origin: 'Cái' },
        categories: [{ id: 4, name: 'Phụ kiện' }]
      },
      current_quantity: 3,
      min_quantity: 5,
      max_quantity: 30,
      updated_at: '2024-01-12T14:20:00Z'
    }
  ];
};

const handleSearch = () => {
  currentPage.value = 1;
  loadInventoryData();
};

const handleFilterChange = () => {
  currentPage.value = 1;
  loadInventoryData();
};

const handleSizeChange = (size) => {
  pageSize.value = size;
  currentPage.value = 1;
  loadInventoryData();
};

const handleCurrentChange = (page) => {
  currentPage.value = page;
  loadInventoryData();
};

const handleRowClick = (row) => {
  viewDetails(row);
};

const viewDetails = (item) => {
  router.push(`/e-commerce/inventory/${item.id}`);
};

const adjustStock = (item) => {
  adjustForm.value = {
    productId: item.id,
    productName: item.product?.name?.origin || item.product?.name,
    currentQuantity: item.current_quantity || 0,
    type: 'add',
    quantity: 0,
    reason: ''
  };
  adjustStockDialogVisible.value = true;
};

const editThresholds = (item) => {
  thresholdsForm.value = {
    inventoryId: item.id,
    productName: item.product?.name?.origin || item.product?.name,
    currentQuantity: item.current_quantity || 0,
    min_quantity: item.min_quantity || 0,
    max_quantity: item.max_quantity || null
  };
  editThresholdsDialogVisible.value = true;
};

const confirmEditThresholds = async () => {
  if (thresholdsForm.value.min_quantity < 0) {
    ElMessage.warning(t('Minimum_stock_cannot_be_negative'));
    return;
  }

  if (thresholdsForm.value.max_quantity !== null && 
      thresholdsForm.value.max_quantity < thresholdsForm.value.min_quantity) {
    ElMessage.warning(t('Maximum_stock_must_be_greater_than_minimum'));
    return;
  }

  updatingThresholds.value = true;
  try {
    await InventoryService.updateInventory(
      thresholdsForm.value.inventoryId,
      {
        min_quantity: thresholdsForm.value.min_quantity,
        max_quantity: thresholdsForm.value.max_quantity
      }
    );
    
    ElMessage.success(t('Stock_thresholds_updated_successfully'));
    editThresholdsDialogVisible.value = false;
    await loadInventoryData();
    await loadInventoryStats();
  } catch (error) {
    console.error('Error updating thresholds:', error);
    ElMessage.error(t('Failed_to_update_thresholds'));
  } finally {
    updatingThresholds.value = false;
  }
};

const confirmAdjustStock = async () => {
  if (!adjustForm.value.quantity || adjustForm.value.quantity <= 0) {
    ElMessage.warning(t('Please_enter_valid_quantity'));
    return;
  }

  adjusting.value = true;
  try {
    await InventoryService.updateInventoryQuantity(
      adjustForm.value.productId,
      adjustForm.value.quantity,
      adjustForm.value.type
    );
    
    ElMessage.success(t('Stock_adjusted_successfully'));
    adjustStockDialogVisible.value = false;
    await loadInventoryData();
    await loadInventoryStats();
  } catch (error) {
    console.error('Error adjusting stock:', error);
    ElMessage.error(t('Failed_to_adjust_stock'));
  } finally {
    adjusting.value = false;
  }
};

const refreshData = async () => {
  // Load inventory data first, then stats and categories
  await loadInventoryData();
  await Promise.all([
    loadCategories(),
    loadInventoryStats()
  ]);
};

const exportToExcel = () => {
  ElMessage.info(t('Export_feature_coming_soon'));
};

const showConfigDialog = async () => {
  configDialogVisible.value = true;
  await loadConfig();
};

const loadConfig = async () => {
  loadingConfig.value = true;
  try {
    const config = await InventoryService.getInventoryConfig();
    configForm.value = {
      low_stock_threshold_type: config.low_stock_threshold_type,
      low_stock_threshold_value: config.low_stock_threshold_value,
      out_of_stock_threshold: config.out_of_stock_threshold,
      enable_auto_reorder: config.enable_auto_reorder,
      auto_reorder_quantity_type: config.auto_reorder_quantity_type,
      auto_reorder_quantity_value: config.auto_reorder_quantity_value,
      allow_negative_stock: config.allow_negative_stock,
      require_transaction_reason: config.require_transaction_reason,
      require_transaction_reference: config.require_transaction_reference,
      in_stock_label: config.in_stock_label,
      low_stock_label: config.low_stock_label,
      out_of_stock_label: config.out_of_stock_label,
      auto_reserve_on_order: config.auto_reserve_on_order,
      reservation_expiry_hours: config.reservation_expiry_hours,
      enable_multi_warehouse: config.enable_multi_warehouse
    };
  } catch (error) {
    console.error('Error loading config:', error);
    ElMessage.error('Failed to load configuration');
  } finally {
    loadingConfig.value = false;
  }
};

const saveConfig = async () => {
  savingConfig.value = true;
  try {
    await InventoryService.updateInventoryConfig(configForm.value);
    ElMessage.success('Configuration saved successfully');
    configDialogVisible.value = false;
    // Reload stats to reflect new configuration
    await loadInventoryStats();
  } catch (error) {
    console.error('Error saving config:', error);
    ElMessage.error('Failed to save configuration');
  } finally {
    savingConfig.value = false;
  }
};

const resetConfigToDefault = async () => {
  savingConfig.value = true;
  try {
    const defaultConfig = {
      low_stock_threshold_type: 'min_quantity',
      low_stock_threshold_value: 0,
      out_of_stock_threshold: 0,
      enable_auto_reorder: false,
      auto_reorder_quantity_type: 'max_quantity',
      auto_reorder_quantity_value: 0,
      allow_negative_stock: false,
      require_transaction_reason: false,
      require_transaction_reference: false,
      in_stock_label: 'In Stock',
      low_stock_label: 'Low Stock',
      out_of_stock_label: 'Out of Stock',
      auto_reserve_on_order: true,
      reservation_expiry_hours: 24,
      enable_multi_warehouse: false
    };
    
    await InventoryService.updateInventoryConfig(defaultConfig);
    configForm.value = { ...defaultConfig };
    ElMessage.success('Configuration reset to default');
    await loadInventoryStats();
  } catch (error) {
    console.error('Error resetting config:', error);
    ElMessage.error('Failed to reset configuration');
  } finally {
    savingConfig.value = false;
  }
};

// Watch for filter changes
watch(showLowStockOnly, () => {
  // This is handled by computed property
});

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

.cursor-pointer {
  cursor: pointer;
}
</style>
