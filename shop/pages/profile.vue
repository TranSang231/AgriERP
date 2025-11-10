<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="flex gap-8">
        <div class="w-64 flex-shrink-0">
          <div class="bg-white rounded-lg shadow-sm border border-gray-200">
            <div class="p-6 border-b border-gray-100">
              <div class="flex items-center space-x-3">
                <div class="w-10 h-10 bg-gradient-to-r from-green-500 to-emerald-500 rounded-full flex items-center justify-center">
                  <span class="text-white text-sm font-medium">{{ (profileForm.first_name || 'U')[0] }}</span>
                </div>
                <div>
                  <p class="text-sm font-semibold text-gray-900">{{ profileForm.first_name || t('profile.guest') }} {{ profileForm.last_name || '' }}</p>
                  <p class="text-xs text-gray-500">{{ profileForm.email || 'email@example.com' }}</p>
                </div>
              </div>
            </div>

            <nav class="p-2">
              <div class="space-y-1">
                <div class="px-3 py-2">
                  <p class="text-xs font-semibold text-gray-500 uppercase tracking-wider">{{ t('profile.sidebar.navTitle') }}</p>
                </div>
                
                <a href="/" class="flex items-center px-3 py-2 text-sm font-medium text-green-600 bg-green-50 rounded-md group">
                  <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z"></path></svg>
                  {{ t('profile.sidebar.home') }}
                </a>
                
                <a href="/products" class="flex items-center px-3 py-2 text-sm font-medium text-gray-600 rounded-md hover:text-gray-900 hover:bg-gray-50 group">
                  <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M12 11V7"></path></svg>
                  {{ t('profile.sidebar.products') }}
                </a>

                <a href="/cart" class="flex items-center px-3 py-2 text-sm font-medium text-gray-600 rounded-md hover:text-gray-900 hover:bg-gray-50 group">
                  <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-2.5 5M7 13l2.5 5m6-5v6a2 2 0 01-2 2H9a2 2 0 01-2-2v-6m8 0V9a2 2 0 00-2-2H9a2 2 0 00-2 2v4.01"></path></svg>
                  {{ t('profile.sidebar.cart') }}
                </a>
              </div>
            </nav>
          </div>
        </div>

        <div class="flex-1">
          <div class="bg-white rounded-lg shadow-sm border border-gray-200">
            <div class="px-6 py-4 border-b border-gray-100">
              <div class="flex items-center justify-between">
                <div>
                  <h1 class="text-xl font-semibold text-gray-900">{{ t('profile.header.title') }}</h1>
                  <p class="text-sm text-gray-500 mt-1">{{ t('profile.header.subtitle') }}</p>
                </div>
                <div class="flex items-center space-x-3">
                  <span class="text-sm text-gray-500">{{ t('profile.header.settings') }}</span>
                </div>
              </div>
            </div>

            <div class="p-6">
              <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <div class="lg:col-span-1">
                  <div class="text-center">
                    <div class="relative inline-block">
                      <div class="w-48 h-48 bg-gradient-to-br from-orange-200 via-pink-200 to-orange-300 rounded-lg overflow-hidden shadow-lg flex items-center justify-center">
                        <div v-if="!profileForm.avatar" class="text-6xl font-bold text-orange-600">{{ (profileForm.first_name || 'U')[0] }}</div>
                        <img v-if="profileForm.avatar" :src="profileForm.avatar" alt="Profile" class="w-full h-full object-cover">
                      </div>
                      <button v-if="canUploadAvatar()" @click="toggleEdit('avatar')" class="absolute top-2 right-2 w-8 h-8 bg-white rounded-full shadow-lg flex items-center justify-center hover:bg-gray-50">
                        <svg class="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"></path></svg>
                      </button>
                    </div>
                    
                    <div class="mt-4">
                      <label v-if="editingField === 'avatar'" class="file-upload-label">
                        <input type="file" accept="image/*" @change="handleImageUpload">
                        {{ t('profile.avatar.upload') }}
                      </label>
                    </div>

                    <div class="mt-8 text-left">
                      <div v-if="!showPasswordForm && canChangePassword()">
                        <button @click="togglePasswordForm" class="w-full px-4 py-2 bg-green-600 text-white text-sm font-medium rounded-lg hover:bg-green-700 transition-colors flex items-center justify-center space-x-2">
                          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path></svg>
                          <span>{{ t('profile.password.changeButton') }}</span>
                        </button>
                      </div>

                      <div v-else class="space-y-4">
                        <div class="flex items-center justify-between mb-4">
                          <h4 class="text-sm font-semibold text-gray-700">{{ t('profile.password.title') }}</h4>
                          <button @click="togglePasswordForm" class="text-gray-400 hover:text-gray-600">
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
                          </button>
                        </div>
                        <div>
                          <label class="block text-sm font-medium text-gray-700 mb-2">{{ t('profile.password.currentLabel') }}</label>
                          <input v-model="passwordForm.current_password" type="password" autocomplete="current-password" :placeholder="t('profile.password.currentPlaceholder')" class="w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 text-sm">
                        </div>
                        <div>
                          <label class="block text-sm font-medium text-gray-700 mb-2">{{ t('profile.password.newLabel') }}</label>
                          <input v-model="passwordForm.new_password" type="password" autocomplete="new-password" :placeholder="t('profile.password.newPlaceholder')" class="w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 text-sm">
                        </div>
                        <div>
                          <label class="block text-sm font-medium text-gray-700 mb-2">{{ t('profile.password.confirmLabel') }}</label>
                          <input v-model="passwordForm.confirm_password" type="password" autocomplete="new-password" :placeholder="t('profile.password.confirmPlaceholder')" class="w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 text-sm">
                        </div>
                        <div class="flex space-x-3 pt-2">
                          <button @click="changePassword" :disabled="loading" class="flex-1 px-4 py-2 bg-green-600 text-white text-sm font-medium rounded-lg hover:bg-green-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed">
                            {{ loading ? t('profile.actions.processing') : t('profile.password.updateButton') }}
                          </button>
                          <button @click="cancelPasswordChange" type="button" class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors">
                            {{ t('profile.password.cancelButton') }}
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <div class="lg:col-span-2">
                  <div class="space-y-6">
                    <div>
                      <h3 class="text-lg font-medium text-gray-900 mb-4">{{ t('profile.info.title') }}</h3>
                      <form @submit.prevent="updateProfile" class="space-y-4">
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                          <div>
                            <div class="flex items-center justify-between mb-1"><label class="block text-sm font-medium text-gray-700">{{ t('profile.info.emailLabel') }}</label><button v-if="canEditProfile()" type="button" @click="toggleEdit('email')" class="p-1 text-gray-600 hover:text-green-600 hover:bg-green-50 rounded transition-colors"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"></path></svg></button></div>
                            <input v-model="profileForm.email" :disabled="editingField !== 'email'" type="email" placeholder="email@example.com" :class="['w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 text-sm', editingField === 'email' ? 'border-gray-200' : 'border-gray-200 bg-gray-50']">
                            <div v-if="editingField === 'email'" class="flex space-x-2 mt-2">
                              <button type="button" @click="saveField('email')" :disabled="loading" class="px-3 py-1 text-xs font-medium text-white bg-green-600 rounded hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed">{{ loading ? t('profile.actions.saving') : t('profile.actions.save') }}</button>
                              <button type="button" @click="cancelEdit" :disabled="loading" class="px-3 py-1 text-xs font-medium text-gray-700 bg-gray-200 rounded hover:bg-gray-300 disabled:opacity-50">{{ t('profile.actions.cancel') }}</button>
                            </div>
                          </div>
                          <div>
                            <div class="flex items-center justify-between mb-1"><label class="block text-sm font-medium text-gray-700">{{ t('profile.info.firstNameLabel') }}</label><button v-if="canEditProfile()" type="button" @click="toggleEdit('first_name')" class="p-1 text-gray-600 hover:text-green-600 hover:bg-green-50 rounded transition-colors"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"></path></svg></button></div>
                            <input v-model="profileForm.first_name" :disabled="editingField !== 'first_name'" type="text" :placeholder="t('profile.info.firstNamePlaceholder')" :class="['w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 text-sm', editingField === 'first_name' ? 'border-gray-200' : 'border-gray-200 bg-gray-50']">
                            <div v-if="editingField === 'first_name'" class="flex space-x-2 mt-2">
                              <button type="button" @click="saveField('first_name')" :disabled="loading" class="px-3 py-1 text-xs font-medium text-white bg-green-600 rounded hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed">{{ loading ? t('profile.actions.saving') : t('profile.actions.save') }}</button>
                              <button type="button" @click="cancelEdit" :disabled="loading" class="px-3 py-1 text-xs font-medium text-gray-700 bg-gray-200 rounded hover:bg-gray-300 disabled:opacity-50">{{ t('profile.actions.cancel') }}</button>
                            </div>
                          </div>
                          <div>
                            <div class="flex items-center justify-between mb-1"><label class="block text-sm font-medium text-gray-700">{{ t('profile.info.lastNameLabel') }}</label><button type="button" @click="toggleEdit('last_name')" class="p-1 text-gray-600 hover:text-green-600 hover:bg-green-50 rounded transition-colors"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"></path></svg></button></div>
                            <input v-model="profileForm.last_name" :disabled="editingField !== 'last_name'" type="text" :placeholder="t('profile.info.lastNamePlaceholder')" :class="['w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 text-sm', editingField === 'last_name' ? 'border-gray-200' : 'border-gray-200 bg-gray-50']">
                            <div v-if="editingField === 'last_name'" class="flex space-x-2 mt-2">
                              <button type="button" @click="saveField('last_name')" :disabled="loading" class="px-3 py-1 text-xs font-medium text-white bg-green-600 rounded hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed">{{ loading ? t('profile.actions.saving') : t('profile.actions.save') }}</button>
                              <button type="button" @click="cancelEdit" :disabled="loading" class="px-3 py-1 text-xs font-medium text-gray-700 bg-gray-200 rounded hover:bg-gray-300 disabled:opacity-50">{{ t('profile.actions.cancel') }}</button>
                            </div>
                          </div>
                        </div>
                        <div class="border-t border-gray-100 pt-6">
                          <h4 class="text-md font-medium text-gray-900 mb-4">{{ t('profile.contact.title') }}</h4>
                          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                              <div class="flex items-center justify-between mb-1"><label class="block text-sm font-medium text-gray-700">{{ t('profile.contact.addressLabel') }}</label><button type="button" @click="toggleEdit('address')" class="p-1 text-gray-600 hover:text-green-600 hover:bg-green-50 rounded transition-colors"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"></path></svg></button></div>
                              <input v-model="profileForm.address" :disabled="editingField !== 'address'" type="text" :placeholder="t('profile.contact.addressPlaceholder')" :class="['w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 text-sm', editingField === 'address' ? 'border-gray-200' : 'border-gray-200 bg-gray-50']">
                              <div v-if="editingField === 'address'" class="flex space-x-2 mt-2">
                                <button type="button" @click="saveField('address')" :disabled="loading" class="px-3 py-1 text-xs font-medium text-white bg-green-600 rounded hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed">{{ loading ? t('profile.actions.saving') : t('profile.actions.save') }}</button>
                                <button type="button" @click="cancelEdit" :disabled="loading" class="px-3 py-1 text-xs font-medium text-gray-700 bg-gray-200 rounded hover:bg-gray-300 disabled:opacity-50">{{ t('profile.actions.cancel') }}</button>
                              </div>
                            </div>
                            <div class="md:col-span-2">
                              <div class="flex items-center justify-between mb-3"><label class="block text-sm font-medium text-gray-700">{{ t('profile.contact.locationLabel') }}</label><button type="button" @click="toggleEdit('location')" class="p-1 text-gray-600 hover:text-green-600 hover:bg-green-50 rounded transition-colors"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"></path></svg></button></div>
                              <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                                <div>
                                  <label class="block text-xs font-medium text-gray-500 mb-1">{{ t('profile.contact.provinceLabel') }}</label>
                                  <select v-model="profileForm.province_id" @change="onProvinceChange" :disabled="editingField !== 'location'" class="border rounded w-full p-3 appearance-none">
                                    <option value="">{{ t('profile.contact.provincePlaceholder') }}</option>
                                    <option v-for="p in provinces" :key="p.code" :value="String(p.code)">{{ p.name }}</option>
                                  </select>
                                </div>
                                <div>
                                  <label class="block text-xs font-medium text-gray-500 mb-1">{{ t('profile.contact.districtLabel') }}</label>
                                  <select v-model="profileForm.district_id" @change="onDistrictChange" :disabled="editingField !== 'location' || !profileForm.province_id" class="border rounded w-full p-3 appearance-none">
                                    <option value="">{{ t('profile.contact.districtPlaceholder') }}</option>
                                    <option v-for="d in districts" :key="d.code" :value="String(d.code)">{{ d.name }}</option>
                                  </select>
                                </div>
                                <div>
                                  <label class="block text-xs font-medium text-gray-500 mb-1">{{ t('profile.contact.wardLabel') }}</label>
                                  <select v-model="profileForm.ward_id" :disabled="editingField !== 'location' || !profileForm.district_id" class="border rounded w-full p-3 appearance-none">
                                    <option value="">{{ t('profile.contact.wardPlaceholder') }}</option>
                                    <option v-for="w in wards" :key="w.code" :value="String(w.code)">{{ w.name }}</option>
                                  </select>
                                </div>
                              </div>
                              <div v-if="editingField === 'location'" class="flex space-x-2 mt-2">
                                <button type="button" @click="saveField('location')" :disabled="loading" class="px-3 py-1 text-xs font-medium text-white bg-green-600 rounded hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed">{{ loading ? t('profile.actions.saving') : t('profile.actions.save') }}</button>
                                <button type="button" @click="cancelEdit" :disabled="loading" class="px-3 py-1 text-xs font-medium text-gray-700 bg-gray-200 rounded hover:bg-gray-300 disabled:opacity-50">{{ t('profile.actions.cancel') }}</button>
                              </div>
                            </div>
                            <div>
                              <div class="flex items-center justify-between mb-1"><label class="block text-sm font-medium text-gray-700">{{ t('profile.contact.phoneLabel') }}</label><button type="button" @click="toggleEdit('phone')" class="p-1 text-gray-600 hover:text-green-600 hover:bg-green-50 rounded transition-colors"><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"></path></svg></button></div>
                              <input v-model="profileForm.phone" :disabled="editingField !== 'phone'" type="tel" :placeholder="t('profile.contact.phonePlaceholder')" :class="['w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 text-sm', editingField === 'phone' ? 'border-gray-200' : 'border-gray-200 bg-gray-50']">
                              <div v-if="editingField === 'phone'" class="flex space-x-2 mt-2">
                                <button type="button" @click="saveField('phone')" :disabled="loading" class="px-3 py-1 text-xs font-medium text-white bg-green-600 rounded hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed">{{ loading ? t('profile.actions.saving') : t('profile.actions.save') }}</button>
                                <button type="button" @click="cancelEdit" :disabled="loading" class="px-3 py-1 text-xs font-medium text-gray-700 bg-gray-200 rounded hover:bg-gray-300 disabled:opacity-50">{{ t('profile.actions.cancel') }}</button>
                              </div>
                            </div>
                          </div>
                        </div>
                      </form>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <footer class="bg-white border-t border-gray-200 mt-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div class="flex items-center justify-between">
          <p class="text-sm text-gray-500">{{ t('profile.footer.copyright') }}</p>
          <div class="flex items-center space-x-6">
            <select class="text-sm text-gray-500 bg-transparent border-none focus:outline-none">
              <option>{{ t('profile.footer.language.vietnamese') }}</option>
              <option>{{ t('profile.footer.language.english') }}</option>
            </select>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { useAuthStore } from '~/stores/auth';
import { useCustomersService } from '~/services/customers';
import { useActionPermissions } from '~/composables/useActionPermissions';
import { useNuxtApp, navigateTo } from 'nuxt/app';

const { t } = useI18n();
const auth = useAuthStore();
const customersService = useCustomersService();
const { $toast } = useNuxtApp() as any;
const { canEditProfile, canChangePassword, canUploadAvatar, validateAction } = useActionPermissions();

const loading = ref(false);
const editingField = ref<string | null>(null);
const originalValues = ref<any>({});
const showPasswordForm = ref(false);
const passwordForm = ref({
  current_password: '',
  new_password: '',
  confirm_password: ''
});
const profileForm = ref<any>({
  first_name: '',
  last_name: '',
  email: '',
  username: '',
  nickname: '',
  website: '',
  bio: '',
  avatar: '',
  phone: '',
  address: '',
  province_id: '',
  district_id: '',
  ward_id: '',
  date_of_birth: '',
  gender: 'male'
});

// Computed
const isAuthenticated = computed(() => !!auth.user);

// Methods
const loadProfile = async () => {
  try {
    if (!isAuthenticated.value) {
      await navigateTo('/auth/login');
      return;
    }
    if (auth.user) {
      profileForm.value = { ...profileForm.value, ...auth.user };
      if (profileForm.value.province_id) await fetchDistricts(String(profileForm.value.province_id));
      if (profileForm.value.district_id) await fetchWards(String(profileForm.value.district_id));
    }
    const profileData = await customersService.getProfile();
    if (profileData?.customer) {
      profileForm.value = { ...profileForm.value, ...profileData.customer };
      if (profileForm.value.province_id) await fetchDistricts(String(profileForm.value.province_id));
      if (profileForm.value.district_id) await fetchWards(String(profileForm.value.district_id));
    }
  } catch (error) {
    console.error('Error loading profile:', error);
    $toast.error(t('profile.notifications.loadProfileError'));
  }
};

const updateProfile = async () => {
  try {
    loading.value = true;
    const result = await customersService.updateProfile(profileForm.value);
    if (result?.customer) {
      auth.user = result.customer;
      profileForm.value = { ...profileForm.value, ...result.customer };
      $toast.success(t('profile.notifications.updateProfileSuccess'));
    }
  } catch (error: any) {
    $toast.error(error?.data?.message || t('profile.notifications.updateProfileError'));
  } finally {
    loading.value = false;
  }
};

const toggleEdit = (fieldName: string) => {
  // Check permission before allowing edit
  const validation = validateAction('edit_profile');
  if (!validation.allowed) {
    $toast.error(validation.reason || 'No permission to edit profile');
    return;
  }

  if (editingField.value === fieldName) {
    cancelEdit();
  } else {
    editingField.value = fieldName;
    originalValues.value[fieldName] = profileForm.value[fieldName];
  }
};

const cancelEdit = () => {
  if (editingField.value && originalValues.value[editingField.value] !== undefined) {
    profileForm.value[editingField.value] = originalValues.value[editingField.value];
  }
  editingField.value = null;
  originalValues.value = {};
};

const saveField = async (fieldName: string) => {
  // Check permission before saving
  const validation = validateAction('edit_profile');
  if (!validation.allowed) {
    $toast.error(validation.reason || 'No permission to edit profile');
    return;
  }

  try {
    loading.value = true;
    const updateData: any = {};
    if (fieldName === 'location') {
      updateData.province_id = profileForm.value.province_id ? String(profileForm.value.province_id) : '';
      updateData.district_id = profileForm.value.district_id ? String(profileForm.value.district_id) : '';
      updateData.ward_id = profileForm.value.ward_id ? String(profileForm.value.ward_id) : '';
    } else {
      updateData[fieldName] = profileForm.value[fieldName];
    }
    const result = await customersService.updateProfile(updateData);
    if (result?.customer) {
      auth.user = result.customer;
      profileForm.value = { ...profileForm.value, ...result.customer };
      $toast.success(t('profile.notifications.fieldUpdateSuccess'));
    }
  } catch (err: any) {
    $toast.error(err?.data?.message || t('profile.notifications.fieldUpdateError'));
    if (originalValues.value[fieldName] !== undefined) {
      profileForm.value[fieldName] = originalValues.value[fieldName];
    }
  } finally {
    loading.value = false;
    editingField.value = null;
    originalValues.value = {};
  }
};

const handleImageUpload = async (event: any) => {
  // Check permission before uploading
  const validation = validateAction('edit_profile');
  if (!validation.allowed) {
    $toast.error(validation.reason || 'No permission to upload avatar');
    return;
  }

  const file = event.target.files?.[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = async (e: any) => {
    const base64 = e.target.result;
    profileForm.value.avatar = base64;
    try {
      const result = await customersService.updateProfile({ avatar: base64 });
      if (result?.customer) {
        auth.user = result.customer;
        profileForm.value.avatar = result.customer.avatar || base64;
      }
      $toast.success(t('profile.notifications.avatarUpdateSuccess'));
      if (editingField.value === 'avatar') {
        editingField.value = null;
      }
    } catch (err: any) {
      $toast.error(err?.data?.message || t('profile.notifications.avatarUpdateError'));
    }
  };
  reader.readAsDataURL(file);
};

const togglePasswordForm = () => {
  showPasswordForm.value = !showPasswordForm.value;
  if (!showPasswordForm.value) {
    resetPasswordForm();
  }
};

const cancelPasswordChange = () => {
  resetPasswordForm();
};

const changePassword = async () => {
  // Check permission before changing password
  const validation = validateAction('change_password');
  if (!validation.allowed) {
    $toast.error(validation.reason || 'No permission to change password');
    return;
  }

  if (!passwordForm.value.current_password) return $toast.error(t('profile.notifications.currentPasswordRequired'));
  if (!passwordForm.value.new_password) return $toast.error(t('profile.notifications.newPasswordRequired'));
  if (passwordForm.value.new_password.length < 6) return $toast.error(t('profile.notifications.newPasswordMinLength'));
  if (passwordForm.value.new_password !== passwordForm.value.confirm_password) return $toast.error(t('profile.notifications.passwordMismatch'));

  try {
    loading.value = true;
    await customersService.changePassword({
      current_password: passwordForm.value.current_password,
      new_password: passwordForm.value.new_password
    });
    $toast.success(t('profile.notifications.passwordUpdateSuccess'));
    resetPasswordForm();
  } catch (error: any) {
    if (error?.statusCode === 401) {
      $toast.error(t('profile.notifications.sessionExpired'));
      await navigateTo('/auth/login');
    } else {
      $toast.error(error?.data?.message || t('profile.notifications.passwordUpdateError'));
    }
  } finally {
    loading.value = false;
  }
};

const resetPasswordForm = () => {
  passwordForm.value = { current_password: '', new_password: '', confirm_password: '' };
  showPasswordForm.value = false;
};

// --- Vietnam Province API ---
const provinces = ref<any[]>([]);
const districts = ref<any[]>([]);
const wards = ref<any[]>([]);

async function fetchProvinces() {
  try {
    const res = await fetch('https://provinces.open-api.vn/api/');
    provinces.value = await res.json();
  } catch (e) { console.error(e) }
}

async function fetchDistricts(provinceCode: string) {
  if (!provinceCode) { districts.value = []; wards.value = []; return }
  try {
    const res = await fetch(`https://provinces.open-api.vn/api/p/${provinceCode}?depth=2`);
    const data = await res.json();
    districts.value = data?.districts || [];
    wards.value = [];
  } catch (e) { console.error(e) }
}

async function fetchWards(districtCode: string) {
  if (!districtCode) { wards.value = []; return }
  try {
    const res = await fetch(`https://provinces.open-api.vn/api/d/${districtCode}?depth=2`);
    const data = await res.json();
    wards.value = data?.wards || [];
  } catch (e) { console.error(e) }
}

function onProvinceChange() {
  fetchDistricts(profileForm.value.province_id);
  profileForm.value.district_id = '';
  profileForm.value.ward_id = '';
}

function onDistrictChange() {
  fetchWards(profileForm.value.district_id);
  profileForm.value.ward_id = '';
}

onMounted(() => {
  loadProfile();
  fetchProvinces();
});
</script>

<style scoped>
/* Custom scrollbar for sidebar */
.overflow-y-auto::-webkit-scrollbar {
  width: 4px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f1f5f9;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 2px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Smooth transitions for interactive elements */
button, a {
  transition: all 0.2s ease-in-out;
}

/* Focus styles for better accessibility */
input:focus, textarea:focus, select:focus {
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Custom gradient for profile avatar */
.profile-gradient {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Hover effects for navigation items */
nav a:hover {
  transform: translateX(2px);
}

/* Loading state for buttons */
button:disabled {
  cursor: not-allowed;
}

/* Custom file input styling */
input[type="file"] {
  display: none;
}

.file-upload-label {
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  padding: 0.5rem 1rem;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: #475569;
  transition: all 0.2s ease-in-out;
}

.file-upload-label:hover {
  background: #f1f5f9;
  border-color: #cbd5e1;
}

/* Responsive design improvements */
@media (max-width: 1024px) {
  .grid-cols-1.lg\\:grid-cols-3 {
    grid-template-columns: 1fr;
  }
  
  .w-64 {
    width: 100%;
    margin-bottom: 2rem;
  }
  
  .flex {
    flex-direction: column;
  }
}

@media (max-width: 768px) {
  .hidden.md\\:flex {
    display: none;
  }
  
  .grid-cols-1.md\\:grid-cols-2 {
    grid-template-columns: 1fr;
  }
  
  .max-w-lg {
    max-width: 100%;
  }
  
  .mx-8 {
    margin-left: 1rem;
    margin-right: 1rem;
  }
}

/* Animation for form submission */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* Custom styling for select dropdowns */
select {
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='m6 8 4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 0.5rem center;
  background-repeat: no-repeat;
  background-size: 1.5em 1.5em;
  padding-right: 2.5rem;
}

/* Toast notification styling */
.toast {
  position: fixed;
  top: 1rem;
  right: 1rem;
  z-index: 50;
  padding: 1rem;
  border-radius: 0.5rem;
  font-weight: 500;
  font-size: 0.875rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

.toast.success {
  background-color: #10b981;
  color: white;
}

.toast.error {
  background-color: #ef4444;
  color: white;
}

/* Profile image container */
.profile-image-container {
  position: relative;
  overflow: hidden;
  border-radius: 0.5rem;
}

.profile-image-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(45deg, rgba(255, 165, 0, 0.3), rgba(255, 192, 203, 0.3), rgba(255, 165, 0, 0.3));
  z-index: 1;
}

.profile-image-container img {
  position: relative;
  z-index: 2;
}
</style>