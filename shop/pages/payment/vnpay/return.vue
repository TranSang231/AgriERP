<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useVNPayService } from '~/services/vnpayService'
import { useCartStore } from '~/stores/cart'
import { useCheckoutStore } from '~/stores/checkout'
import { useCurrency } from '~/composables/useCurrency'

const route = useRoute()
const router = useRouter()
const { getPaymentResult } = useVNPayService()
const cartStore = useCartStore()
const checkoutStore = useCheckoutStore()
const { format } = useCurrency()

const loading = ref(true)
const paymentResult = ref<any>(null)
const error = ref('')

useHead({
  title: 'Kết quả thanh toán - VNPay'
})

onMounted(async () => {
  try {
    // Lấy tất cả query params từ VNPay
    const queryParams = Object.fromEntries(
      Object.entries(route.query).map(([k, v]) => [k, String(v)])
    )
    
    if (Object.keys(queryParams).length === 0) {
      error.value = 'Không tìm thấy thông tin thanh toán'
      loading.value = false
      return
    }
    
    // Validate payment với backend
    const result = await getPaymentResult(queryParams)
    paymentResult.value = result
    
    // Nếu thanh toán thành công, clear cart và checkout
    if (result.success) {
      checkoutStore.clear()
      // Clear all items from cart
      const cartItems = cartStore.items
      cartItems.forEach(item => {
        cartStore.remove(item.productId)
      })
    }
    
  } catch (e: any) {
    console.error('Error processing VNPay return:', e)
    error.value = e?.data?.error || e?.message || 'Có lỗi xảy ra khi xử lý thanh toán'
  } finally {
    loading.value = false
  }
})

const goToOrders = () => {
  router.push('/orders')
}

const goToHome = () => {
  router.push('/')
}

const retryPayment = () => {
  router.push('/checkout')
}
</script>

<template>
  <div class="container mx-auto px-4 py-8 min-h-screen">
    <!-- Loading State -->
    <div v-if="loading" class="flex flex-col items-center justify-center py-20">
      <div class="animate-spin rounded-full h-16 w-16 border-b-4 border-orange-500 mb-4"></div>
      <p class="text-xl text-gray-600">Đang xử lý thanh toán...</p>
      <p class="text-sm text-gray-500 mt-2">Vui lòng không đóng trang này</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="max-w-md mx-auto">
      <div class="bg-red-50 border-2 border-red-200 rounded-lg p-8 text-center shadow-lg">
        <div class="text-6xl mb-4">⚠️</div>
        <h2 class="text-2xl font-bold text-red-700 mb-3">Có lỗi xảy ra</h2>
        <p class="text-gray-700 mb-6">{{ error }}</p>
        <button 
          @click="goToHome" 
          class="bg-orange-500 text-white px-8 py-3 rounded-lg hover:bg-orange-600 transition-colors font-semibold"
        >
          Về trang chủ
        </button>
      </div>
    </div>

    <!-- Payment Result -->
    <div v-else-if="paymentResult" class="max-w-2xl mx-auto">
      <!-- Success -->
      <div v-if="paymentResult.success" class="bg-white rounded-xl shadow-xl overflow-hidden">
        <div class="bg-gradient-to-r from-green-400 to-green-600 p-8 text-center text-white">
          <div class="text-6xl mb-3">✅</div>
          <h2 class="text-3xl font-bold mb-2">Thanh toán thành công!</h2>
          <p class="text-green-100">{{ paymentResult.message }}</p>
        </div>
        
        <div class="p-8">
          <div class="bg-gray-50 rounded-lg p-6 mb-6">
            <h3 class="text-lg font-semibold text-gray-800 mb-4">Thông tin giao dịch</h3>
            <div class="space-y-3">
              <div class="flex justify-between items-center py-2 border-b border-gray-200">
                <span class="text-gray-600">Mã đơn hàng</span>
                <span class="font-bold text-gray-900">#{{ paymentResult.order_id }}</span>
              </div>
              <div class="flex justify-between items-center py-2 border-b border-gray-200">
                <span class="text-gray-600">Số tiền thanh toán</span>
                <span class="font-bold text-green-600 text-xl">{{ format(paymentResult.amount) }}</span>
              </div>
              <div class="flex justify-between items-center py-2 border-b border-gray-200">
                <span class="text-gray-600">Mã giao dịch VNPay</span>
                <span class="font-mono text-sm text-gray-900">{{ paymentResult.transaction_no }}</span>
              </div>
              <div v-if="paymentResult.bank_code" class="flex justify-between items-center py-2 border-b border-gray-200">
                <span class="text-gray-600">Ngân hàng</span>
                <span class="font-semibold text-gray-900">{{ paymentResult.bank_code }}</span>
              </div>
              <div v-if="paymentResult.card_type" class="flex justify-between items-center py-2">
                <span class="text-gray-600">Loại thẻ</span>
                <span class="font-semibold text-gray-900">{{ paymentResult.card_type }}</span>
              </div>
            </div>
          </div>

          <div class="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
            <p class="text-sm text-blue-800">
              <strong>Lưu ý:</strong> Đơn hàng của bạn đang được xử lý. Chúng tôi sẽ gửi email xác nhận và cập nhật tình trạng đơn hàng sớm nhất.
            </p>
          </div>

          <div class="flex flex-col sm:flex-row gap-3">
            <button 
              @click="goToOrders" 
              class="flex-1 bg-orange-500 text-white px-6 py-4 rounded-lg hover:bg-orange-600 transition-colors font-semibold text-lg"
            >
              Xem đơn hàng của tôi
            </button>
            <button 
              @click="goToHome" 
              class="flex-1 bg-gray-200 text-gray-700 px-6 py-4 rounded-lg hover:bg-gray-300 transition-colors font-semibold text-lg"
            >
              Tiếp tục mua sắm
            </button>
          </div>
        </div>
      </div>

      <!-- Failure -->
      <div v-else class="bg-white rounded-xl shadow-xl overflow-hidden">
        <div class="bg-gradient-to-r from-red-400 to-red-600 p-8 text-center text-white">
          <div class="text-6xl mb-3">❌</div>
          <h2 class="text-3xl font-bold mb-2">Thanh toán thất bại</h2>
          <p class="text-red-100">{{ paymentResult.message }}</p>
        </div>
        
        <div class="p-8">
          <div class="bg-gray-50 rounded-lg p-6 mb-6">
            <h3 class="text-lg font-semibold text-gray-800 mb-4">Chi tiết lỗi</h3>
            <div class="space-y-3">
              <div class="flex justify-between items-center py-2 border-b border-gray-200">
                <span class="text-gray-600">Mã đơn hàng</span>
                <span class="font-bold text-gray-900">#{{ paymentResult.order_id }}</span>
              </div>
              <div class="flex justify-between items-center py-2 border-b border-gray-200">
                <span class="text-gray-600">Mã lỗi</span>
                <span class="font-mono text-sm text-red-600 font-bold">{{ paymentResult.response_code }}</span>
              </div>
              <div class="flex justify-between items-center py-2">
                <span class="text-gray-600">Số tiền</span>
                <span class="font-bold text-gray-900">{{ format(paymentResult.amount) }}</span>
              </div>
            </div>
          </div>

          <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
            <p class="text-sm text-yellow-800">
              <strong>Gợi ý:</strong> Vui lòng kiểm tra lại thông tin thẻ, số dư tài khoản hoặc liên hệ ngân hàng để biết thêm chi tiết.
            </p>
          </div>

          <div class="flex flex-col sm:flex-row gap-3">
            <button 
              @click="retryPayment" 
              class="flex-1 bg-orange-500 text-white px-6 py-4 rounded-lg hover:bg-orange-600 transition-colors font-semibold text-lg"
            >
              Thử lại thanh toán
            </button>
            <button 
              @click="goToHome" 
              class="flex-1 bg-gray-200 text-gray-700 px-6 py-4 rounded-lg hover:bg-gray-300 transition-colors font-semibold text-lg"
            >
              Về trang chủ
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
