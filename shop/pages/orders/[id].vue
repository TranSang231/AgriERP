<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useCurrency } from '~/composables/useCurrency';
import { useOrderService } from '~/services/orders';

const route = useRoute();
const router = useRouter();
const { format } = useCurrency();
const { getOrder } = useOrderService();

const order = ref(null);
const loading = ref(true);
const error = ref('');

onMounted(async () => {
  const orderId = route.params.id as string;
  
  if (!orderId) {
    error.value = 'Không tìm thấy ID đơn hàng';
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
      throw new Error('Không tìm thấy đơn hàng');
    }
  } catch (e: any) {
    console.error('Lỗi khi tải đơn hàng:', e);
    error.value = e?.message || 'Không thể tải thông tin đơn hàng';
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
    <!-- Loading State -->
    <div v-if="loading" class="text-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-orange-500 mx-auto"></div>
      <p class="mt-4 text-gray-600">Đang tải thông tin đơn hàng...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-12">
      <div class="text-red-500 text-6xl mb-4">⚠️</div>
      <h2 class="text-2xl font-bold text-gray-900 mb-2">Có lỗi xảy ra</h2>
      <p class="text-gray-600 mb-6">{{ error }}</p>
      <div class="space-x-4">
        <button @click="router.back()" class="bg-gray-500 hover:bg-gray-600 text-white px-6 py-3 rounded-lg">
          Quay lại
        </button>
        <button @click="window.location.reload()" class="bg-orange-500 hover:bg-orange-600 text-white px-6 py-3 rounded-lg">
          Thử lại
        </button>
      </div>
    </div>

    <!-- Order Details -->
    <div v-else-if="order" class="max-w-6xl mx-auto">
      <!-- Header -->
      <div class="mb-8">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">Đơn hàng #{{ order.id }}</h1>
            <p class="text-gray-600">Đặt ngày {{ formatDate(order.created_at) }}</p>
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
          <NuxtLink to="/orders" class="hover:text-orange-600">Đơn hàng</NuxtLink>
          <span>›</span>
          <span>Chi tiết đơn hàng</span>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Main Content -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Customer Information -->
          <div class="bg-white rounded-lg border p-6">
            <h2 class="text-xl font-semibold mb-4">Thông tin khách hàng</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="text-sm font-medium text-gray-500">Tên khách hàng</label>
                <p class="text-lg">{{ order.customer_name }}</p>
              </div>
              <div v-if="order.company_name">
                <label class="text-sm font-medium text-gray-500">Công ty</label>
                <p class="text-lg">{{ order.company_name }}</p>
              </div>
              <div v-if="order.tax_code">
                <label class="text-sm font-medium text-gray-500">Mã số thuế</label>
                <p class="text-lg">{{ order.tax_code }}</p>
              </div>
              <div>
                <label class="text-sm font-medium text-gray-500">Phương thức thanh toán</label>
                <p class="text-lg">{{ getPaymentMethodText(order.payment_method) }}</p>
              </div>
            </div>
          </div>

          <!-- Order Items -->
          <div class="bg-white rounded-lg border p-6">
            <h2 class="text-xl font-semibold mb-4">Sản phẩm đã đặt</h2>
            <div class="space-y-4">
              <div v-for="item in order.items" :key="item.id" class="flex items-center justify-between py-4 border-b border-gray-200 last:border-b-0">
                <div class="flex-1">
                  <h3 class="font-medium text-lg">{{ item.product_name }}</h3>
                  <p class="text-sm text-gray-500">Số lượng: {{ item.quantity }} {{ item.unit }}</p>
                  <p class="text-sm text-gray-500">Đơn giá: {{ format(item.price) }}</p>
                </div>
                <div class="text-right">
                  <p class="text-lg font-semibold">{{ format(item.amount) }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Payment Information -->
          <div v-if="order.payment_method === 0" class="bg-blue-50 border border-blue-200 rounded-lg p-6">
            <h2 class="text-xl font-semibold text-blue-900 mb-4">Thông tin thanh toán</h2>
            <div class="text-center">
              <div v-if="order.payment_status === 0" class="mb-4">
                <p class="text-gray-700 mb-4">Đơn hàng đang chờ xác nhận thanh toán.</p>
                <div class="bg-white p-4 rounded-lg border-2 border-dashed border-blue-300">
                  <div class="text-gray-500 text-sm mb-2">QR Code thanh toán</div>
                  <div class="w-48 h-48 bg-gray-100 mx-auto rounded-lg flex items-center justify-center">
                    <div class="text-gray-400 text-sm">QR Code</div>
                  </div>
                </div>
                <p class="text-sm text-gray-600 mt-4">
                  Quét QR code bằng ứng dụng ngân hàng để thanh toán
                </p>
              </div>
              <div v-else-if="order.payment_status === 1" class="text-green-600">
                <div class="text-4xl mb-2">✅</div>
                <p class="font-medium">Đã thanh toán thành công</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Sidebar -->
        <div class="space-y-6">
          <!-- Order Summary -->
          <div class="bg-white rounded-lg border p-6">
            <h2 class="text-xl font-semibold mb-4">Tóm tắt đơn hàng</h2>
            <div class="space-y-3">
              <div class="flex justify-between">
                <span class="text-gray-600">Tạm tính</span>
                <span>{{ format(order.items.reduce((sum, item) => sum + item.amount, 0)) }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">Thuế ({{ (order.vat_rate || 0).toFixed(1) }}%)</span>
                <span>{{ format(order.items.reduce((sum, item) => sum + item.amount, 0) * ((order.vat_rate || 0) / 100)) }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">Phí vận chuyển</span>
                <span>{{ format(order.shipping_fee) }}</span>
              </div>
              <div class="border-t pt-3">
                <div class="flex justify-between text-lg font-bold">
                  <span>Tổng cộng</span>
                  <span class="text-orange-600">{{ format(calculateOrderTotal(order)) }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Order Actions -->
          <div class="bg-white rounded-lg border p-6">
            <h2 class="text-xl font-semibold mb-4">Thao tác</h2>
            <div class="space-y-3">
              <button 
                v-if="order.payment_method === 0 && order.payment_status === 0"
                class="w-full bg-blue-500 hover:bg-blue-600 text-white py-2 px-4 rounded-lg font-medium"
              >
                Thanh toán
              </button>
              <button 
                v-if="order.order_status === 0"
                class="w-full bg-red-500 hover:bg-red-600 text-white py-2 px-4 rounded-lg font-medium"
              >
                Hủy đơn hàng
              </button>
              <button 
                @click="window.print()"
                class="w-full bg-gray-500 hover:bg-gray-600 text-white py-2 px-4 rounded-lg font-medium"
              >
                In đơn hàng
              </button>
              <NuxtLink 
                to="/orders"
                class="w-full bg-orange-500 hover:bg-orange-600 text-white py-2 px-4 rounded-lg font-medium text-center block"
              >
                Quay lại danh sách
              </NuxtLink>
            </div>
          </div>

          <!-- Order Timeline -->
          <div class="bg-white rounded-lg border p-6">
            <h2 class="text-xl font-semibold mb-4">Trạng thái đơn hàng</h2>
            <div class="space-y-4">
              <div class="flex items-center">
                <div class="w-3 h-3 bg-green-500 rounded-full mr-3"></div>
                <div>
                  <p class="font-medium">Đơn hàng đã được tạo</p>
                  <p class="text-sm text-gray-500">{{ formatDate(order.created_at) }}</p>
                </div>
              </div>
              <div v-if="order.order_status >= 1" class="flex items-center">
                <div class="w-3 h-3 bg-green-500 rounded-full mr-3"></div>
                <div>
                  <p class="font-medium">Đã xác nhận</p>
                  <p class="text-sm text-gray-500">Đơn hàng đã được xác nhận</p>
                </div>
              </div>
              <div v-if="order.order_status >= 2" class="flex items-center">
                <div class="w-3 h-3 bg-yellow-500 rounded-full mr-3"></div>
                <div>
                  <p class="font-medium">Đang đóng gói</p>
                  <p class="text-sm text-gray-500">Đơn hàng đang được đóng gói</p>
                </div>
              </div>
              <div v-if="order.order_status >= 3" class="flex items-center">
                <div class="w-3 h-3 bg-purple-500 rounded-full mr-3"></div>
                <div>
                  <p class="font-medium">Đã giao hàng</p>
                  <p class="text-sm text-gray-500">Đơn hàng đã được giao</p>
                </div>
              </div>
              <div v-if="order.order_status >= 4" class="flex items-center">
                <div class="w-3 h-3 bg-green-500 rounded-full mr-3"></div>
                <div>
                  <p class="font-medium">Hoàn thành</p>
                  <p class="text-sm text-gray-500">Đơn hàng đã hoàn thành</p>
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
