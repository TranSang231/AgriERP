<template>
    <div class="pt-24 p-6 bg-gray-50 min-h-screen">
        <!-- Header -->
        <div class="mb-8">
            <h1 class="text-3xl font-bold text-gray-900">{{ t('E_commerce_dashboard') }}</h1>
            <p class="text-gray-600 mt-2">{{ t('Overview_of_your_ecommerce_business') }}</p>
        </div>

        <!-- Stats Grid -->
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
                        <p class="text-sm font-medium text-gray-600">{{ t('Total_products') }}</p>
                        <p class="text-2xl font-bold text-gray-900">{{ generalStats.total_products || 0 }}</p>
                        <p class="text-xs text-green-600" v-if="generalStats.products_growth">
                            +{{ generalStats.products_growth }}% {{ t('from_last_month') }}
                        </p>
                    </div>
                </div>
            </el-card>

            <!-- Total Orders -->
            <el-card class="hover:shadow-lg transition-shadow">
                <div class="flex items-center">
                    <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
                        <el-icon :size="24" class="text-green-600">
                            <ShoppingCart />
                        </el-icon>
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">{{ t('Total_orders') }}</p>
                        <p class="text-2xl font-bold text-gray-900">{{ generalStats.total_orders || 0 }}</p>
                        <p class="text-xs text-green-600" v-if="generalStats.orders_growth">
                            +{{ generalStats.orders_growth }}% {{ t('from_last_month') }}
                        </p>
                    </div>
                </div>
            </el-card>

            <!-- Total Customers -->
            <el-card class="hover:shadow-lg transition-shadow">
                <div class="flex items-center">
                    <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center">
                        <el-icon :size="24" class="text-purple-600">
                            <User />
                        </el-icon>
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">{{ t('Total_customers') }}</p>
                        <p class="text-2xl font-bold text-gray-900">{{ generalStats.total_customers || 0 }}</p>
                        <p class="text-xs text-green-600" v-if="generalStats.customers_growth">
                            +{{ generalStats.customers_growth }}% {{ t('from_last_month') }}
                        </p>
                    </div>
                </div>
            </el-card>

            <!-- Total Revenue -->
            <el-card class="hover:shadow-lg transition-shadow">
                <div class="flex items-center">
                    <div class="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center">
                        <el-icon :size="24" class="text-yellow-600">
                            <Money />
                        </el-icon>
                    </div>
                    <div class="ml-4">
                        <p class="text-sm font-medium text-gray-600">{{ t('Total_revenue') }}</p>
                        <p class="text-2xl font-bold text-gray-900">{{ formatCurrency(generalStats.total_revenue || 0) }}</p>
                        <p class="text-xs text-green-600" v-if="generalStats.revenue_growth">
                            +{{ generalStats.revenue_growth }}% {{ t('from_last_month') }}
                        </p>
                    </div>
                </div>
            </el-card>
        </div>

        <!-- Charts Row -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            <!-- Sales Chart -->
            <el-card>
                <template #header>
                    <div class="flex justify-between items-center">
                        <h3 class="text-lg font-semibold text-white">{{ t('Sales_overview') }}</h3>
                        <el-select v-model="salesPeriod" @change="loadSalesData" size="small">
                            <el-option :label="t('Last_7_days')" value="7d" />
                            <el-option :label="t('Last_30_days')" value="30d" />
                            <el-option :label="t('Last_3_months')" value="3m" />
                        </el-select>
                    </div>
                </template>
                <div class="h-80">
                    <Line v-if="salesChartData" 
                        :data="salesChartData" 
                        :options="chartOptions" 
                    />
                    <div v-else class="flex items-center justify-center h-full">
                        <el-empty :description="t('No_data_available')" />
                    </div>
                </div>
            </el-card>

            <!-- Order Status Distribution -->
            <el-card>
                <template #header>
                    <h3 class="text-lg font-semibold text-white">{{ t('Order_status_distribution') }}</h3>
                </template>
                <div class="h-80">
                    <Doughnut v-if="orderStatusChartData" 
                        :data="orderStatusChartData" 
                        :options="doughnutOptions" 
                    />
                    <div v-else class="flex items-center justify-center h-full">
                        <el-empty :description="t('No_data_available')" />
                    </div>
                </div>
            </el-card>
        </div>

        <!-- Inventory Alerts -->
        <div class="mb-8">
            <InventoryAlerts ref="inventoryAlertsRef" />
        </div>

        <!-- Recent Orders and Top Products -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- Recent Orders -->
            <el-card>
                <template #header>
                    <div class="flex justify-between items-center">
                        <h3 class="text-lg font-semibold text-white">{{ t('Recent_orders') }}</h3>
                        <el-button type="primary" size="small" @click="$router.push('/e-commerce/orders')">
                            {{ t('View_all') }}
                        </el-button>
                    </div>
                </template>
                <div class="space-y-4">
                    <div v-for="order in recentOrders" :key="order.id" 
                         class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div>
                            <p class="font-medium">#{{ order.id }}</p>
                            <p class="text-sm text-gray-600">{{ order.customer_name }}</p>
                            <p class="text-xs text-gray-500">{{ formatDate(order.created_at) }}</p>
                        </div>
                        <div class="text-right">
                            <p class="font-semibold">{{ formatCurrency(order.total_amount) }}</p>
                            <el-tag :type="getOrderStatusType(order.order_status)" size="small">
                                {{ getOrderStatusText(order.order_status) }}
                            </el-tag>
                        </div>
                    </div>
                    <div v-if="!recentOrders.length" class="text-center py-8">
                        <el-empty :description="t('No_recent_orders')" />
                    </div>
                </div>
            </el-card>

            <!-- Top Products -->
            <el-card>
                <template #header>
                    <div class="flex justify-between items-center">
                        <h3 class="text-lg font-semibold text-white">{{ t('Top_selling_products') }}</h3>
                        <el-button type="primary" size="small" @click="$router.push('/e-commerce/products')">
                            {{ t('View_all') }}
                        </el-button>
                    </div>
                </template>
                <div class="space-y-4">
                    <div v-for="product in topProducts" :key="product.id" 
                         class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div class="flex items-center">
                            <img v-if="product.thumbnail" 
                                 :src="product.thumbnail" 
                                 :alt="product.name" 
                                 class="w-12 h-12 object-cover rounded-lg mr-3">
                            <div v-else class="w-12 h-12 bg-gray-200 rounded-lg mr-3 flex items-center justify-center">
                                <el-icon class="text-gray-400">
                                    <Picture />
                                </el-icon>
                            </div>
                            <div>
                                <p class="font-medium">{{ product.name }}</p>
                                <p class="text-sm text-gray-600">{{ formatCurrency(product.price) }}</p>
                            </div>
                        </div>
                        <div class="text-right">
                            <p class="font-semibold">{{ product.sold_quantity }} {{ t('sold') }}</p>
                            <p class="text-sm text-gray-600">{{ product.in_stock }} {{ t('in_stock') }}</p>
                        </div>
                    </div>
                    <div v-if="!topProducts.length" class="text-center py-8">
                        <el-empty :description="t('No_products_data')" />
                    </div>
                </div>
            </el-card>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useI18n } from 'vue-i18n';
import { 
    Box, 
    ShoppingCart, 
    User, 
    Money, 
    Picture 
} from '@element-plus/icons-vue';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    ArcElement
} from 'chart.js';
import { Line, Doughnut } from 'vue-chartjs';
import EcommerceStatisticService from '@/services/ecommerce/statistic';
import InventoryAlerts from '@/components/ecommerce/InventoryAlerts.vue';

// Register Chart.js components
ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    ArcElement
);

definePageMeta({
    layout: 'ecommerce'
});

const { t } = useI18n();

// Reactive data
const generalStats = ref({
    total_products: 0,
    total_orders: 0,
    total_customers: 0,
    total_revenue: 0,
    products_growth: 0,
    orders_growth: 0,
    customers_growth: 0,
    revenue_growth: 0
});

const salesPeriod = ref('30d');
const salesData = ref([]);
const orderStatusData = ref([]);
const recentOrders = ref([]);
const topProducts = ref([]);
const inventoryAlertsRef = ref(null);

// Chart options
const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            position: 'top' as const,
        },
        title: {
            display: false,
        },
    },
    scales: {
        y: {
            beginAtZero: true,
        },
    },
};

const doughnutOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: {
            position: 'bottom' as const,
        },
    },
};

// Computed properties
const salesChartData = computed(() => {
    if (!salesData.value.length) return null;
    
    return {
        labels: salesData.value.map((item: any) => item.date),
        datasets: [
            {
                label: t('Revenue'),
                data: salesData.value.map((item: any) => item.revenue),
                borderColor: 'rgb(59, 130, 246)',
                backgroundColor: 'rgba(59, 130, 246, 0.1)',
                tension: 0.4,
            },
            {
                label: t('Orders'),
                data: salesData.value.map((item: any) => item.orders),
                borderColor: 'rgb(16, 185, 129)',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                tension: 0.4,
                yAxisID: 'y1',
            }
        ],
    };
});

const orderStatusChartData = computed(() => {
    if (!orderStatusData.value.length) return null;
    
    return {
        labels: orderStatusData.value.map((item: any) => t(item.status)),
        datasets: [
            {
                data: orderStatusData.value.map((item: any) => item.count),
                backgroundColor: [
                    '#3B82F6', // Blue
                    '#10B981', // Green
                    '#F59E0B', // Yellow
                    '#EF4444', // Red
                    '#8B5CF6', // Purple
                ],
            },
        ],
    };
});

// Methods
const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('vi-VN', {
        style: 'currency',
        currency: 'VND'
    }).format(amount);
};

const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('vi-VN');
};

const getOrderStatusType = (status: number) => {
    const statusMap: { [key: number]: string } = {
        1: 'info',    // New
        2: 'warning', // Processing
        3: 'success', // Completed
        4: 'danger',  // Cancelled
    };
    return statusMap[status] || 'info';
};

const getOrderStatusText = (status: number) => {
    const statusMap: { [key: number]: string } = {
        1: t('New'),
        2: t('Processing'),
        3: t('Completed'),
        4: t('Cancelled'),
    };
    return statusMap[status] || t('Unknown');
};

const loadGeneralStats = async () => {
    try {
        const response = await EcommerceStatisticService.getGeneralStats();
        generalStats.value = response;
    } catch (error) {
        console.error('Error loading general stats:', error);
        // Fallback to mock data if API fails
        generalStats.value = {
            total_products: 156,
            total_orders: 1234,
            total_customers: 567,
            total_revenue: 45678900,
            products_growth: 12.5,
            orders_growth: 8.3,
            customers_growth: 15.2,
            revenue_growth: 22.1
        };
    }
};

const loadSalesData = async () => {
    try {
        const response = await EcommerceStatisticService.getSalesData(salesPeriod.value);
        salesData.value = response;
    } catch (error) {
        console.error('Error loading sales data:', error);
        // Fallback to mock data if API fails
        const mockData = [];
        const days = salesPeriod.value === '7d' ? 7 : salesPeriod.value === '30d' ? 30 : 90;
        
        for (let i = days - 1; i >= 0; i--) {
            const date = new Date();
            date.setDate(date.getDate() - i);
            mockData.push({
                date: date.toLocaleDateString('vi-VN'),
                revenue: Math.floor(Math.random() * 5000000) + 1000000,
                orders: Math.floor(Math.random() * 50) + 10
            });
        }
        salesData.value = mockData;
    }
};

const loadOrderStatusData = async () => {
    try {
        const response = await EcommerceStatisticService.getOrderStatusData();
        orderStatusData.value = response;
    } catch (error) {
        console.error('Error loading order status data:', error);
        // Fallback to mock data if API fails
        orderStatusData.value = [
            { status: 'New', count: 45 },
            { status: 'Processing', count: 32 },
            { status: 'Completed', count: 156 },
            { status: 'Cancelled', count: 8 }
        ];
    }
};

const loadRecentOrders = async () => {
    try {
        const response = await EcommerceStatisticService.getRecentOrders();
        console.log('Recent orders response:', response);
        recentOrders.value = response;
    } catch (error) {
        console.error('Error loading recent orders:', error);
        // Fallback to mock data if API fails
        recentOrders.value = [
            {
                id: 'ORD001',
                customer_name: 'Nguyễn Văn A',
                total_amount: 1250000,
                order_status: 1,
                created_at: new Date().toISOString()
            },
            {
                id: 'ORD002',
                customer_name: 'Trần Thị B',
                total_amount: 890000,
                order_status: 2,
                created_at: new Date(Date.now() - 86400000).toISOString()
            },
            {
                id: 'ORD003',
                customer_name: 'Lê Văn C',
                total_amount: 2100000,
                order_status: 3,
                created_at: new Date(Date.now() - 172800000).toISOString()
            }
        ];
    }
};

const loadTopProducts = async () => {
    try {
        const response = await EcommerceStatisticService.getTopProducts();
        console.log('Top products response:', response);
        topProducts.value = response;
    } catch (error) {
        console.error('Error loading top products:', error);
        // Fallback to mock data if API fails
        topProducts.value = [
            {
                id: 1,
                name: 'Phân bón hữu cơ NPK',
                price: 150000,
                sold_quantity: 45,
                in_stock: 120,
                thumbnail: null
            },
            {
                id: 2,
                name: 'Thuốc trừ sâu sinh học',
                price: 85000,
                sold_quantity: 38,
                in_stock: 200,
                thumbnail: null
            },
            {
                id: 3,
                name: 'Giống lúa ST25',
                price: 25000,
                sold_quantity: 156,
                in_stock: 500,
                thumbnail: null
            }
        ];
    }
};

// Lifecycle
onMounted(() => {
    loadGeneralStats();
    loadSalesData();
    loadOrderStatusData();
    loadRecentOrders();
    loadTopProducts();
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