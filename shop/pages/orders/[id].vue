<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useCurrency } from '~/composables/useCurrency';
import { useOrderService } from '~/services/orders';
import { useI18n } from 'vue-i18n';

const route = useRoute();
const router = useRouter();
const { format } = useCurrency();
const { getOrder } = useOrderService();
const { t } = useI18n();

const order = ref(null);
const loading = ref(true);
const error = ref('');

onMounted(async () => {
  const orderId = route.params.id as string;
  
  if (!orderId) {
    error.value = t('order.errorMessages.noId');
    loading.value = false;
    return;
  }

  try {
    loading.value = true;
    const { data, error: orderError } = await getOrder(orderId);
    
    if (orderError?.value) {
      throw orderError.value;
    }
    
    if (data?.value) {
      order.value = data.value;
    } else {
      throw new Error(t('order.errorMessages.notFound'));
    }
  } catch (e: any) {
    console.error('Lỗi khi tải đơn hàng:', e);
    error.value = e?.message || t('order.errorMessages.loadFailed');
  } finally {
    loading.value = false;
  }
});

const getPaymentMethodText = (method: number) => {
  return method === 0 ? t('order.paymentMethods.bank') : t('order.paymentMethods.cod');
};

const getOrderStatusText = (status: number) => {
  const statusMap = {
    0: t('order.statuses.new'),
    1: t('order.statuses.confirmed'),
    2: t('order.statuses.packing'),
    3: t('order.statuses.shipped'),
    4: t('order.statuses.completed'),
    5: t('order.statuses.canceled')
  };
  return statusMap[status] || t('order.statuses.unknown');
};

const getOrderStatusColor = (status: number) => {
  const colorMap = {
    0: 'bg-blue-100 text-blue-800',
    1: 'bg-green-100 text-green-800',
    2: 'bg-yellow-100 text-yellow-800',
    3: 'bg-purple-100 text-purple-800',
    4: 'bg-green-100 text-green-800',
    5: 'bg-red-100 text-red-800'
  };
  return colorMap[status] || 'bg-gray-100 text-gray-800';
};

const getPaymentStatusText = (status: number) => {
  const statusMap = {
    0: t('order.paymentStatuses.init'),
    1: t('order.paymentStatuses.pending'),
    2: t('order.paymentStatuses.authorized'),
    3: t('order.paymentStatuses.captured'),
    4: t('order.paymentStatuses.completed'),
    5: t('order.paymentStatuses.rejected'),
    6: t('order.paymentStatuses.error'),
    7: t('order.paymentStatuses.canceled'),
    8: t('order.paymentStatuses.paid')
  };
  return statusMap[status] || t('order.statuses.unknown');
};

const getPaymentStatusColor = (status: number) => {
  const colorMap = {
    0: 'bg-blue-100 text-blue-800',
    1: 'bg-yellow-100 text-yellow-800',
    2: 'bg-purple-100 text-purple-800',
    3: 'bg-green-100 text-green-800',
    4: 'bg-green-100 text-green-800',
    5: 'bg-red-100 text-red-800',
    6: 'bg-red-100 text-red-800',
    7: 'bg-gray-100 text-gray-800',
    8: 'bg-green-100 text-green-800'
  };
  return colorMap[status] || 'bg-gray-100 text-gray-800';
};

const getShippingStatusText = (status: number) => {
  const statusMap = {
    0: t('order.shippingStatuses.placed'),
    1: t('order.shippingStatuses.packing'),
    2: t('order.shippingStatuses.delivering'),
    3: t('order.shippingStatuses.delivered'),
    4: t('order.shippingStatuses.returnRequested'),
    5: t('order.shippingStatuses.returning'),
    6: t('order.shippingStatuses.returned')
  };
  return statusMap[status] || t('order.statuses.unknown');
};

const getShippingStatusColor = (status: number) => {
  const colorMap = {
    0: 'bg-blue-100 text-blue-800',
    1: 'bg-yellow-100 text-yellow-800',
    2: 'bg-purple-100 text-purple-800',
    3: 'bg-green-100 text-green-800',
    4: 'bg-orange-100 text-orange-800',
    5: 'bg-red-100 text-red-800',
    6: 'bg-gray-100 text-gray-800'
  };
  return colorMap[status] || 'bg-gray-100 text-gray-800';
};

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('vi-VN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
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
    <!-- Loading State -->
    <div v-if="loading" class="text-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500 mx-auto"></div>
      <p class="mt-4 text-gray-600">{{ $t('order.loading') }}</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-12">
      <div class="text-red-500 text-6xl mb-4">⚠️</div>
      <h2 class="text-2xl font-bold text-gray-900 mb-2">{{ $t('order.error') }}</h2>
      <p class="text-gray-600 mb-6">{{ error }}</p>
      <div class="space-x-4">
        <button @click="router.back()" class="bg-gray-500 hover:bg-gray-600 text-white px-6 py-3 rounded-lg">
          {{ $t('order.back') }}
        </button>
        <button @click="window.location.reload()" class="bg-orange-500 hover:bg-orange-600 text-white px-6 py-3 rounded-lg">
          {{ $t('order.retry') }}
        </button>
      </div>
    </div>

    <!-- Order Details -->
    <div v-else-if="order" class="max-w-6xl mx-auto">
      <!-- Header -->
      <div class="mb-8">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">{{ $t('order.title') }} #{{ order.id }}</h1>
            <p class="text-gray-600">{{ $t('order.placedOn') }} {{ formatDate(order.created_at) }}</p>
          </div>
          <div class="flex flex-wrap gap-3">
            <span :class="['px-4 py-2 rounded-full text-sm font-medium', getOrderStatusColor(order.order_status)]">
              {{ getOrderStatusText(order.order_status) }}
            </span>
            <span :class="['px-4 py-2 rounded-full text-sm font-medium', getPaymentStatusColor(order.payment_status)]">
              {{ getPaymentStatusText(order.payment_status) }}
            </span>
            <span :class="['px-4 py-2 rounded-full text-sm font-medium', getShippingStatusColor(order.shipping_status)]">
              {{ getShippingStatusText(order.shipping_status) }}
            </span>
          </div>
        </div>
        
        <!-- Navigation -->
        <div class="flex items-center space-x-2 text-sm text-gray-500">
          <NuxtLink to="/orders" class="hover:text-orange-600">{{ $t('order.title_plural') }}</NuxtLink>
          <span>›</span>
          <span>{{ $t('order.details') }}</span>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Main Content -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Customer Information -->
          <div class="bg-white rounded-lg border p-6">
            <h2 class="text-xl font-semibold mb-4">{{ $t('order.customerInfo') }}</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="text-sm font-medium text-gray-500">{{ $t('order.customerName') }}</label>
                <p class="text-lg">{{ order.customer_name }}</p>
              </div>
              <div v-if="order.company_name">
                <label class="text-sm font-medium text-gray-500">{{ $t('order.company') }}</label>
                <p class="text-lg">{{ order.company_name }}</p>
              </div>
              <div v-if="order.tax_code">
                <label class="text-sm font-medium text-gray-500">{{ $t('order.taxCode') }}</label>
                <p class="text-lg">{{ order.tax_code }}</p>
              </div>
              <div>
                <label class="text-sm font-medium text-gray-500">{{ $t('order.paymentMethod') }}</label>
                <p class="text-lg">{{ getPaymentMethodText(order.payment_method) }}</p>
              </div>
            </div>
          </div>

          <!-- Order Items -->
          <div class="bg-white rounded-lg border p-6">
            <h2 class="text-xl font-semibold mb-4">{{ $t('order.productList') }}</h2>
            <div class="space-y-4">
              <div v-for="item in order.items" :key="item.id" class="flex items-center justify-between py-4 border-b border-gray-200 last:border-b-0">
                <div class="flex-1">
                  <h3 class="font-medium text-lg">{{ item.product_name }}</h3>
                  <p class="text-sm text-gray-500">{{ $t('order.quantity') }}: {{ item.quantity }} {{ item.unit }}</p>
                  <p class="text-sm text-gray-500">{{ $t('order.unitPrice') }}: {{ format(item.price) }}</p>
                </div>
                <div class="text-right">
                  <p class="text-lg font-semibold">{{ format(item.amount) }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Payment Information -->
          <div v-if="order.payment_method === 0" class="bg-blue-50 border border-blue-200 rounded-lg p-6">
            <h2 class="text-xl font-semibold text-blue-900 mb-4">{{ $t('order.paymentInfo') }}</h2>
            <div class="text-center">
              <div v-if="order.payment_status === 0" class="mb-4">
                <p class="text-gray-700 mb-4">{{ $t('order.paymentWaiting') }}</p>
                <div class="bg-white p-4 rounded-lg border-2 border-dashed border-blue-300">
                  <div class="text-gray-500 text-sm mb-2">{{ $t('order.qrCode') }}</div>
                  <div class="w-48 h-48 bg-gray-100 mx-auto rounded-lg flex items-center justify-center">
                    <div class="text-gray-400 text-sm">{{ $t('order.qrCode') }}</div>
                  </div>
                </div>
                <p class="text-sm text-gray-600 mt-4">
                  {{ $t('order.qrInstruction') }}
                </p>
              </div>
              <div v-else-if="order.payment_status === 1" class="text-green-600">
                <div class="text-4xl mb-2">✅</div>
                <p class="font-medium">{{ $t('order.paymentSuccess') }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Sidebar -->
        <div class="space-y-6">
          <!-- Order Summary -->
          <div class="bg-white rounded-lg border p-6">
            <h2 class="text-xl font-semibold mb-4">{{ $t('order.orderSummary') }}</h2>
            <div class="space-y-3">
              <div class="flex justify-between">
                <span class="text-gray-600">{{ $t('order.subtotal') }}</span>
                <span>{{ format(order.items.reduce((sum, item) => sum + item.amount, 0)) }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">{{ $t('order.tax') }} ({{ (order.vat_rate || 0).toFixed(1) }}%)</span>
                <span>{{ format(order.items.reduce((sum, item) => sum + item.amount, 0) * ((order.vat_rate || 0) / 100)) }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">{{ $t('order.shippingFee') }}</span>
                <span>{{ format(order.shipping_fee) }}</span>
              </div>
              <div class="border-t pt-3">
                <div class="flex justify-between text-lg font-bold">
                  <span>{{ $t('order.total') }}</span>
                  <span class="text-orange-600">{{ format(calculateOrderTotal(order)) }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Order Actions -->
          <div class="bg-white rounded-lg border p-6">
            <h2 class="text-xl font-semibold mb-4">{{ $t('order.actions') }}</h2>
            <div class="space-y-3">
              <button 
                v-if="order.payment_method === 0 && order.payment_status === 0"
                class="w-full bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-lg font-medium"
              >
                {{ $t('order.pay') }}
              </button>
              <button 
                v-if="order.order_status === 0"
                class="w-full bg-red-500 hover:bg-red-600 text-white py-2 px-4 rounded-lg font-medium"
              >
                {{ $t('order.cancel') }}
              </button>
              <button 
                @click="window.print()"
                class="w-full bg-gray-500 hover:bg-gray-600 text-white py-2 px-4 rounded-lg font-medium"
              >
                {{ $t('order.print') }}
              </button>
              <NuxtLink 
                to="/orders"
                class="w-full bg-orange-500 hover:bg-orange-600 text-white py-2 px-4 rounded-lg font-medium text-center block"
              >
                {{ $t('order.back') }}
              </NuxtLink>
            </div>
          </div>

          <!-- Order Timeline -->
          <div class="bg-white rounded-lg border p-6">
            <h2 class="text-xl font-semibold mb-4">{{ $t('order.timeline') }}</h2>
            <div class="space-y-4">
              <div class="flex items-center">
                <div class="w-3 h-3 bg-green-500 rounded-full mr-3"></div>
                <div>
                  <p class="font-medium">{{ $t('order.timelineEvents.created') }}</p>
                  <p class="text-sm text-gray-500">{{ formatDate(order.created_at) }}</p>
                </div>
              </div>
              <div v-if="order.order_status >= 1" class="flex items-center">
                <div class="w-3 h-3 bg-green-500 rounded-full mr-3"></div>
                <div>
                  <p class="font-medium">{{ $t('order.statuses.confirmed') }}</p>
                  <p class="text-sm text-gray-500">{{ $t('order.timelineEvents.confirmed') }}</p>
                </div>
              </div>
              <div v-if="order.order_status >= 2" class="flex items-center">
                <div class="w-3 h-3 bg-yellow-500 rounded-full mr-3"></div>
                <div>
                  <p class="font-medium">{{ $t('order.statuses.packing') }}</p>
                  <p class="text-sm text-gray-500">{{ $t('order.timelineEvents.packing') }}</p>
                </div>
              </div>
              <div v-if="order.order_status >= 3" class="flex items-center">
                <div class="w-3 h-3 bg-purple-500 rounded-full mr-3"></div>
                <div>
                  <p class="font-medium">{{ $t('order.statuses.shipped') }}</p>
                  <p class="text-sm text-gray-500">{{ $t('order.timelineEvents.shipped') }}</p>
                </div>
              </div>
              <div v-if="order.order_status >= 4" class="flex items-center">
                <div class="w-3 h-3 bg-green-500 rounded-full mr-3"></div>
                <div>
                  <p class="font-medium">{{ $t('order.statuses.completed') }}</p>
                  <p class="text-sm text-gray-500">{{ $t('order.timelineEvents.completed') }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@media print {
  .container {
    max-width: none;
    margin: 0;
    padding: 0;
  }
  
  .bg-orange-500, .bg-blue-500, .bg-red-500, .bg-gray-500 {
    display: none;
  }
}
</style>