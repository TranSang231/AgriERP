<script setup lang="ts">
import { reactive, ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { storeToRefs } from 'pinia';
import { useI18n } from 'vue-i18n';
import { useCheckoutStore } from '~/stores/checkout';
import { useCartStore } from '~/stores/cart';
import { useCurrency } from '~/composables/useCurrency'; 
import { usePromotionService } from '~/services/promotions';
import { useOrderService } from '~/services/orders'; 
import { useAuthStore } from '~/stores/auth';
import { useCustomersService } from '~/services/customers';
import { useVNPayService } from '~/services/vnpayService';

// --- KHỞI TẠO ---
const checkoutStore = useCheckoutStore();
const cartStore = useCartStore();
const router = useRouter();
const { t } = useI18n();
const { format } = useCurrency();
const { getActivePromotions, validatePromotion } = usePromotionService();
const { createOrder } = useOrderService();
const auth = useAuthStore();
const { getProfile } = useCustomersService();
const { createPayment: createVNPayPayment, getSupportedBanks } = useVNPayService();

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
const selectedBank = ref(''); // VNPay bank code
const voucherCode = ref('');
const discount = ref(0);
const voucherError = ref('');
const loading = ref(false);
const err = ref('');
const supportedBanks = getSupportedBanks();

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

// --- SEO ---
useHead({
  title: t('checkout.meta.title'),
  meta: [{ name: 'description', content: t('checkout.meta.description') }]
});

// Load provinces, customer info and promotions on mount
onMounted(async () => {
  await loadProvinces();
  await loadCustomerProfileIntoCheckout();
  await loadActivePromotions();
});

async function loadCustomerProfileIntoCheckout() {
  try {
    // Prefer auth store first for speed
    let customer: any = auth.user || null;
    if (!customer) {
      const data = await getProfile();
      customer = (data as any)?.customer || null;
    }
    if (!customer) return;

    // Fill customer name
    const first = (customer.first_name || '').trim();
    const last = (customer.last_name || '').trim();
    customerInfo.customer_name = [first, last].filter(Boolean).join(' ');

    // Fill address line
    address.line1 = customer.address || '';

    // Fill province/district/ward with dependent loading
    const prov = customer.province_id ? String(customer.province_id) : '';
    const dist = customer.district_id ? String(customer.district_id) : '';
    const ward = customer.ward_id ? String(customer.ward_id) : '';

    if (prov) {
      address.province_id = prov;
      await loadDistricts(prov);
      if (dist) {
        address.district_id = dist;
        await loadWards(dist);
        if (ward) {
          address.ward_id = ward;
        }
      }
    }
  } catch (e) {
    // Silent fallback if cannot load
    console.error("Failed to auto-fill customer profile:", e);
  }
}

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
    const data = await getActivePromotions();
    if (data) {
      // Only show voucher-type promotions at checkout
      availablePromotions.value = (data || []).filter((p: any) => (p?.type || '').toLowerCase() === 'voucher');
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
    
    // validatePromotion uses POST, so it returns direct data (not {data, error} object)
    const result = await validatePromotion(promotionId, productIds, quantities);
    
    if (result && result.valid) {
      // Backend đã trả về số tiền giảm thực tế
      discount.value = result.discount || 0;
      selectedPromotion.value = availablePromotions.value.find(p => p.id === promotionId);
      voucherError.value = '';
    } else {
      voucherError.value = result?.message || t('checkout.errors.invalidVoucher');
      discount.value = 0;
      selectedPromotion.value = null;
    }
  } catch (error) {
    voucherError.value = t('checkout.errors.applyVoucherFailed');
    discount.value = 0;
    selectedPromotion.value = null;
  }
}

// --- GIÁ TRỊ TÍNH TOÁN ---
// Thuế được tính sau khi đã trừ giảm giá (voucher/discount)
const taxableBase = computed(() => {
  const base = subtotal.value - discount.value;
  return base > 0 ? base : 0;
});
const tax = computed(() => taxableBase.value * 0.08);
const finalTotal = computed(() => {
  const total = taxableBase.value + tax.value;
  return total > 0 ? total : 0;
});

// --- VALIDATION ---
const showValidation = ref(false); // Chỉ hiển thị validation sau khi user nhấn submit

const validationErrors = computed(() => {
  const errors = [];
  if (!customerInfo.customer_name?.trim()) errors.push(t('checkout.errors.validation.nameRequired'));
  if (!address.line1?.trim()) errors.push(t('checkout.errors.validation.addressRequired'));
  if (!address.province_id) errors.push(t('checkout.errors.validation.provinceRequired'));
  if (!address.district_id) errors.push(t('checkout.errors.validation.districtRequired'));
  if (!address.ward_id) errors.push(t('checkout.errors.validation.wardRequired'));
  return errors;
});

const isFormValid = computed(() => validationErrors.value.length === 0);

// --- HÀM XỬ LÝ ---
// Clear bank selection when payment method changes
watch(paymentMethod, (newMethod) => {
  if (newMethod !== 'bank_transfer') {
    selectedBank.value = '';
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
  const promotion = availablePromotions.value.find((p: any) => (p?.type || '').toLowerCase() === 'voucher' && p.name === voucherCode.value);
  if (promotion) {
    applyPromotion(promotion.id);
  } else {
    voucherError.value = t('checkout.errors.voucherNotFound');
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
    err.value = t('checkout.errors.fillRequiredFields');
    return;
  }
  
  loading.value = true;
  err.value = '';
  try {
    // Chuẩn bị dữ liệu đơn hàng theo cấu trúc backend
    const orderData = {
      customer_id: (auth.user as any)?.id || undefined,
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

    // Gọi API tạo đơn hàng - POST uses $fetch, returns data directly
    const data = await createOrder(orderData as any);
    
    if (data) {
      console.log('Đơn hàng đã được tạo:', data);
      
      // Kiểm tra phương thức thanh toán
      if (paymentMethod.value === 'bank_transfer') {
        // Thanh toán qua VNPay
        try {
          console.log('Tạo link thanh toán VNPay cho đơn hàng:', data.id);
          
          const paymentRequest = {
            order_id: data.id,
            bank_code: selectedBank.value || undefined,
            language: 'vn' as 'vn' | 'en'
          };
          
          const paymentResult = await createVNPayPayment(paymentRequest);
          
          if (paymentResult && paymentResult.payment_url) {
            console.log('Chuyển hướng đến VNPay:', paymentResult.payment_url);
            
            // Xóa sản phẩm khỏi giỏ hàng trước khi chuyển sang VNPay
            const purchasedItemIds = checkoutItems.value.map(item => item.productId);
            purchasedItemIds.forEach(id => cartStore.remove(id));
            checkoutStore.clear();
            
            // Chuyển hướng sang trang thanh toán VNPay
            window.location.href = paymentResult.payment_url;
            return; // Dừng lại để chờ redirect
          } else {
            throw new Error('Không thể tạo link thanh toán VNPay');
          }
        } catch (vnpayError: any) {
          console.error('Lỗi tạo thanh toán VNPay:', vnpayError);
          throw new Error(`VNPay: ${vnpayError?.message || 'Lỗi không xác định'}`);
        }
      } else {
        // Thanh toán COD - flow cũ
        // Xóa sản phẩm khỏi giỏ hàng
        const purchasedItemIds = checkoutItems.value.map(item => item.productId);
        purchasedItemIds.forEach(id => cartStore.remove(id));
        checkoutStore.clear();

        // Chuyển hướng đến trang cảm ơn
        router.push(`/thanks?order_id=${data.id}`);
      }
    } else {
      throw new Error(t('checkout.errors.noServerResponse'));
    }
    
  } catch (e: any) {
    console.error('Lỗi khi tạo đơn hàng:', e);
    err.value = e?.message || e?.data?.detail || t('checkout.errors.orderFailed');
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold text-gray-900 mb-8">{{ $t('checkout.title') }}</h1>
    
    <div v-if="checkoutCount === 0" class="text-center py-12">
      <h2 class="text-xl font-semibold text-gray-700 mb-2">{{ $t('checkout.empty.title') }}</h2>
      <NuxtLink to="/cart" class="text-orange-600 hover:underline">{{ $t('checkout.empty.backToCart') }}</NuxtLink>
    </div>

    <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Cột trái -->
      <section class="lg:col-span-2 space-y-8">
        <!-- Thông tin khách hàng -->
        <div>
          <h2 class="text-xl font-semibold mb-4">{{ $t('checkout.customerInfo.title') }}</h2>
          <div class="bg-white p-6 rounded-lg border">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">{{ $t('checkout.customerInfo.nameLabel') }}</label>
                <input 
                  v-model="customerInfo.customer_name" 
                  :placeholder="$t('checkout.customerInfo.namePlaceholder')" 
                  :class="['border rounded w-full p-3', showValidation && !customerInfo.customer_name?.trim() ? 'border-red-500 focus:border-red-500' : 'border-gray-300 focus:border-orange-500']"
                  required
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">{{ $t('checkout.customerInfo.companyLabel') }}</label>
                <input 
                  v-model="customerInfo.company_name" 
                  :placeholder="$t('checkout.customerInfo.companyPlaceholder')" 
                  class="border rounded w-full p-3"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">{{ $t('checkout.customerInfo.taxCodeLabel') }}</label>
                <input 
                  v-model="customerInfo.tax_code" 
                  :placeholder="$t('checkout.customerInfo.taxCodePlaceholder')" 
                  class="border rounded w-full p-3"
                />
              </div>
            </div>
          </div>
        </div>

        <!-- Thông tin giao hàng -->
        <div>
          <h2 class="text-xl font-semibold mb-4">{{ $t('checkout.shippingInfo.title') }}</h2>
          <div class="space-y-4 bg-white p-6 rounded-lg border">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">{{ $t('checkout.shippingInfo.addressLabel') }}</label>
              <input 
                v-model="address.line1" 
                :placeholder="$t('checkout.shippingInfo.addressPlaceholder')" 
                :class="['border rounded w-full p-3', showValidation && !address.line1?.trim() ? 'border-red-500 focus:border-red-500' : 'border-gray-300 focus:border-orange-500']"
                required
              />
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">{{ $t('checkout.shippingInfo.provinceLabel') }}</label>
                <select 
                  v-model="address.province_id" 
                  @change="loadDistricts(address.province_id)"
                  :class="['border rounded w-full p-3', showValidation && !address.province_id ? 'border-red-500 focus:border-red-500' : 'border-gray-300 focus:border-orange-500']"
                  :disabled="loadingProvinces"
                  required
                >
                  <option value="">{{ $t('checkout.shippingInfo.provincePlaceholder') }}</option>
                  <option v-for="province in provinces" :key="province.code" :value="province.code">{{ province.name }}</option>
                </select>
                <div v-if="loadingProvinces" class="text-sm text-gray-500 mt-1">{{ $t('checkout.shippingInfo.loading') }}</div>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">{{ $t('checkout.shippingInfo.districtLabel') }}</label>
                <select 
                  v-model="address.district_id" 
                  @change="loadWards(address.district_id)"
                  :class="['border rounded w-full p-3', showValidation && !address.district_id ? 'border-red-500 focus:border-red-500' : 'border-gray-300 focus:border-orange-500']"
                  :disabled="!address.province_id || loadingDistricts"
                  required
                >
                  <option value="">{{ $t('checkout.shippingInfo.districtPlaceholder') }}</option>
                  <option v-for="district in districts" :key="district.code" :value="district.code">{{ district.name }}</option>
                </select>
                <div v-if="loadingDistricts" class="text-sm text-gray-500 mt-1">{{ $t('checkout.shippingInfo.loading') }}</div>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">{{ $t('checkout.shippingInfo.wardLabel') }}</label>
                <select 
                  v-model="address.ward_id" 
                  :class="['border rounded w-full p-3', showValidation && !address.ward_id ? 'border-red-500 focus:border-red-500' : 'border-gray-300 focus:border-orange-500']"
                  :disabled="!address.district_id || loadingWards"
                  required
                >
                  <option value="">{{ $t('checkout.shippingInfo.wardPlaceholder') }}</option>
                  <option v-for="ward in wards" :key="ward.code" :value="ward.code">{{ ward.name }}</option>
                </select>
                <div v-if="loadingWards" class="text-sm text-gray-500 mt-1">{{ $t('checkout.shippingInfo.loading') }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Phương thức thanh toán -->
        <div>
          <h2 class="text-xl font-semibold mb-4">{{ $t('checkout.payment.title') }}</h2>
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
                  <div class="font-medium">{{ $t('checkout.payment.bankTransfer') }}</div>
                  <div class="text-sm text-gray-500">{{ $t('checkout.payment.bankTransferDesc') }}</div>
                </div>
              </label>
              
              <!-- Bank Selection for VNPay -->
              <div v-if="paymentMethod === 'bank_transfer'" class="ml-7 mt-3 p-4 bg-blue-50 rounded-lg border border-blue-200">
                <label class="block mb-2 text-sm font-medium text-gray-700">
                  Chọn ngân hàng (tùy chọn)
                </label>
                <select 
                  v-model="selectedBank" 
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500"
                >
                  <option value="">-- Tất cả ngân hàng --</option>
                  <option v-for="bank in supportedBanks" :key="bank.code" :value="bank.code">
                    {{ bank.name }}
                  </option>
                </select>
                <p class="mt-2 text-xs text-gray-500">
                  Nếu không chọn, bạn có thể chọn ngân hàng trên trang VNPay
                </p>
              </div>
              
              <label class="flex items-center space-x-3 cursor-pointer">
                <input 
                  type="radio" 
                  v-model="paymentMethod" 
                  value="cash_on_delivery" 
                  class="h-4 w-4 text-orange-600 focus:ring-orange-500"
                />
                <div>
                  <div class="font-medium">{{ $t('checkout.payment.cod') }}</div>
                  <div class="text-sm text-gray-500">{{ $t('checkout.payment.codDesc') }}</div>
                </div>
              </label>
            </div>
          </div>
        </div>

        <!-- Danh sách sản phẩm -->
        <div>
          <h2 class="text-xl font-semibold mb-4">{{ $t('checkout.products.title') }}</h2>
          <div class="bg-white rounded-lg border divide-y">
            <div v-for="item in checkoutItems" :key="item.productId" class="flex items-center space-x-4 p-4">
              <img :src="item.image" :alt="item.name" class="w-16 h-16 object-cover rounded-md" />
              <div class="flex-grow">
                <p class="font-medium">{{ item.name }}</p>
                <p class="text-sm text-gray-500">{{ $t('checkout.products.quantity') }} {{ item.qty }}</p>
              </div>
              <div class="font-semibold">{{ format(item.price * item.qty) }}</div>
            </div>
          </div>
        </div>

        <!-- Thông tin thanh toán VNPay -->
        <div v-if="paymentMethod === 'bank_transfer'" class="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 class="text-lg font-semibold text-blue-900 mb-4">💳 Thanh toán qua VNPay</h3>
          <div class="text-sm text-gray-600 space-y-2">
            <p>✓ Thanh toán an toàn qua cổng VNPay</p>
            <p>✓ Hỗ trợ ATM nội địa, thẻ quốc tế Visa/Master</p>
            <p>✓ Bạn sẽ được chuyển sang trang VNPay để thanh toán</p>
            <p class="font-medium text-blue-900 mt-4">Số tiền thanh toán: {{ format(finalTotal) }}</p>
          </div>
        </div>
      </section>

      <!-- Cột phải -->
      <aside class="lg:col-span-1">
        <div class="bg-white rounded-lg border p-6 space-y-4 sticky top-4">
          <h2 class="text-xl font-semibold text-center mb-2">{{ $t('checkout.summary.title') }}</h2>
          
          <!-- Chọn voucher -->
          <div>
            <label for="voucher" class="block text-sm font-medium text-gray-700">{{ $t('checkout.summary.voucherLabel') }}</label>
            <select 
              v-model="voucherCode" 
              @change="applyVoucher"
              class="mt-1 block w-full border-gray-300 rounded-md p-2"
              :disabled="promotionLoading"
            >
              <option value="">{{ $t('checkout.summary.voucherPlaceholder') }}</option>
              <option 
                v-for="promotion in availablePromotions" 
                :key="promotion.id" 
                :value="promotion.name"
              >
                {{ promotion.name }} ({{ new Date(promotion.start).toLocaleDateString() }} - {{ new Date(promotion.end).toLocaleDateString() }})
              </option>
            </select>
            <div v-if="promotionLoading" class="text-sm text-gray-500 mt-1">{{ $t('checkout.summary.voucherLoading') }}</div>
            <p v-if="voucherError" class="text-red-500 text-sm mt-1">{{ voucherError }}</p>
            <p v-if="selectedPromotion" class="text-green-600 text-sm mt-1">
              {{ $t('checkout.summary.voucherApplied') }} {{ selectedPromotion.name }}
            </p>
          </div>
          
          <!-- Chi tiết giá -->
          <div class="space-y-2 border-t pt-4">
            <div class="flex justify-between text-gray-600">
              <span>{{ $t('checkout.summary.subtotal') }}</span>
              <span>{{ format(subtotal) }}</span>
            </div>
            <div class="flex justify-between text-gray-600">
              <span>{{ $t('checkout.summary.tax') }}</span>
              <span>{{ format(tax) }}</span>
            </div>
            <div v-if="discount > 0" class="flex justify-between text-green-600">
              <span>{{ $t('checkout.summary.discount') }}</span>
              <span>- {{ format(discount) }}</span>
            </div>
            <div class="flex justify-between text-xl font-bold border-t pt-2 mt-2">
              <span>{{ $t('checkout.summary.total') }}</span>
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
            {{ loading ? $t('checkout.actions.processing') : $t('checkout.actions.placeOrder') }}
          </button>
        </div>
      </aside>
    </div>
  </div>
</template>