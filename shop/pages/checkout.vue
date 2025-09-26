<script setup lang="ts">
import { reactive, ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { storeToRefs } from 'pinia';
import { useCheckoutStore } from '~/stores/checkout';
import { useCartStore } from '~/stores/cart';
import { useCurrency } from '~/composables/useCurrency'; 

// --- KHỞI TẠO ---
const checkoutStore = useCheckoutStore();
const cartStore = useCartStore();
const router = useRouter();
const { format } = useCurrency();

// Lấy dữ liệu từ checkoutStore
const { items: checkoutItems, total: subtotal, count: checkoutCount } = storeToRefs(checkoutStore);

// --- STATE ---
const address = reactive({
  line1: '',
  province_id: '',
  district_id: '',
  ward_id: '',
});
const voucherCode = ref('');
const discount = ref(0);
const voucherError = ref('');
const loading = ref(false);
const err = ref('');

// --- GIÁ TRỊ TÍNH TOÁN ---
const tax = computed(() => subtotal.value * 0.08);
const finalTotal = computed(() => {
  const total = subtotal.value + tax.value - discount.value;
  return total > 0 ? total : 0; 
});

// --- HÀM XỬ LÝ ---
function applyVoucher() {
  voucherError.value = '';
  discount.value = 0;

  if (!voucherCode.value) return;

  if (voucherCode.value === 'SALE50') {
    discount.value = 50000; // giảm trực tiếp 50k
  } else if (voucherCode.value === 'SALE10P') {
    discount.value = subtotal.value * 0.1; // giảm 10%
  } else {
    voucherError.value = 'Mã giảm giá không hợp lệ.';
  }
}

async function placeOrder() {
  loading.value = true;
  err.value = '';
  try {
    const orderPayload = {
      items: checkoutItems.value.map(item => ({ 
        product_id: item.productId, 
        quantity: item.qty, 
        price: item.price 
      })),
      shipping_address: address,
      voucher_code: voucherCode.value,
      final_total: finalTotal.value,
    };
    console.log('Đang gửi đơn hàng:', orderPayload);

    await new Promise(r => setTimeout(r, 1000));
    alert('Thanh toán thành công!');

    const purchasedItemIds = checkoutItems.value.map(item => item.productId);
    purchasedItemIds.forEach(id => cartStore.remove(id));
    checkoutStore.clear();

    router.push(`/thanks`);
  } catch (e: any) {
    err.value = e?.data?.detail || 'Thanh toán thất bại, vui lòng thử lại.';
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold text-gray-900 mb-8">Checkout</h1>
    
    <div v-if="checkoutCount === 0" class="text-center py-12">
      <h2 class="text-xl font-semibold text-gray-700 mb-2">Không có sản phẩm nào để thanh toán</h2>
      <NuxtLink to="/cart" class="text-orange-600 hover:underline">Quay lại giỏ hàng</NuxtLink>
    </div>

    <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Cột trái -->
      <section class="lg:col-span-2 space-y-8">
        <!-- Thông tin giao hàng -->
        <div>
          <h2 class="text-xl font-semibold mb-4">Thông tin giao hàng</h2>
          <div class="space-y-4 bg-white p-6 rounded-lg border">
            <input v-model="address.line1" placeholder="Địa chỉ, số nhà, tên đường" class="border rounded w-full p-3" />
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <input v-model="address.province_id" placeholder="Tỉnh/Thành phố" class="border rounded p-3" />
              <input v-model="address.district_id" placeholder="Quận/Huyện" class="border rounded p-3" />
              <input v-model="address.ward_id" placeholder="Phường/Xã" class="border rounded p-3" />
            </div>
          </div>
        </div>

        <!-- Danh sách sản phẩm -->
        <div>
          <h2 class="text-xl font-semibold mb-4">Sản phẩm thanh toán</h2>
          <div class="bg-white rounded-lg border divide-y">
            <div v-for="item in checkoutItems" :key="item.productId" class="flex items-center space-x-4 p-4">
              <img :src="'/placeholder-product.jpg'" :alt="item.name" class="w-16 h-16 object-cover rounded-md" />
              <div class="flex-grow">
                <p class="font-medium">{{ item.name }}</p>
                <p class="text-sm text-gray-500">Số lượng: {{ item.qty }}</p>
              </div>
              <div class="font-semibold">{{ format(item.price * item.qty) }}</div>
            </div>
          </div>
        </div>
      </section>

      <!-- Cột phải -->
      <aside class="lg:col-span-1">
        <div class="bg-white rounded-lg border p-6 space-y-4 sticky top-4">
          <h2 class="text-xl font-semibold text-center mb-2">Tóm tắt đơn hàng</h2>
          
          <!-- Chọn voucher -->
          <div>
            <label for="voucher" class="block text-sm font-medium text-gray-700">Chọn Voucher</label>
            <select v-model="voucherCode" @change="applyVoucher"
                    class="mt-1 block w-full border-gray-300 rounded-md p-2">
              <option value="">-- Chọn voucher --</option>
              <option value="SALE50">Giảm 50,000đ</option>
              <option value="SALE10P">Giảm 10%</option>
            </select>
            <p v-if="voucherError" class="text-red-500 text-sm mt-1">{{ voucherError }}</p>
          </div>
          
          <!-- Chi tiết giá -->
          <div class="space-y-2 border-t pt-4">
            <div class="flex justify-between text-gray-600">
              <span>Tạm tính</span>
              <span>{{ format(subtotal) }}</span>
            </div>
            <div class="flex justify-between text-gray-600">
              <span>Thuế (8%)</span>
              <span>{{ format(tax) }}</span>
            </div>
            <div v-if="discount > 0" class="flex justify-between text-green-600">
              <span>Giảm giá</span>
              <span>- {{ format(discount) }}</span>
            </div>
            <div class="flex justify-between text-xl font-bold border-t pt-2 mt-2">
              <span>Tổng cộng</span>
              <span>{{ format(finalTotal) }}</span>
            </div>
          </div>

          <p v-if="err" class="text-red-600 text-sm text-center">{{ err }}</p>
          
          <!-- Nút thanh toán -->
          <button :disabled="loading" @click="placeOrder" class="mt-4 w-full bg-orange-500 hover:bg-orange-600 text-white py-3 rounded-lg font-semibold text-lg disabled:opacity-50">
            {{ loading ? 'Đang xử lý...' : 'Thanh Toán' }}
          </button>
        </div>
      </aside>
    </div>
  </div>
</template>
