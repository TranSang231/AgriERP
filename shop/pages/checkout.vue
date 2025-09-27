<script setup lang="ts">
import { reactive, ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { storeToRefs } from 'pinia';
import { useCheckoutStore } from '~/stores/checkout';
import { useCartStore } from '~/stores/cart';
import { useCurrency } from '~/composables/useCurrency'; 
import { usePromotionService } from '~/services/promotions';
import { useOrderService } from '~/services/orders'; 

// --- KHỞI TẠO ---
const checkoutStore = useCheckoutStore();
const cartStore = useCartStore();
const router = useRouter();
const { format } = useCurrency();
const { getActivePromotions, validatePromotion } = usePromotionService();
const { createOrder } = useOrderService();

// Lấy dữ liệu từ checkoutStore
const { items: checkoutItems, total: subtotal, count: checkoutCount } = storeToRefs(checkoutStore);

// --- STATE ---
const address = reactive({
  line1: '',
  province_id: '',
  district_id: '',
  ward_id: '',
});
const paymentMethod = ref('bank_transfer'); // 'bank_transfer' or 'cash_on_delivery'
const voucherCode = ref('');
const discount = ref(0);
const voucherError = ref('');
const loading = ref(false);
const err = ref('');
const transferConfirmed = ref(false); // Xác nhận đã chuyển khoản

// Promotion state
const availablePromotions = ref([]);
const selectedPromotion = ref(null);
const promotionLoading = ref(false);

// Customer information
const customerInfo = reactive({
  customer_name: '',
  company_name: '',
  tax_code: '',
  account_number: '',
});

// Order details
const orderDetails = reactive({
  vat_rate: 8.0, // 8% VAT
  shipping_fee: 0.0,
});

// --- VIETNAM PROVINCE API ---
const provinces = ref([]);
const districts = ref([]);
const wards = ref([]);
const loadingProvinces = ref(false);
const loadingDistricts = ref(false);
const loadingWards = ref(false);

// Load provinces and promotions on mount
onMounted(async () => {
  await loadProvinces();
  await loadActivePromotions();
});

async function loadProvinces() {
  loadingProvinces.value = true;
  try {
    const response = await fetch('https://provinces.open-api.vn/api/');
    provinces.value = await response.json();
  } catch (error) {
    console.error('Error loading provinces:', error);
  } finally {
    loadingProvinces.value = false;
  }
}

async function loadDistricts(provinceCode) {
  if (!provinceCode) {
    districts.value = [];
    wards.value = [];
    address.district_id = '';
    address.ward_id = '';
    return;
  }
  
  loadingDistricts.value = true;
  try {
    const response = await fetch(`https://provinces.open-api.vn/api/p/${provinceCode}?depth=2`);
    const data = await response.json();
    districts.value = data.districts || [];
    wards.value = [];
    address.district_id = '';
    address.ward_id = '';
  } catch (error) {
    console.error('Error loading districts:', error);
  } finally {
    loadingDistricts.value = false;
  }
}

async function loadWards(districtCode) {
  if (!districtCode) {
    wards.value = [];
    address.ward_id = '';
    return;
  }
  
  loadingWards.value = true;
  try {
    const response = await fetch(`https://provinces.open-api.vn/api/d/${districtCode}?depth=2`);
    const data = await response.json();
    wards.value = data.wards || [];
    address.ward_id = '';
  } catch (error) {
    console.error('Error loading wards:', error);
  } finally {
    loadingWards.value = false;
  }
}

// --- PROMOTION FUNCTIONS ---
async function loadActivePromotions() {
  promotionLoading.value = true;
  try {
    const { data, error } = await getActivePromotions();
    if (!error?.value && data?.value) {
      availablePromotions.value = data.value;
    }
  } catch (error) {
    console.error('Error loading promotions:', error);
  } finally {
    promotionLoading.value = false;
  }
}

async function applyPromotion(promotionId) {
  if (!promotionId) {
    discount.value = 0;
    selectedPromotion.value = null;
    voucherError.value = '';
    return;
  }

  try {
    const productIds = checkoutItems.value.map(item => item.productId);
    const quantities = checkoutItems.value.map(item => item.qty);
    
    const { data, error } = await validatePromotion(promotionId, productIds, quantities);
    
    if (!error?.value && data?.value) {
      if (data.value.valid) {
        // Backend đã trả về số tiền giảm thực tế
        discount.value = data.value.discount || 0;
        selectedPromotion.value = availablePromotions.value.find(p => p.id === promotionId);
        voucherError.value = '';
      } else {
        voucherError.value = data.value.message || 'Mã giảm giá không áp dụng được cho sản phẩm này.';
        discount.value = 0;
        selectedPromotion.value = null;
      }
    }
  } catch (error) {
    voucherError.value = 'Lỗi khi áp dụng mã giảm giá.';
    discount.value = 0;
    selectedPromotion.value = null;
  }
}

// --- GIÁ TRỊ TÍNH TOÁN ---
const tax = computed(() => subtotal.value * 0.08);
const finalTotal = computed(() => {
  const total = subtotal.value + tax.value - discount.value;
  return total > 0 ? total : 0; 
});

// --- VALIDATION ---
const showValidation = ref(false); // Chỉ hiển thị validation sau khi user nhấn submit

const validationErrors = computed(() => {
  const errors = [];
  
  if (!customerInfo.customer_name?.trim()) {
    errors.push('Tên khách hàng là bắt buộc');
  }
  
  if (!address.line1?.trim()) {
    errors.push('Địa chỉ chi tiết là bắt buộc');
  }
  
  if (!address.province_id) {
    errors.push('Tỉnh/Thành phố là bắt buộc');
  }
  
  if (!address.district_id) {
    errors.push('Quận/Huyện là bắt buộc');
  }
  
  if (!address.ward_id) {
    errors.push('Phường/Xã là bắt buộc');
  }
  
  // Nếu chọn chuyển khoản thì cần xác nhận đã chuyển
  if (paymentMethod.value === 'bank_transfer' && !transferConfirmed.value) {
    errors.push('Vui lòng xác nhận đã chuyển khoản');
  }
  
  return errors;
});

const isFormValid = computed(() => validationErrors.value.length === 0);

// --- HÀM XỬ LÝ ---
// Reset checkbox khi chuyển đổi phương thức thanh toán
watch(paymentMethod, (newMethod) => {
  if (newMethod !== 'bank_transfer') {
    transferConfirmed.value = false;
  }
});

function applyVoucher() {
  voucherError.value = '';
  discount.value = 0;

  if (!voucherCode.value) {
    selectedPromotion.value = null;
    return;
  }

  // Find promotion by name (assuming voucherCode is promotion name)
  const promotion = availablePromotions.value.find(p => p.name === voucherCode.value);
  if (promotion) {
    applyPromotion(promotion.id);
  } else {
    voucherError.value = 'Mã giảm giá không tồn tại hoặc đã hết hạn.';
    selectedPromotion.value = null;
  }
}

// Helper function to map payment method
function mapPaymentMethod(method: string): number {
  return method === 'bank_transfer' ? 0 : 1; // 0 = BANK_TRANSFER, 1 = CASH_ON_DELIVERY
}

async function placeOrder() {
  // Bật validation mode để hiển thị lỗi
  showValidation.value = true;
  
  // Kiểm tra validation trước khi xử lý
  if (!isFormValid.value) {
    err.value = 'Vui lòng điền đầy đủ thông tin bắt buộc';
    return;
  }
  
  loading.value = true;
  err.value = '';
  try {
    // Chuẩn bị dữ liệu đơn hàng theo cấu trúc backend
    const orderData = {
      customer_name: customerInfo.customer_name,
      company_name: customerInfo.company_name || '',
      tax_code: customerInfo.tax_code || '',
      payment_method: mapPaymentMethod(paymentMethod.value),
      account_number: customerInfo.account_number || '',
      vat_rate: orderDetails.vat_rate,
      shipping_fee: orderDetails.shipping_fee,
      date: new Date().toISOString().split('T')[0],
      items: checkoutItems.value.map(item => ({
        product_id: item.productId,
        product_name: item.name,
        unit: 'Cái', // Default unit
        quantity: item.qty,
        price: item.price,
        amount: item.price * item.qty
      }))
    };

    console.log('Đang tạo đơn hàng:', orderData);

    // Gọi API tạo đơn hàng
    const { data, error } = await createOrder(orderData);
    
    if (error?.value) {
      throw error.value;
    }

    if (data?.value) {
      console.log('Đơn hàng đã được tạo:', data.value);
      
      // Xóa sản phẩm khỏi giỏ hàng
      const purchasedItemIds = checkoutItems.value.map(item => item.productId);
      purchasedItemIds.forEach(id => cartStore.remove(id));
      checkoutStore.clear();

      // Chuyển hướng đến trang cảm ơn
      router.push(`/thanks?order_id=${data.value.id}`);
    } else {
      throw new Error('Không nhận được phản hồi từ server');
    }
    
  } catch (e: any) {
    console.error('Lỗi khi tạo đơn hàng:', e);
    err.value = e?.message || e?.data?.detail || 'Đặt hàng thất bại, vui lòng thử lại.';
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
        <!-- Thông tin khách hàng -->
        <div>
          <h2 class="text-xl font-semibold mb-4">Thông tin khách hàng</h2>
          <div class="bg-white p-6 rounded-lg border">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Tên khách hàng *</label>
                <input 
                  v-model="customerInfo.customer_name" 
                  placeholder="Nhập tên khách hàng" 
                  :class="[
                    'border rounded w-full p-3',
                    showValidation && !customerInfo.customer_name?.trim() ? 'border-red-500 focus:border-red-500' : 'border-gray-300 focus:border-orange-500'
                  ]"
                  required
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Tên công ty</label>
                <input 
                  v-model="customerInfo.company_name" 
                  placeholder="Nhập tên công ty (nếu có)" 
                  class="border rounded w-full p-3"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Mã số thuế</label>
                <input 
                  v-model="customerInfo.tax_code" 
                  placeholder="Nhập mã số thuế (nếu có)" 
                  class="border rounded w-full p-3"
                />
              </div>
            </div>
          </div>
        </div>

        <!-- Thông tin giao hàng -->
        <div>
          <h2 class="text-xl font-semibold mb-4">Thông tin giao hàng</h2>
          <div class="space-y-4 bg-white p-6 rounded-lg border">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Địa chỉ chi tiết</label>
              <input 
                v-model="address.line1" 
                placeholder="Số nhà, tên đường, tòa nhà..." 
                  :class="[
                    'border rounded w-full p-3',
                    showValidation && !address.line1?.trim() ? 'border-red-500 focus:border-red-500' : 'border-gray-300 focus:border-orange-500'
                  ]"
                required
              />
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Tỉnh/Thành phố</label>
                <select 
                  v-model="address.province_id" 
                  @change="loadDistricts(address.province_id)"
                  :class="[
                    'border rounded w-full p-3',
                    showValidation && !address.province_id ? 'border-red-500 focus:border-red-500' : 'border-gray-300 focus:border-orange-500'
                  ]"
                  :disabled="loadingProvinces"
                  required
                >
                  <option value="">-- Chọn tỉnh/thành phố --</option>
                  <option v-for="province in provinces" :key="province.code" :value="province.code">
                    {{ province.name }}
                  </option>
                </select>
                <div v-if="loadingProvinces" class="text-sm text-gray-500 mt-1">Đang tải...</div>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Quận/Huyện</label>
                <select 
                  v-model="address.district_id" 
                  @change="loadWards(address.district_id)"
                  :class="[
                    'border rounded w-full p-3',
                    showValidation && !address.district_id ? 'border-red-500 focus:border-red-500' : 'border-gray-300 focus:border-orange-500'
                  ]"
                  :disabled="!address.province_id || loadingDistricts"
                  required
                >
                  <option value="">-- Chọn quận/huyện --</option>
                  <option v-for="district in districts" :key="district.code" :value="district.code">
                    {{ district.name }}
                  </option>
                </select>
                <div v-if="loadingDistricts" class="text-sm text-gray-500 mt-1">Đang tải...</div>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">Phường/Xã</label>
                <select 
                  v-model="address.ward_id" 
                  :class="[
                    'border rounded w-full p-3',
                    showValidation && !address.ward_id ? 'border-red-500 focus:border-red-500' : 'border-gray-300 focus:border-orange-500'
                  ]"
                  :disabled="!address.district_id || loadingWards"
                  required
                >
                  <option value="">-- Chọn phường/xã --</option>
                  <option v-for="ward in wards" :key="ward.code" :value="ward.code">
                    {{ ward.name }}
                  </option>
                </select>
                <div v-if="loadingWards" class="text-sm text-gray-500 mt-1">Đang tải...</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Phương thức thanh toán -->
        <div>
          <h2 class="text-xl font-semibold mb-4">Phương thức thanh toán</h2>
          <div class="bg-white p-6 rounded-lg border">
            <div class="space-y-4">
              <label class="flex items-center space-x-3 cursor-pointer">
                <input 
                  type="radio" 
                  v-model="paymentMethod" 
                  value="bank_transfer" 
                  class="h-4 w-4 text-orange-600 focus:ring-orange-500"
                />
                <div>
                  <div class="font-medium">Chuyển khoản ngân hàng</div>
                  <div class="text-sm text-gray-500">Quét QR code để thanh toán</div>
                </div>
              </label>
              
              <label class="flex items-center space-x-3 cursor-pointer">
                <input 
                  type="radio" 
                  v-model="paymentMethod" 
                  value="cash_on_delivery" 
                  class="h-4 w-4 text-orange-600 focus:ring-orange-500"
                />
                <div>
                  <div class="font-medium">Thanh toán khi nhận hàng (COD)</div>
                  <div class="text-sm text-gray-500">Thanh toán bằng tiền mặt khi nhận hàng</div>
                </div>
              </label>
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

        <!-- QR Code cho chuyển khoản -->
        <div v-if="paymentMethod === 'bank_transfer'" class="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 class="text-lg font-semibold text-blue-900 mb-4">Thông tin chuyển khoản</h3>
          <div class="text-center">
            <div class="bg-white p-4 rounded-lg border-2 border-dashed border-blue-300 mb-4">
              <div class="text-gray-500 text-sm mb-2">QR Code sẽ hiển thị ở đây</div>
              <div class="w-48 h-48 bg-gray-100 mx-auto rounded-lg flex items-center justify-center">
                <div class="text-gray-400 text-sm">QR Code</div>
              </div>
            </div>
            <div class="text-sm text-gray-600 mb-4">
              <p class="mb-2">Quét QR code bằng ứng dụng ngân hàng để thanh toán</p>
              <p class="font-medium">Số tiền: {{ format(finalTotal) }}</p>
            </div>
            
            <!-- Checkbox xác nhận chuyển khoản -->
            <div class="bg-white p-4 rounded-lg border border-blue-300">
              <label class="flex items-center justify-center space-x-3 cursor-pointer">
                <input 
                  type="checkbox" 
                  v-model="transferConfirmed"
                  :class="[
                    'h-5 w-5 rounded border-2',
                    showValidation && !transferConfirmed ? 'border-red-500' : 'border-blue-500 text-blue-600 focus:ring-blue-500'
                  ]"
                />
                <span class="text-sm font-medium text-gray-700">
                  Tôi đã chuyển khoản thành công
                </span>
              </label>
              <p class="text-xs text-gray-500 mt-2">
                Đơn hàng sẽ được xử lý sau khi admin xác nhận giao dịch
              </p>
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
            <select 
              v-model="voucherCode" 
              @change="applyVoucher"
              class="mt-1 block w-full border-gray-300 rounded-md p-2"
              :disabled="promotionLoading"
            >
              <option value="">-- Chọn voucher --</option>
              <option 
                v-for="promotion in availablePromotions" 
                :key="promotion.id" 
                :value="promotion.name"
              >
                {{ promotion.name }} ({{ new Date(promotion.start).toLocaleDateString() }} - {{ new Date(promotion.end).toLocaleDateString() }})
              </option>
            </select>
            <div v-if="promotionLoading" class="text-sm text-gray-500 mt-1">Đang tải voucher...</div>
            <p v-if="voucherError" class="text-red-500 text-sm mt-1">{{ voucherError }}</p>
            <p v-if="selectedPromotion" class="text-green-600 text-sm mt-1">
              ✅ Đã áp dụng: {{ selectedPromotion.name }}
            </p>
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

          <p v-if="err" class="text-red-600 text-sm text-center mb-4">{{ err }}</p>
          
          <!-- Nút thanh toán -->
          <button 
            :disabled="loading" 
            @click="placeOrder" 
            class="mt-4 w-full bg-orange-500 hover:bg-orange-600 text-white py-3 rounded-lg font-semibold text-lg disabled:opacity-50"
          >
            {{ loading ? 'Đang xử lý...' : 'Đặt hàng' }}
          </button>
        </div>
      </aside>
    </div>
  </div>
</template>
