<!-- D:\nam5ky1\ERP\AgriERP\shop\pages\orders.vue -->
<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { useI18n } from 'vue-i18n';
import { useCurrency } from '~/composables/useCurrency';
import { useOrderService } from '~/services/orders';
import { useAuthStore } from '~/stores/auth';

const { format } = useCurrency();
const { getOrders } = useOrderService();
const auth = useAuthStore();
// THAY ĐỔI: Lấy thêm locale để dùng cho hàm formatDate
const { t, locale } = useI18n(); 

const orders = ref([]);
const loading = ref(true);
const error = ref('');

useHead({
  title: t('orders.meta.title'),
  meta: [{ name: 'description', content: t('orders.meta.description') }]
});

// THAY ĐỔI: Tối ưu hóa bằng cách tạo một hàm fetch riêng
const fetchOrders = async () => {
  try {
    loading.value = true;
    error.value = ''; // Reset lỗi mỗi lần fetch
    if (!auth.isAuthenticated) {
      orders.value = [];
      return;
    }
    const customerId = (auth.user as any)?.id;
    const { data, error: ordersError } = await getOrders(customerId ? { customer_id: customerId } : { customer_id: 'me' });
    
    if (ordersError?.value) {
      throw ordersError.value;
    }
    
    orders.value = data?.value || [];
  } catch (e: any) {
    console.error('Lỗi khi tải danh sách đơn hàng:', e);
    error.value = e?.message || t('orders.error.loadFailed');
  } finally {
    loading.value = false;
  }
};

onMounted(fetchOrders);

// Refetch when auth changes (login/logout)
watch(
  () => auth.isAuthenticated,
  (isAuthed) => {
    if (isAuthed) {
      fetchOrders();
    } else {
      // Clear data on logout without showing error
      orders.value = [];
      error.value = '';
      loading.value = false;
    }
  }
);

const getPaymentMethodText = (method: number) => {
  return method === 0 ? t('orders.paymentMethods.bank_transfer') : t('orders.paymentMethods.cod');
};


// --- THAY ĐỔI QUAN TRỌNG: Sử dụng key 'order.*' cho các trạng thái dùng chung ---

const getOrderStatusText = (status: number) => {
  const statusMap = {
    0: t('order.statuses.new'), // THAY ĐỔI: từ 'orders' -> 'order'
    1: t('order.statuses.confirmed'), 
    2: t('order.statuses.packing'),
    3: t('order.statuses.shipped'),
    4: t('order.statuses.completed'),
    5: t('order.statuses.canceled')
  };
  return statusMap[status] || t('orders.unknownStatus');
};

const getOrderStatusColor = (status: number) => {
  const colorMap = {
    0: 'bg-blue-100 text-blue-800', 1: 'bg-green-100 text-green-800', 2: 'bg-yellow-100 text-yellow-800',
    3: 'bg-purple-100 text-purple-800', 4: 'bg-green-100 text-green-800', 5: 'bg-red-100 text-red-800'
  };
  return colorMap[status] || 'bg-gray-100 text-gray-800';
};

const getPaymentStatusText = (status: number) => {
  const statusMap = {
    0: t('order.paymentStatuses.init'), // THAY ĐỔI: từ 'orders' -> 'order'
    1: t('order.paymentStatuses.pending'), 2: t('order.paymentStatuses.authorized'),
    3: t('order.paymentStatuses.captured'), 4: t('order.paymentStatuses.completed'), 5: t('order.paymentStatuses.rejected'),
    6: t('order.paymentStatuses.error'), 7: t('order.paymentStatuses.canceled'), 8: t('order.paymentStatuses.paid')
  };
  return statusMap[status] || t('orders.unknownStatus');
};

const getPaymentStatusColor = (status: number) => {
  const colorMap = {
    0: 'bg-blue-100 text-blue-800', 1: 'bg-yellow-100 text-yellow-800', 2: 'bg-purple-100 text-purple-800',
    3: 'bg-green-100 text-green-800', 4: 'bg-green-100 text-green-800', 5: 'bg-red-100 text-red-800',
    6: 'bg-red-100 text-red-800', 7: 'bg-gray-100 text-gray-800', 8: 'bg-green-100 text-green-800'
  };
  return colorMap[status] || 'bg-gray-100 text-gray-800';
};

const getShippingStatusText = (status: number) => {
  const statusMap = {
    0: t('order.shippingStatuses.placed'), // THAY ĐỔI: từ 'orders' -> 'order'
    1: t('order.shippingStatuses.packing'), 2: t('order.shippingStatuses.delivering'),
    3: t('order.shippingStatuses.delivered'), 4: t('order.shippingStatuses.returnRequested'),
    5: t('order.shippingStatuses.returning'), 6: t('order.shippingStatuses.returned')
  };
  return statusMap[status] || t('orders.unknownStatus');
};

const getShippingStatusColor = (status: number) => {
  const colorMap = {
    0: 'bg-blue-100 text-blue-800', 1: 'bg-yellow-100 text-yellow-800', 2: 'bg-purple-100 text-purple-800',
    3: 'bg-green-100 text-green-800', 4: 'bg-orange-100 text-orange-800', 5: 'bg-red-100 text-red-800',
    6: 'bg-gray-100 text-gray-800'
  };
  return colorMap[status] || 'bg-gray-100 text-gray-800';
};

const formatDate = (dateString: string) => {
  // THAY ĐỔI: Dùng biến 'locale' đã lấy ở trên
  const lang = locale.value === 'vi' ? 'vi-VN' : 'en-US';
  return new Date(dateString).toLocaleDateString(lang, {
    year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit'
  });
};

const calculateOrderTotal = (order: any) => {
  const subtotal = order.items.reduce((sum: number, item: any) => sum + item.amount, 0);
  const vatRate = (order.vat_rate || 0) / 100;
  const tax = subtotal * vatRate;
  const shippingFee = order.shipping_fee || 0;
  return subtotal + tax + shippingFee;
};
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">{{ $t('orders.title') }}</h1>
      <p class="text-gray-600">{{ $t('orders.subtitle') }}</p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500 mx-auto"></div>
      <p class="mt-4 text-gray-600">{{ $t('orders.loading') }}</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-12">
      <div class="text-red-500 text-6xl mb-4">⚠️</div>
      <h2 class="text-2xl font-bold text-gray-900 mb-2">{{ $t('orders.error.title') }}</h2>
      <p class="text-gray-600 mb-6">{{ error }}</p>
      <button @click="fetchOrders" class="bg-orange-500 hover:bg-orange-600 text-white px-6 py-3 rounded-lg">
        {{ $t('orders.error.retryButton') }}
      </button>
    </div>

    <!-- Empty State -->
    <div v-else-if="orders.length === 0" class="text-center py-12">
      <div class="text-gray-400 text-6xl mb-4">📦</div>
      <h2 class="text-2xl font-bold text-gray-900 mb-2">{{ $t('orders.empty.title') }}</h2>
      <p class="text-gray-600 mb-6">{{ $t('orders.empty.subtitle') }}</p>
      <NuxtLink to="/" class="bg-orange-500 hover:bg-orange-600 text-white px-6 py-3 rounded-lg">
        {{ $t('orders.empty.shopNow') }}
      </NuxtLink>
    </div>

    <!-- Orders List -->
    <div v-else class="space-y-6">
      <div v-for="order in orders" :key="order.id" class="bg-white rounded-lg border shadow-sm">
        <!-- Order Header -->
        <div class="p-6 border-b border-gray-200">
          <div class="flex flex-col md:flex-row md:items-center md:justify-between">
            <div class="mb-4 md:mb-0">
              <h3 class="text-lg font-semibold text-gray-900">{{ $t('orders.orderCard.orderId', { id: order.id }) }}</h3>
              <p class="text-sm text-gray-500">{{ $t('orders.orderCard.placedOn', { date: formatDate(order.created_at) }) }}</p>
            </div>
            <div class="flex flex-col md:flex-row md:items-center space-y-2 md:space-y-0 md:space-x-4">
              <span :class="['px-3 py-1 rounded-full text-sm font-medium', getOrderStatusColor(order.order_status)]">
                {{ getOrderStatusText(order.order_status) }}
              </span>
              <span :class="['px-3 py-1 rounded-full text-sm font-medium', getPaymentStatusColor(order.payment_status)]">
                {{ getPaymentStatusText(order.payment_status) }}
              </span>
              <span :class="['px-3 py-1 rounded-full text-sm font-medium', getShippingStatusColor(order.shipping_status)]">
                {{ getShippingStatusText(order.shipping_status) }}
              </span>
            </div>
          </div>
        </div>

        <!-- Order Details -->
        <div class="p-6">
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- Customer Info -->
            <div>
              <h4 class="font-medium text-gray-900 mb-3">{{ $t('orders.orderCard.customerInfo') }}</h4>
              <div class="space-y-2 text-sm">
                <p><span class="text-gray-500">{{ $t('orders.orderCard.name') }}</span> {{ order.customer_name }}</p>
                <p v-if="order.company_name"><span class="text-gray-500">{{ $t('orders.orderCard.company') }}</span> {{ order.company_name }}</p>
                <p v-if="order.tax_code"><span class="text-gray-500">{{ $t('orders.orderCard.taxCode') }}</span> {{ order.tax_code }}</p>
                <p><span class="text-gray-500">{{ $t('orders.orderCard.paymentMethod') }}</span> {{ getPaymentMethodText(order.payment_method) }}</p>
              </div>
            </div>

            <!-- Order Items -->
            <div>
              <h4 class="font-medium text-gray-900 mb-3">{{ $t('orders.orderCard.products', { count: order.items.length }) }}</h4>
              <div class="space-y-2">
                <div v-for="item in order.items.slice(0, 3)" :key="item.id" class="text-sm">
                  <p class="font-medium">{{ item.product_name }}</p>
                  <p class="text-gray-500">{{ item.quantity }} {{ item.unit }} × {{ format(item.price) }}</p>
                </div>
                <p v-if="order.items.length > 3" class="text-sm text-gray-500">
                  {{ $t('orders.orderCard.moreProducts', { count: order.items.length - 3 }) }}
                </p>
              </div>
            </div>

            <!-- Order Summary -->
            <div>
              <h4 class="font-medium text-gray-900 mb-3">{{ $t('orders.orderCard.summary') }}</h4>
              <div class="space-y-2 text-sm">
                <div class="flex justify-between">
                  <span class="text-gray-500">{{ $t('orders.orderCard.subtotal') }}</span>
                  <span>{{ format(order.items.reduce((sum, item) => sum + item.amount, 0)) }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-500">{{ $t('orders.orderCard.tax', { rate: (order.vat_rate || 0).toFixed(1) }) }}</span>
                  <span>{{ format(order.items.reduce((sum, item) => sum + item.amount, 0) * ((order.vat_rate || 0) / 100)) }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-500">{{ $t('orders.orderCard.shippingFee') }}</span>
                  <span>{{ format(order.shipping_fee) }}</span>
                </div>
                <div class="flex justify-between font-semibold text-lg border-t pt-2">
                  <span>{{ $t('orders.orderCard.total') }}</span>
                  <span class="text-orange-600">{{ format(calculateOrderTotal(order)) }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Order Actions -->
          <div class="mt-6 pt-6 border-t border-gray-200">
            <div class="flex flex-col sm:flex-row gap-3">
              <NuxtLink 
                :to="`/orders/${order.id}`" 
                class="bg-orange-500 hover:bg-orange-600 text-white px-4 py-2 rounded-lg text-sm font-medium text-center"
              >
                {{ $t('orders.orderCard.viewDetails') }}
              </NuxtLink>
              <button 
                v-if="order.payment_method === 0 && order.payment_status === 0"
                class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium"
              >
                {{ $t('orders.orderCard.payNow') }}
              </button>
              <button 
                v-if="order.order_status === 0"
                class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg text-sm font-medium"
              >
                {{ $t('orders.orderCard.cancelOrder') }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Back to Shop -->
    <div class="mt-8 text-center">
      <NuxtLink to="/" class="text-orange-600 hover:text-orange-700 font-medium">
        {{ $t('orders.orderCard.continueShopping') }}
      </NuxtLink>
    </div>
  </div>
</template>