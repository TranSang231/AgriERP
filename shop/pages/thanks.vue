<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useI18n } from 'vue-i18n';
import { useCurrency } from '~/composables/useCurrency';
import { useOrderService } from '~/services/orders';

const { t } = useI18n();
const route = useRoute();
const { format } = useCurrency();
const { getOrder } = useOrderService();

const order = ref(null);
const loading = ref(true);
const error = ref('');

onMounted(async () => {
  const orderId = route.query.order_id as string;
  
  if (!orderId) {
    error.value = t('thanks.errorMessages.notFound');
    loading.value = false;
    return;
  }

  try {
    const data = await getOrder(orderId);
    
    if (data) {
      order.value = data;
    } else {
      throw new Error(t('thanks.errorMessages.notFound'));
    }
  } catch (e: any) {
    console.error('Lỗi khi tải đơn hàng:', e);
    error.value = e?.message || t('thanks.errorMessages.loadFailed');
  } finally {
    loading.value = false;
  }
});

const getPaymentMethodText = (method: number) => {
  const key = method === 0 ? 'orders.paymentMethods.bank_transfer' : 'orders.paymentMethods.cod';
  return t(key);
};

const getOrderStatusText = (status: number) => {
  const statusMap: { [key: number]: string } = {
    0: 'new',
    1: 'confirmed',
    2: 'packing',
    3: 'shipped',
    4: 'completed',
    5: 'canceled'
  };
  const statusKey = statusMap[status] || 'unknown';
  return t(`order.statuses.${statusKey}`);
};
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <div v-if="loading" class="text-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500 mx-auto"></div>
      <p class="mt-4 text-gray-600">{{ $t('thanks.loading') }}</p>
    </div>

    <div v-else-if="error" class="text-center py-12">
      <div class="text-red-500 text-6xl mb-4">⚠️</div>
      <h2 class="text-2xl font-bold text-gray-900 mb-2">{{ $t('thanks.errorTitle') }}</h2>
      <p class="text-gray-600 mb-6">{{ error }}</p>
      <NuxtLink to="/" class="bg-orange-500 hover:bg-orange-600 text-white px-6 py-3 rounded-lg">
        {{ $t('thanks.backToHome') }}
      </NuxtLink>
    </div>

    <div v-else-if="order" class="max-w-4xl mx-auto">
      <!-- Header -->
      <div class="text-center mb-8">
        <div class="text-green-500 text-6xl mb-4">✅</div>
        <h1 class="text-3xl font-bold text-gray-900 mb-2">{{ $t('thanks.successTitle') }}</h1>
        <p class="text-gray-600">{{ $t('thanks.successSubtitle') }}</p>
      </div>

      <!-- Order Info -->
      <div class="bg-white rounded-lg border p-6 mb-6">
        <h2 class="text-xl font-semibold mb-4">{{ $t('thanks.orderInfoTitle') }}</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="text-sm font-medium text-gray-500">{{ $t('thanks.orderId') }}</label>
            <p class="text-lg font-semibold">{{ order.id }}</p>
          </div>
          <div>
            <label class="text-sm font-medium text-gray-500">{{ $t('thanks.orderDate') }}</label>
            <p class="text-lg">{{ new Date(order.created_at).toLocaleDateString('vi-VN') }}</p>
          </div>
          <div>
            <label class="text-sm font-medium text-gray-500">{{ $t('thanks.paymentMethod') }}</label>
            <p class="text-lg">{{ getPaymentMethodText(order.payment_method) }}</p>
          </div>
          <div>
            <label class="text-sm font-medium text-gray-500">{{ $t('thanks.status') }}</label>
            <p class="text-lg">{{ getOrderStatusText(order.order_status) }}</p>
          </div>
        </div>
      </div>

      <!-- Customer Info -->
      <div class="bg-white rounded-lg border p-6 mb-6">
        <h2 class="text-xl font-semibold mb-4">{{ $t('thanks.customerInfoTitle') }}</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="text-sm font-medium text-gray-500">{{ $t('thanks.customerName') }}</label>
            <p class="text-lg">{{ order.customer_name }}</p>
          </div>
          <div v-if="order.company_name">
            <label class="text-sm font-medium text-gray-500">{{ $t('thanks.company') }}</label>
            <p class="text-lg">{{ order.company_name }}</p>
          </div>
          <div v-if="order.tax_code">
            <label class="text-sm font-medium text-gray-500">{{ $t('thanks.taxCode') }}</label>
            <p class="text-lg">{{ order.tax_code }}</p>
          </div>
        </div>
      </div>

      <!-- Order Items -->
      <div class="bg-white rounded-lg border p-6 mb-6">
        <h2 class="text-xl font-semibold mb-4">{{ $t('thanks.itemsTitle') }}</h2>
        <div class="space-y-4">
          <div v-for="item in order.items" :key="item.id" class="flex items-center justify-between py-3 border-b border-gray-200 last:border-b-0">
            <div class="flex-1">
              <h3 class="font-medium">{{ item.product_name }}</h3>
              <p class="text-sm text-gray-500">{{ $t('thanks.quantity') }} {{ item.quantity }} {{ item.unit }}</p>
            </div>
            <div class="text-right">
              <p class="font-semibold">{{ format(item.amount) }}</p>
              <p class="text-sm text-gray-500">{{ format(item.price) }} / {{ item.unit }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Order Summary -->
      <div class="bg-white rounded-lg border p-6 mb-6">
        <h2 class="text-xl font-semibold mb-4">{{ $t('thanks.summaryTitle') }}</h2>
        <div class="space-y-2">
          <div class="flex justify-between">
            <span>{{ $t('thanks.subtotal') }}</span>
            <span>{{ format(order.items.reduce((sum, item) => sum + item.amount, 0)) }}</span>
          </div>
          <div class="flex justify-between">
            <span>{{ $t('thanks.tax') }} ({{ (order.vat_rate || 0).toFixed(1) }}%)</span>
            <span>{{ format(order.items.reduce((sum, item) => sum + item.amount, 0) * ((order.vat_rate || 0) / 100)) }}</span>
          </div>
          <div class="flex justify-between">
            <span>{{ $t('thanks.shippingFee') }}</span>
            <span>{{ format(order.shipping_fee || 0) }}</span>
          </div>
          <div class="border-t pt-2">
            <div class="flex justify-between text-lg font-bold">
              <span>{{ $t('thanks.total') }}</span>
              <span class="text-orange-600">{{ format(order.items.reduce((sum, item) => sum + item.amount, 0) * (1 + (order.vat_rate || 0) / 100) + (order.shipping_fee || 0)) }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Payment Info -->
      <div v-if="order.payment_method === 0" class="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-6">
        <h2 class="text-xl font-semibold text-blue-900 mb-4">{{ $t('thanks.paymentInfoTitle') }}</h2>
        <div class="text-center">
          <p class="text-gray-700 mb-4">{{ $t('thanks.paymentPending') }}</p>
          <p class="text-sm text-gray-600">{{ $t('thanks.paymentConfirmation') }}</p>
        </div>
      </div>

      <!-- Actions -->
      <div class="text-center">
        <NuxtLink to="/" class="bg-orange-500 hover:bg-orange-600 text-white px-8 py-3 rounded-lg font-semibold mr-4">
          {{ $t('thanks.continueShopping') }}
        </NuxtLink>
        <button @click="window.print()" class="bg-gray-500 hover:bg-gray-600 text-white px-8 py-3 rounded-lg font-semibold">
          {{ $t('thanks.printOrder') }}
        </button>
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
  
  .bg-orange-500, .bg-gray-500 {
    display: none;
  }
}
</style>