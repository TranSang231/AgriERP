<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useCurrency } from '~/composables/useCurrency';
import { useOrderService } from '~/services/orders';
import { useAuthStore } from '~/stores/auth';

const { format } = useCurrency();
const { getOrders } = useOrderService();
const auth = useAuthStore();

const orders = ref([]);
const loading = ref(true);
const error = ref('');

onMounted(async () => {
  try {
    loading.value = true;
    const customerId = (auth.user as any)?.id;
    const { data, error: ordersError } = await getOrders(customerId ? { customer_id: customerId } : undefined);
    
    if (ordersError?.value) {
      throw ordersError.value;
    }
    
    if (data?.value) {
      orders.value = data.value;
    } else {
      orders.value = [];
    }
  } catch (e: any) {
    console.error('Lỗi khi tải danh sách đơn hàng:', e);
    error.value = e?.message || 'Không thể tải danh sách đơn hàng';
  } finally {
    loading.value = false;
  }
});

const getPaymentMethodText = (method: number) => {
  return method === 0 ? 'Chuyển khoản ngân hàng' : 'Thanh toán khi nhận hàng (COD)';
};

const getOrderStatusText = (status: number) => {
  const statusMap = {
    0: 'Mới',
    1: 'Đã xác nhận', 
    2: 'Đang đóng gói',
    3: 'Đã giao hàng',
    4: 'Hoàn thành',
    5: 'Đã hủy'
  };
  return statusMap[status] || 'Không xác định';
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
    0: 'Đã khởi tạo',
    1: 'Đang chờ',
    2: 'Đã ủy quyền',
    3: 'Đã thu tiền',
    4: 'Hoàn thành',
    5: 'Từ chối',
    6: 'Lỗi',
    7: 'Đã hủy',
    8: 'Đã thanh toán'
  };
  return statusMap[status] || 'Không xác định';
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
    0: 'Đã đặt hàng',
    1: 'Đang đóng gói',
    2: 'Đang giao hàng',
    3: 'Đã giao hàng',
    4: 'Yêu cầu trả hàng',
    5: 'Đang trả hàng',
    6: 'Đã trả hàng'
  };
  return statusMap[status] || 'Không xác định';
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
  // vat_rate trong DB là phần trăm (800 = 8%), cần chia cho 100
  const vatRate = (order.vat_rate || 0) / 100;
  const tax = subtotal * vatRate;
  const shippingFee = order.shipping_fee || 0;
  return subtotal + tax + shippingFee;
};
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">Đơn hàng của tôi</h1>
      <p class="text-gray-600">Quản lý và theo dõi các đơn hàng đã đặt</p>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500 mx-auto"></div>
      <p class="mt-4 text-gray-600">Đang tải danh sách đơn hàng...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-12">
      <div class="text-red-500 text-6xl mb-4">⚠️</div>
      <h2 class="text-2xl font-bold text-gray-900 mb-2">Có lỗi xảy ra</h2>
      <p class="text-gray-600 mb-6">{{ error }}</p>
      <button @click="window.location.reload()" class="bg-orange-500 hover:bg-orange-600 text-white px-6 py-3 rounded-lg">
        Thử lại
      </button>
    </div>

    <!-- Empty State -->
    <div v-else-if="orders.length === 0" class="text-center py-12">
      <div class="text-gray-400 text-6xl mb-4">📦</div>
      <h2 class="text-2xl font-bold text-gray-900 mb-2">Chưa có đơn hàng nào</h2>
      <p class="text-gray-600 mb-6">Bạn chưa đặt đơn hàng nào. Hãy bắt đầu mua sắm!</p>
      <NuxtLink to="/" class="bg-orange-500 hover:bg-orange-600 text-white px-6 py-3 rounded-lg">
        Mua sắm ngay
      </NuxtLink>
    </div>

    <!-- Orders List -->
    <div v-else class="space-y-6">
      <div v-for="order in orders" :key="order.id" class="bg-white rounded-lg border shadow-sm">
        <!-- Order Header -->
        <div class="p-6 border-b border-gray-200">
          <div class="flex flex-col md:flex-row md:items-center md:justify-between">
            <div class="mb-4 md:mb-0">
              <h3 class="text-lg font-semibold text-gray-900">Đơn hàng #{{ order.id }}</h3>
              <p class="text-sm text-gray-500">Đặt ngày {{ formatDate(order.created_at) }}</p>
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
              <h4 class="font-medium text-gray-900 mb-3">Thông tin khách hàng</h4>
              <div class="space-y-2 text-sm">
                <p><span class="text-gray-500">Tên:</span> {{ order.customer_name }}</p>
                <p v-if="order.company_name"><span class="text-gray-500">Công ty:</span> {{ order.company_name }}</p>
                <p v-if="order.tax_code"><span class="text-gray-500">MST:</span> {{ order.tax_code }}</p>
                <p><span class="text-gray-500">Thanh toán:</span> {{ getPaymentMethodText(order.payment_method) }}</p>
              </div>
            </div>

            <!-- Order Items -->
            <div>
              <h4 class="font-medium text-gray-900 mb-3">Sản phẩm ({{ order.items.length }})</h4>
              <div class="space-y-2">
                <div v-for="item in order.items.slice(0, 3)" :key="item.id" class="text-sm">
                  <p class="font-medium">{{ item.product_name }}</p>
                  <p class="text-gray-500">{{ item.quantity }} {{ item.unit }} × {{ format(item.price) }}</p>
                </div>
                <p v-if="order.items.length > 3" class="text-sm text-gray-500">
                  +{{ order.items.length - 3 }} sản phẩm khác
                </p>
              </div>
            </div>

            <!-- Order Summary -->
            <div>
              <h4 class="font-medium text-gray-900 mb-3">Tóm tắt</h4>
              <div class="space-y-2 text-sm">
                <div class="flex justify-between">
                  <span class="text-gray-500">Tạm tính:</span>
                  <span>{{ format(order.items.reduce((sum, item) => sum + item.amount, 0)) }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-500">Thuế ({{ (order.vat_rate || 0).toFixed(1) }}%):</span>
                  <span>{{ format(order.items.reduce((sum, item) => sum + item.amount, 0) * ((order.vat_rate || 0) / 100)) }}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-gray-500">Phí vận chuyển:</span>
                  <span>{{ format(order.shipping_fee) }}</span>
                </div>
                <div class="flex justify-between font-semibold text-lg border-t pt-2">
                  <span>Tổng cộng:</span>
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
                Xem chi tiết
              </NuxtLink>
              <button 
                v-if="order.payment_method === 0 && order.payment_status === 0"
                class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium"
              >
                Thanh toán
              </button>
              <button 
                v-if="order.order_status === 0"
                class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg text-sm font-medium"
              >
                Hủy đơn hàng
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Back to Shop -->
    <div class="mt-8 text-center">
      <NuxtLink to="/" class="text-orange-600 hover:text-orange-700 font-medium">
        ← Tiếp tục mua sắm
      </NuxtLink>
    </div>
  </div>
</template>
