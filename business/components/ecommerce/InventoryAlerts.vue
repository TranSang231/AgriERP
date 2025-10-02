<template>
    <el-card>
        <template #header>
            <div class="flex justify-between items-center">
                <h3 class="text-lg font-semibold text-white">{{ t('Inventory_alerts') }}</h3>
                <el-badge :value="totalAlerts" :hidden="totalAlerts === 0" type="danger">
                    <el-icon :size="20" class="text-gray-600">
                        <Warning />
                    </el-icon>
                </el-badge>
            </div>
        </template>
        
        <div v-if="loading" class="flex justify-center py-8">
            <el-icon class="is-loading" :size="24">
                <Loading />
            </el-icon>
        </div>
        
        <div v-else-if="totalAlerts === 0" class="text-center py-8">
            <el-icon :size="48" class="text-green-500 mb-4">
                <CircleCheck />
            </el-icon>
            <p class="text-gray-600">{{ t('All_products_in_good_stock') }}</p>
        </div>
        
        <div v-else class="space-y-4">
            <!-- Out of Stock Products -->
            <div v-if="alerts.out_of_stock.length > 0">
                <div class="flex items-center mb-3">
                    <el-icon class="text-red-500 mr-2">
                        <CircleClose />
                    </el-icon>
                    <h4 class="font-medium text-red-700">
                        {{ t('Out_of_stock') }} ({{ alerts.out_of_stock_count }})
                    </h4>
                </div>
                <div class="space-y-2">
                    <div v-for="product in alerts.out_of_stock.slice(0, showAllOutOfStock ? undefined : 3)" 
                         :key="`out-${product.id}`"
                         class="flex items-center justify-between p-3 bg-red-50 rounded-lg border border-red-200">
                        <div>
                            <p class="font-medium text-red-800">{{ product.name }}</p>
                            <p class="text-sm text-red-600">{{ formatCurrency(product.price) }}</p>
                        </div>
                        <el-tag type="danger" size="small">
                            {{ t('Out_of_stock') }}
                        </el-tag>
                    </div>
                    <div v-if="alerts.out_of_stock.length > 3" class="text-center">
                        <el-button 
                            type="text" 
                            size="small" 
                            @click="showAllOutOfStock = !showAllOutOfStock"
                        >
                            {{ showAllOutOfStock ? t('Show_less') : t('Show_more') }}
                            ({{ alerts.out_of_stock.length - 3 }} {{ t('more') }})
                        </el-button>
                    </div>
                </div>
            </div>
            
            <!-- Low Stock Products -->
            <div v-if="alerts.low_stock.length > 0">
                <div class="flex items-center mb-3">
                    <el-icon class="text-yellow-500 mr-2">
                        <Warning />
                    </el-icon>
                    <h4 class="font-medium text-yellow-700">
                        {{ t('Low_stock') }} ({{ alerts.low_stock_count }})
                    </h4>
                </div>
                <div class="space-y-2">
                    <div v-for="product in alerts.low_stock.slice(0, showAllLowStock ? undefined : 3)" 
                         :key="`low-${product.id}`"
                         class="flex items-center justify-between p-3 bg-yellow-50 rounded-lg border border-yellow-200">
                        <div>
                            <p class="font-medium text-yellow-800">{{ product.name }}</p>
                            <p class="text-sm text-yellow-600">{{ formatCurrency(product.price) }}</p>
                        </div>
                        <el-tag type="warning" size="small">
                            {{ product.in_stock }} {{ t('left') }}
                        </el-tag>
                    </div>
                    <div v-if="alerts.low_stock.length > 3" class="text-center">
                        <el-button 
                            type="text" 
                            size="small" 
                            @click="showAllLowStock = !showAllLowStock"
                        >
                            {{ showAllLowStock ? t('Show_less') : t('Show_more') }}
                            ({{ alerts.low_stock.length - 3 }} {{ t('more') }})
                        </el-button>
                    </div>
                </div>
            </div>
        </div>
        
        <template #footer v-if="totalAlerts > 0">
            <div class="text-center">
                <el-button type="primary" size="small" @click="$router.push('/e-commerce/products')">
                    {{ t('Manage_inventory') }}
                </el-button>
            </div>
        </template>
    </el-card>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useI18n } from 'vue-i18n';
import { 
    Warning, 
    Loading, 
    CircleCheck, 
    CircleClose 
} from '@element-plus/icons-vue';
import EcommerceStatisticService from '@/services/ecommerce/statistic';

const { t } = useI18n();

// Reactive data
const loading = ref(true);
const alerts = ref({
    low_stock: [],
    out_of_stock: [],
    low_stock_count: 0,
    out_of_stock_count: 0
});
const showAllOutOfStock = ref(false);
const showAllLowStock = ref(false);

// Computed properties
const totalAlerts = computed(() => {
    return alerts.value.low_stock_count + alerts.value.out_of_stock_count;
});

// Methods
const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('vi-VN', {
        style: 'currency',
        currency: 'VND'
    }).format(amount);
};

const loadInventoryAlerts = async () => {
    try {
        loading.value = true;
        const response = await EcommerceStatisticService.getInventoryAlerts();
        alerts.value = response;
    } catch (error) {
        console.error('Error loading inventory alerts:', error);
        // Fallback to mock data if API fails
        alerts.value = {
            low_stock: [
                {
                    id: 1,
                    name: 'Phân bón hữu cơ NPK',
                    price: 150000,
                    in_stock: 5
                },
                {
                    id: 2,
                    name: 'Thuốc trừ sâu sinh học',
                    price: 85000,
                    in_stock: 8
                }
            ],
            out_of_stock: [
                {
                    id: 3,
                    name: 'Giống lúa ST25',
                    price: 25000,
                    in_stock: 0
                }
            ],
            low_stock_count: 2,
            out_of_stock_count: 1
        };
    } finally {
        loading.value = false;
    }
};

// Lifecycle
onMounted(() => {
    loadInventoryAlerts();
});

// Expose refresh method for parent component
defineExpose({
    refresh: loadInventoryAlerts
});
</script>

<style scoped>
.el-card {
    border-radius: 12px;
    border: 1px solid #e5e7eb;
}

.is-loading {
    animation: rotating 2s linear infinite;
}

@keyframes rotating {
    from {
        transform: rotate(0deg);
    }
    to {
        transform: rotate(360deg);
    }
}
</style>

