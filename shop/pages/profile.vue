<template>
  <div class="min-h-screen bg-gray-50">

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="flex gap-8">
        <!-- Left Sidebar Navigation -->
        <div class="w-64 flex-shrink-0">
          <div class="bg-white rounded-lg shadow-sm border border-gray-200">
            <!-- User Profile Section -->
            <div class="p-6 border-b border-gray-100">
              <div class="flex items-center space-x-3">
                <div class="w-10 h-10 bg-gradient-to-r from-green-500 to-emerald-500 rounded-full flex items-center justify-center">
                  <span class="text-white text-sm font-medium">{{ (profileForm.first_name || 'U')[0] }}</span>
                </div>
                <div>
                  <p class="text-sm font-semibold text-gray-900">{{ profileForm.first_name || 'Khách hàng' }} {{ profileForm.last_name || '' }}</p>
                  <p class="text-xs text-gray-500">{{ profileForm.email || 'email@example.com' }}</p>
                </div>
              </div>
            </div>

            <!-- Navigation Menu -->
            <nav class="p-2">
              <div class="space-y-1">
                <!-- Navigate Section -->
                <div class="px-3 py-2">
                  <p class="text-xs font-semibold text-gray-500 uppercase tracking-wider">Điều hướng</p>
                </div>
                
                <a href="/" class="flex items-center px-3 py-2 text-sm font-medium text-green-600 bg-green-50 rounded-md group">
                  <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z"></path>
                  </svg>
                  Trang chủ
                </a>
                
                <a href="/products" class="flex items-center px-3 py-2 text-sm font-medium text-gray-600 rounded-md hover:text-gray-900 hover:bg-gray-50 group">
                  <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M12 11V7"></path>
                  </svg>
                  Sản phẩm
                </a>

                <a href="/cart" class="flex items-center px-3 py-2 text-sm font-medium text-gray-600 rounded-md hover:text-gray-900 hover:bg-gray-50 group">
                  <svg class="w-4 h-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-2.5 5M7 13l2.5 5m6-5v6a2 2 0 01-2 2H9a2 2 0 01-2-2v-6m8 0V9a2 2 0 00-2-2H9a2 2 0 00-2 2v4.01"></path>
                  </svg>
                  Giỏ hàng
                </a>
              </div>
            </nav>

          </div>
        </div>

        <!-- Main Content Area -->
        <div class="flex-1">
          <div class="bg-white rounded-lg shadow-sm border border-gray-200">
            <!-- Header -->
            <div class="px-6 py-4 border-b border-gray-100">
              <div class="flex items-center justify-between">
                <div>
                  <h1 class="text-xl font-semibold text-gray-900">Hồ sơ cá nhân</h1>
                  <p class="text-sm text-gray-500 mt-1">Quản lý thông tin tài khoản</p>
                </div>
                <div class="flex items-center space-x-3">
                  <span class="text-sm text-gray-500">Cài đặt</span>
                </div>
              </div>
            </div>

            <div class="p-6">
              <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
                <!-- Profile Photo Section -->
                <div class="lg:col-span-1">
                  <div class="text-center">
                    <!-- Profile Image -->
                    <div class="relative inline-block">
                        <div class="w-48 h-48 bg-gradient-to-br from-orange-200 via-pink-200 to-orange-300 rounded-lg overflow-hidden shadow-lg flex items-center justify-center">
                          <div v-if="!profileForm.avatar" class="text-6xl font-bold text-orange-600">
                            {{ (profileForm.first_name || 'U')[0] }}
                          </div>
                          <img 
                            v-if="profileForm.avatar"
                            :src="profileForm.avatar" 
                            alt="Profile" 
                            class="w-full h-full object-cover"
                          >
                        </div>
                      <button @click="toggleEdit('avatar')" class="absolute top-2 right-2 w-8 h-8 bg-white rounded-full shadow-lg flex items-center justify-center hover:bg-gray-50">
                        <svg class="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"></path>
                        </svg>
                      </button>
                    </div>
                    
                    <div class="mt-4">
                      <label v-if="editingField === 'avatar'" class="file-upload-label">
                        <input type="file" accept="image/*" @change="handleImageUpload">
                        Tải lên ảnh
                      </label>
                    </div>

                    <!-- Password Section -->
                    <div class="mt-8 text-left">
                      <!-- Password Change Button (Default State) -->
                      <div v-if="!showPasswordForm">
                        <button 
                          @click="togglePasswordForm"
                          class="w-full px-4 py-2 bg-green-600 text-white text-sm font-medium rounded-lg hover:bg-green-700 transition-colors flex items-center justify-center space-x-2"
                        >
                          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                          </svg>
                          <span>Đổi mật khẩu</span>
                        </button>
                      </div>

                      <!-- Password Change Form (When Expanded) -->
                      <div v-else class="space-y-4">
                        <div class="flex items-center justify-between mb-4">
                          <h4 class="text-sm font-semibold text-gray-700">Đổi mật khẩu</h4>
                          <button 
                            @click="togglePasswordForm"
                            class="text-gray-400 hover:text-gray-600"
                          >
                            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                            </svg>
                          </button>
                        </div>

                        <div>
                          <label class="block text-sm font-medium text-gray-700 mb-2">Mật khẩu hiện tại</label>
                          <input 
                            v-model="passwordForm.current_password"
                            type="password"
                            autocomplete="current-password"
                            placeholder="Nhập mật khẩu hiện tại" 
                            class="w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 text-sm"
                          >
                        </div>
                        
                        <div>
                          <label class="block text-sm font-medium text-gray-700 mb-2">Mật khẩu mới</label>
                          <input 
                            v-model="passwordForm.new_password"
                            type="password"
                            autocomplete="new-password"
                            placeholder="Nhập mật khẩu mới (ít nhất 6 ký tự)" 
                            class="w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 text-sm"
                          >
                        </div>

                        <div>
                          <label class="block text-sm font-medium text-gray-700 mb-2">Xác nhận mật khẩu mới</label>
                          <input 
                            v-model="passwordForm.confirm_password"
                            type="password"
                            autocomplete="new-password"
                            placeholder="Nhập lại mật khẩu mới" 
                            class="w-full px-3 py-2 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 text-sm"
                          >
                        </div>

                        <div class="flex space-x-3 pt-2">
                          <button 
                            @click="changePassword"
                            :disabled="loading"
                            class="flex-1 px-4 py-2 bg-green-600 text-white text-sm font-medium rounded-lg hover:bg-green-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                          >
                            {{ loading ? 'Đang xử lý...' : 'Cập nhật mật khẩu' }}
                          </button>
                          <button 
                            @click="cancelPasswordChange"
                            type="button"
                            class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
                          >
                            Hủy
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Profile Information Section -->
                <div class="lg:col-span-2">
                  <div class="space-y-6">
                    <div>
                      <h3 class="text-lg font-medium text-gray-900 mb-4">Thông tin cá nhân</h3>
                      
                      <form @submit.prevent="updateProfile" class="space-y-4">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                          <!-- Email -->
                          <div>
                            <div class="flex items-center justify-between mb-1">
                              <label class="block text-sm font-medium text-gray-700">Email</label>
                              <button 
                                type="button"
                                @click="toggleEdit('email')"
                                class="p-1 text-gray-600 hover:text-green-600 hover:bg-green-50 rounded transition-colors"
                              >
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"></path>
                                </svg>
                              </button>
                            </div>
                            <input 
                              v-model="profileForm.email"
                              :disabled="editingField !== 'email'"
                              type="email" 
                              placeholder="email@example.com" 
                              :class="[
                                'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 text-sm',
                                editingField === 'email' ? 'border-gray-200' : 'border-gray-200 bg-gray-50'
                              ]"
                            >
                            <p style="display: none;" class="text-xs text-gray-500 mt-1">{{ profileForm.email || 'email@example.com' }}</p>
                            <div v-if="editingField === 'email'" class="flex space-x-2 mt-2">
                              <button 
                                type="button"
                                @click="saveField('email')"
                                :disabled="loading"
                                class="px-3 py-1 text-xs font-medium text-white bg-green-600 rounded hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
                              >
                                {{ loading ? 'Đang lưu...' : 'Lưu' }}
                              </button>
                              <button 
                                type="button"
                                @click="cancelEdit"
                                :disabled="loading"
                                class="px-3 py-1 text-xs font-medium text-gray-700 bg-gray-200 rounded hover:bg-gray-300 disabled:opacity-50"
                              >
                                Hủy
                              </button>
                            </div>
                          </div>
                          
                          <!-- First Name -->
                          <div>
                            <div class="flex items-center justify-between mb-1">
                              <label class="block text-sm font-medium text-gray-700">Tên</label>
                              <button 
                                type="button"
                                @click="toggleEdit('first_name')"
                                class="p-1 text-gray-600 hover:text-green-600 hover:bg-green-50 rounded transition-colors"
                              >
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"></path>
                                </svg>
                              </button>
                            </div>
                            <input 
                              v-model="profileForm.first_name"
                              :disabled="editingField !== 'first_name'"
                              type="text" 
                              placeholder="Tên của bạn" 
                              :class="[
                                'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 text-sm',
                                editingField === 'first_name' ? 'border-gray-200' : 'border-gray-200 bg-gray-50'
                              ]"
                            >
                            <p style="display: none;" class="text-xs text-gray-500 mt-1">{{ profileForm.first_name || 'Tên của bạn' }}</p>
                            <div v-if="editingField === 'first_name'" class="flex space-x-2 mt-2">
                              <button 
                                type="button"
                                @click="saveField('first_name')"
                                :disabled="loading"
                                class="px-3 py-1 text-xs font-medium text-white bg-green-600 rounded hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
                              >
                                {{ loading ? 'Đang lưu...' : 'Lưu' }}
                              </button>
                              <button 
                                type="button"
                                @click="cancelEdit"
                                :disabled="loading"
                                class="px-3 py-1 text-xs font-medium text-gray-700 bg-gray-200 rounded hover:bg-gray-300 disabled:opacity-50"
                              >
                                Hủy
                              </button>
                            </div>
                          </div>


                          <!-- Last Name -->
                          <div>
                            <div class="flex items-center justify-between mb-1">
                              <label class="block text-sm font-medium text-gray-700">Họ</label>
                              <button 
                                type="button"
                                @click="toggleEdit('last_name')"
                                class="p-1 text-gray-600 hover:text-green-600 hover:bg-green-50 rounded transition-colors"
                              >
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"></path>
                                </svg>
                              </button>
                            </div>
                            <input 
                              v-model="profileForm.last_name"
                              :disabled="editingField !== 'last_name'"
                              type="text" 
                              placeholder="Họ của bạn" 
                              :class="[
                                'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 text-sm',
                                editingField === 'last_name' ? 'border-gray-200' : 'border-gray-200 bg-gray-50'
                              ]"
                            >
                            <p style="display: none;" class="text-xs text-gray-500 mt-1">{{ profileForm.last_name || 'Họ của bạn' }}</p>
                            <div v-if="editingField === 'last_name'" class="flex space-x-2 mt-2">
                              <button 
                                type="button"
                                @click="saveField('last_name')"
                                :disabled="loading"
                                class="px-3 py-1 text-xs font-medium text-white bg-green-600 rounded hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
                              >
                                {{ loading ? 'Đang lưu...' : 'Lưu' }}
                              </button>
                              <button 
                                type="button"
                                @click="cancelEdit"
                                :disabled="loading"
                                class="px-3 py-1 text-xs font-medium text-gray-700 bg-gray-200 rounded hover:bg-gray-300 disabled:opacity-50"
                              >
                                Hủy
                              </button>
                            </div>
                          </div>
                        </div>

                        <div class="border-t border-gray-100 pt-6">
                          <h4 class="text-md font-medium text-gray-900 mb-4">Thông tin liên hệ</h4>
                          
                          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                          <!-- Address -->
                          <div>
                            <div class="flex items-center justify-between mb-1">
                              <label class="block text-sm font-medium text-gray-700">Địa chỉ nhà</label>
                              <button 
                                type="button"
                                @click="toggleEdit('address')"
                                class="p-1 text-gray-600 hover:text-green-600 hover:bg-green-50 rounded transition-colors"
                              >
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"></path>
                                </svg>
                              </button>
                            </div>
                            <input 
                              v-model="profileForm.address"
                              :disabled="editingField !== 'address'"
                              type="text" 
                              placeholder="Số nhà, đường, phường/xã, quận/huyện, tỉnh/thành phố" 
                              :class="[
                                'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 text-sm',
                                editingField === 'address' ? 'border-gray-200' : 'border-gray-200 bg-gray-50'
                              ]"
                            >
                            <p style="display: none;" class="text-xs text-gray-500 mt-1">{{ profileForm.address || 'Địa chỉ nhà' }}</p>
                            <div v-if="editingField === 'address'" class="flex space-x-2 mt-2">
                              <button 
                                type="button"
                                @click="saveField('address')"
                                :disabled="loading"
                                class="px-3 py-1 text-xs font-medium text-white bg-green-600 rounded hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
                              >
                                {{ loading ? 'Đang lưu...' : 'Lưu' }}
                              </button>
                              <button 
                                type="button"
                                @click="cancelEdit"
                                :disabled="loading"
                                class="px-3 py-1 text-xs font-medium text-gray-700 bg-gray-200 rounded hover:bg-gray-300 disabled:opacity-50"
                              >
                                Hủy
                              </button>
                            </div>
                          </div>

                          <!-- Province/District/Ward (same editable pattern) -->
                          <div class="md:col-span-2">
                            <div class="flex items-center justify-between mb-3">
                              <label class="block text-sm font-medium text-gray-700">Khu vực (Tỉnh/Quận/Phường)</label>
                              <button 
                                type="button"
                                @click="toggleEdit('location')"
                                class="p-1 text-gray-600 hover:text-green-600 hover:bg-green-50 rounded transition-colors"
                              >
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"></path>
                                </svg>
                              </button>
                            </div>
                            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                              <div>
                                <label class="block text-xs font-medium text-gray-500 mb-1">Tỉnh/Thành phố</label>
                                <select 
                                  v-model="profileForm.province_id" 
                                  @change="onProvinceChange"
                                  :disabled="editingField !== 'location'"
                                  class="border rounded w-full p-3 appearance-none"
                                >
                                  <option value="">-- Chọn tỉnh/thành phố --</option>
                                  <option v-for="p in provinces" :key="p.code" :value="String(p.code)">{{ p.name }}</option>
                                </select>
                                <div v-if="loadingProvinces" class="text-sm text-gray-500 mt-1">Đang tải...</div>
                              </div>
                              <div>
                                <label class="block text-xs font-medium text-gray-500 mb-1">Quận/Huyện</label>
                                <select 
                                  v-model="profileForm.district_id" 
                                  @change="onDistrictChange"
                                  :disabled="editingField !== 'location' || !profileForm.province_id"
                                  class="border rounded w-full p-3 appearance-none"
                                >
                                  <option value="">-- Chọn quận/huyện --</option>
                                  <option v-for="d in districts" :key="d.code" :value="String(d.code)">{{ d.name }}</option>
                                </select>
                                <div v-if="loadingDistricts" class="text-sm text-gray-500 mt-1">Đang tải...</div>
                              </div>
                              <div>
                                <label class="block text-xs font-medium text-gray-500 mb-1">Phường/Xã</label>
                                <select 
                                  v-model="profileForm.ward_id" 
                                  :disabled="editingField !== 'location' || !profileForm.district_id"
                                  class="border rounded w-full p-3 appearance-none"
                                >
                                  <option value="">-- Chọn phường/xã --</option>
                                  <option v-for="w in wards" :key="w.code" :value="String(w.code)">{{ w.name }}</option>
                                </select>
                                <div v-if="loadingWards" class="text-sm text-gray-500 mt-1">Đang tải...</div>
                              </div>
                            </div>
                            <div v-if="editingField === 'location'" class="flex space-x-2 mt-2">
                              <button 
                                type="button"
                                @click="saveField('location')"
                                :disabled="loading"
                                class="px-3 py-1 text-xs font-medium text-white bg-green-600 rounded hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
                              >
                                {{ loading ? 'Đang lưu...' : 'Lưu' }}
                              </button>
                              <button 
                                type="button"
                                @click="cancelEdit"
                                :disabled="loading"
                                class="px-3 py-1 text-xs font-medium text-gray-700 bg-gray-200 rounded hover:bg-gray-300 disabled:opacity-50"
                              >
                                Hủy
                              </button>
                            </div>
                          </div>

                            <!-- Phone -->
                            <div>
                              <div class="flex items-center justify-between mb-1">
                                <label class="block text-sm font-medium text-gray-700">Số điện thoại</label>
                                <button 
                                  type="button"
                                  @click="toggleEdit('phone')"
                                  class="p-1 text-gray-600 hover:text-green-600 hover:bg-green-50 rounded transition-colors"
                                >
                                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"></path>
                                  </svg>
                                </button>
                              </div>
                              <input 
                                v-model="profileForm.phone"
                                :disabled="editingField !== 'phone'"
                                type="tel" 
                                placeholder="0123456789" 
                                :class="[
                                  'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 text-sm',
                                  editingField === 'phone' ? 'border-gray-200' : 'border-gray-200 bg-gray-50'
                                ]"
                              >
                              <p style="display: none;" class="text-xs text-gray-500 mt-1">{{ profileForm.phone || 'Số điện thoại' }}</p>
                              <div v-if="editingField === 'phone'" class="flex space-x-2 mt-2">
                                <button 
                                  type="button"
                                  @click="saveField('phone')"
                                  :disabled="loading"
                                  class="px-3 py-1 text-xs font-medium text-white bg-green-600 rounded hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
                                >
                                  {{ loading ? 'Đang lưu...' : 'Lưu' }}
                                </button>
                                <button 
                                  type="button"
                                  @click="cancelEdit"
                                  :disabled="loading"
                                  class="px-3 py-1 text-xs font-medium text-gray-700 bg-gray-200 rounded hover:bg-gray-300 disabled:opacity-50"
                                >
                                  Hủy
                                </button>
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

    <!-- Footer -->
    <footer class="bg-white border-t border-gray-200 mt-12">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div class="flex items-center justify-between">
          <p class="text-sm text-gray-500">© 2024 AgriShop - Nông nghiệp thông minh</p>
          <div class="flex items-center space-x-6">
            <select class="text-sm text-gray-500 bg-transparent border-none focus:outline-none">
              <option>Tiếng Việt</option>
              <option>English</option>
            </select>
            <div class="flex items-center space-x-2">
              <button class="p-1 text-gray-400 hover:text-gray-600">
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z"/>
                </svg>
              </button>
              <button class="p-1 text-gray-400 hover:text-gray-600">
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M22.46 6c-.77.35-1.6.58-2.46.69.88-.53 1.56-1.37 1.88-2.38-.83.5-1.75.85-2.72 1.05C18.37 4.5 17.26 4 16 4c-2.35 0-4.27 1.92-4.27 4.29 0 .34.04.67.11.98C8.28 9.09 5.11 7.38 3 4.79c-.37.63-.58 1.37-.58 2.15 0 1.49.75 2.81 1.91 3.56-.71 0-1.37-.2-1.95-.5v.03c0 2.08 1.48 3.82 3.44 4.21a4.22 4.22 0 0 1-1.93.07 4.28 4.28 0 0 0 4 2.98 8.521 8.521 0 0 1-5.33 1.84c-.34 0-.68-.02-1.02-.06C3.44 20.29 5.7 21 8.12 21 16 21 20.33 14.46 20.33 8.79c0-.19 0-.37-.01-.56.84-.6 1.56-1.36 2.14-2.23z"/>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useAuthStore } from '~/stores/auth'
import { useCustomersService } from '~/services/customers'

const auth = useAuthStore()
const customersService = useCustomersService()
const { $toast } = useNuxtApp()

// Reactive data
const loading = ref(false)
const editingField = ref(null)
const originalValues = ref({})
const showPasswordForm = ref(false)
const passwordForm = ref({
  current_password: '',
  new_password: '',
  confirm_password: ''
})
const profileForm = ref({
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
})

// Computed
const isAuthenticated = computed(() => !!auth.user)

// Methods
const loadProfile = async () => {
  try {
    if (!isAuthenticated.value) {
      console.log('Not authenticated, redirecting to login')
      await navigateTo('/auth/login')
      return
    }

    console.log('Loading profile... auth.user:', auth.user)
    
    // First try to load from auth store (faster)
    if (auth.user) {
      console.log('Using auth store data first')
      profileForm.value = {
        first_name: auth.user.first_name || '',
        last_name: auth.user.last_name || '',
        email: auth.user.email || '',
        username: auth.user.username || auth.user.email || '',
        nickname: auth.user.nickname || '',
        website: auth.user.website || '',
        bio: auth.user.bio || '',
        avatar: auth.user.avatar || '',
        phone: auth.user.phone || '',
          address: auth.user.address || '',
          province_id: (auth.user as any).province_id || '',
          district_id: (auth.user as any).district_id || '',
          ward_id: (auth.user as any).ward_id || '',
        date_of_birth: auth.user.date_of_birth || '',
        gender: auth.user.gender || 'male'
      }
      // Ensure dependent lists are populated for display
      try {
        if (profileForm.value.province_id) {
          await fetchDistricts(String(profileForm.value.province_id))
        }
        if (profileForm.value.district_id) {
          await fetchWards(String(profileForm.value.district_id))
        }
      } catch (_) {}
      console.log('Profile form populated from auth store:', profileForm.value)
    }
    
    // Then try to refresh from API
    try {
      console.log('Fetching fresh data from API...')
      const profileData = await customersService.getProfile()
      console.log('Profile data received:', profileData)
      
      if (profileData?.customer) {
        const customer = profileData.customer
        console.log('Customer data:', customer)
        profileForm.value = {
          first_name: customer.first_name || '',
          last_name: customer.last_name || '',
          email: customer.email || '',
          username: customer.username || customer.email || '',
          nickname: customer.nickname || '',
          website: customer.website || '',
          bio: customer.bio || '',
          avatar: customer.avatar || '',
          phone: customer.phone || '',
          address: customer.address || '',
          province_id: customer.province_id || '',
          district_id: customer.district_id || '',
          ward_id: customer.ward_id || '',
          date_of_birth: customer.date_of_birth || '',
          gender: customer.gender || 'male'
        }
        try {
          if (profileForm.value.province_id) {
            await fetchDistricts(String(profileForm.value.province_id))
          }
          if (profileForm.value.district_id) {
            await fetchWards(String(profileForm.value.district_id))
          }
        } catch (_) {}
        console.log('Profile form updated from API:', profileForm.value)
      }
    } catch (apiError) {
      console.warn('API call failed, using auth store data:', apiError)
    }
    
  } catch (error) {
    console.error('Error loading profile:', error)
    $toast.error('Không thể tải thông tin hồ sơ')
  }
}

const updateProfile = async () => {
  try {
    loading.value = true
    
    // Call API to update profile
    const result = await customersService.updateProfile(profileForm.value)
    
    if (result?.customer) {
      // Update the auth store with new data
      auth.user = result.customer
      
      // Update profileForm with the latest data from server
      const customer = result.customer
      profileForm.value = {
        first_name: customer.first_name || '',
        last_name: customer.last_name || '',
        email: customer.email || '',
        username: customer.username || customer.email || '',
        nickname: customer.nickname || '',
        website: customer.website || '',
        bio: customer.bio || '',
        avatar: customer.avatar || '',
        phone: customer.phone || '',
        address: customer.address || '',
        date_of_birth: customer.date_of_birth || '',
        gender: customer.gender || 'male'
      }
      
      $toast.success('Cập nhật hồ sơ thành công!')
    }
  } catch (error) {
    console.error('Error updating profile:', error)
    // Check if there's a specific error message
    if (error?.data?.error) {
      $toast.error(error.data.error)
    } else if (error?.data?.message) {
      $toast.error(error.data.message)
    } else if (error?.message) {
      $toast.error(error.message)
    } else {
      $toast.error('Không thể cập nhật hồ sơ')
    }
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  loadProfile()
}

// Edit field methods
const toggleEdit = (fieldName) => {
  if (editingField.value === fieldName) {
    // Cancel editing
    editingField.value = null
    // Restore original value
    if (originalValues.value[fieldName] !== undefined) {
      profileForm.value[fieldName] = originalValues.value[fieldName]
    }
  } else {
    // Start editing
    editingField.value = fieldName
    // Save original value
    originalValues.value[fieldName] = profileForm.value[fieldName]
  }
}

const cancelEdit = () => {
  if (editingField.value && originalValues.value[editingField.value] !== undefined) {
    profileForm.value[editingField.value] = originalValues.value[editingField.value]
  }
  editingField.value = null
  originalValues.value = {}
}

const saveField = async (fieldName) => {
  try {
    loading.value = true
    
    // Create update payload with only the changed field
    const updateData: any = {}
    if (fieldName === 'location') {
    updateData.province_id = profileForm.value.province_id ? String(profileForm.value.province_id) : ''
    updateData.district_id = profileForm.value.district_id ? String(profileForm.value.district_id) : ''
    updateData.ward_id = profileForm.value.ward_id ? String(profileForm.value.ward_id) : ''
    } else {
      updateData[fieldName] = (profileForm.value as any)[fieldName]
    }
    
    // Call API to update profile
    const result = await customersService.updateProfile(updateData)
    
    if (result?.customer) {
      // Update the auth store with new data
      auth.user = result.customer
      
      // Update profileForm with the latest data from server
      const customer = result.customer
      profileForm.value = {
        first_name: customer.first_name || '',
        last_name: customer.last_name || '',
        email: customer.email || '',
        username: customer.username || customer.email || '',
        nickname: customer.nickname || '',
        website: customer.website || '',
        bio: customer.bio || '',
        avatar: customer.avatar || '',
        phone: customer.phone || '',
        address: customer.address || '',
        province_id: customer.province_id || '',
        district_id: customer.district_id || '',
        ward_id: customer.ward_id || '',
        date_of_birth: customer.date_of_birth || '',
        gender: customer.gender || 'male'
      }
      
      if ($toast && (typeof $toast.success === 'function')) {
        $toast.success('Cập nhật thành công!')
      } else {
        console.log('Cập nhật thành công!')
      }
    }
  } catch (err) {
    console.error('Error updating field:', err)
    const anyErr: any = err as any
    const msg = (anyErr && (anyErr.data?.error || anyErr.data?.message || anyErr.message)) || 'Không thể cập nhật thông tin'
    if ($toast && (typeof $toast.error === 'function')) {
      $toast.error(msg)
    } else {
      console.error(msg)
    }
    
    // Always restore original value on error
    if (fieldName === 'location') {
      // Restore location as a group if backed up individually isn't available
      // No-op if not stored; user can reselect
    } else if (originalValues.value[fieldName] !== undefined) {
      profileForm.value[fieldName] = originalValues.value[fieldName]
    }
  } finally {
    // Always clear editing state regardless of success or failure
    loading.value = false
    editingField.value = null
    originalValues.value = {}
  }
}

const handleImageUpload = async (event: any) => {
  const file = event.target.files && event.target.files[0]
  if (!file) return
  const reader = new FileReader()
  reader.onload = async (e: any) => {
    const base64 = e?.target?.result
    if (!base64) return
    profileForm.value.avatar = base64
    try {
      // Save avatar immediately and sync auth store with backend response
      const result = await customersService.updateProfile({ avatar: base64 })
      if (result && (result as any).customer) {
        const customer = (result as any).customer
        auth.user = customer
        profileForm.value.avatar = customer.avatar || base64
      }
      if ($toast && (typeof $toast.success === 'function')) $toast.success('Ảnh đại diện đã được cập nhật')
      // Exit edit mode after successful upload
      if (editingField.value === 'avatar') {
        editingField.value = null
        originalValues.value = {}
      }
    } catch (err) {
      const anyErr: any = err as any
      const msg = (anyErr && (anyErr.data?.error || anyErr.data?.message || anyErr.message)) || 'Không thể cập nhật ảnh'
      if ($toast && (typeof $toast.error === 'function')) $toast.error(msg)
    }
  }
  reader.readAsDataURL(file)
}

// Password change methods
const togglePasswordForm = () => {
  showPasswordForm.value = !showPasswordForm.value
  if (!showPasswordForm.value) {
    // Clear form when hiding
    passwordForm.value = {
      current_password: '',
      new_password: '',
      confirm_password: ''
    }
  }
}

const cancelPasswordChange = () => {
  resetPasswordForm()
}

const changePassword = async () => {
  try {
    loading.value = true
    
    // Validation
    if (!passwordForm.value.current_password) {
      $toast.error('Vui lòng nhập mật khẩu hiện tại')
      loading.value = false
      return
    }
    
    if (!passwordForm.value.new_password) {
      $toast.error('Vui lòng nhập mật khẩu mới')
      loading.value = false
      return
    }
    
    if (passwordForm.value.new_password.length < 6) {
      $toast.error('Mật khẩu mới phải có ít nhất 6 ký tự')
      loading.value = false
      return
    }
    
    if (passwordForm.value.new_password !== passwordForm.value.confirm_password) {
      $toast.error('Mật khẩu xác nhận không khớp')
      loading.value = false
      return
    }
    
    // Call API to change password
    const result = await customersService.changePassword({
      current_password: passwordForm.value.current_password,
      new_password: passwordForm.value.new_password
    })
    
    console.log('Password change result:', result)
    if ($toast && typeof $toast.success === 'function') {
      $toast.success('Đổi mật khẩu thành công!')
    }
    
    // Clear form and hide - always do this on success
    resetPasswordForm()
    
  } catch (error) {
    console.error('Error changing password:', error)
    const anyErr: any = error as any
    // Handle unauthorized explicitly
    if (anyErr?.statusCode === 401) {
      $toast.error('Phiên đăng nhập đã hết hạn. Vui lòng đăng nhập lại.')
      try { await navigateTo('/auth/login') } catch (_) {}
    } else {
      const msg = (anyErr && (anyErr.data?.error || anyErr.data?.message || anyErr.message)) || 'Không thể đổi mật khẩu'
      $toast.error(msg)
    }
  } finally {
    loading.value = false
  }
}

// Helper function to reset password form
const resetPasswordForm = () => {
  passwordForm.value = {
    current_password: '',
    new_password: '',
    confirm_password: ''
  }
  showPasswordForm.value = false
  console.log('Password form reset and hidden')
}

const logout = async () => {
  try {
    auth.logout()
    await navigateTo('/auth/login')
    $toast.success('Đăng xuất thành công')
  } catch (error) {
    console.error('Logout error:', error)
  }
}

// Lifecycle
onMounted(() => {
  loadProfile()
})

// --- Vietnam Province API for profile ---
const provinces = ref<any[]>([])
const districts = ref<any[]>([])
const wards = ref<any[]>([])
const loadingProvinces = ref(false)
const loadingDistricts = ref(false)
const loadingWards = ref(false)

async function fetchProvinces() {
  loadingProvinces.value = true
  try {
    const res = await fetch('https://provinces.open-api.vn/api/')
    provinces.value = await res.json()
  } catch (e) {
    // ignore
  } finally {
    loadingProvinces.value = false
  }
}

async function fetchDistricts(provinceCode: string) {
  if (!provinceCode) { districts.value = []; wards.value = []; return }
  loadingDistricts.value = true
  try {
    const res = await fetch(`https://provinces.open-api.vn/api/p/${provinceCode}?depth=2`)
    const data = await res.json()
    districts.value = data?.districts || []
    wards.value = []
  } catch (e) {
    // ignore
  } finally {
    loadingDistricts.value = false
  }
}

async function fetchWards(districtCode: string) {
  if (!districtCode) { wards.value = []; return }
  loadingWards.value = true
  try {
    const res = await fetch(`https://provinces.open-api.vn/api/d/${districtCode}?depth=2`)
    const data = await res.json()
    wards.value = data?.wards || []
  } catch (e) {
    // ignore
  } finally {
    loadingWards.value = false
  }
}

function onProvinceChange() {
  fetchDistricts(profileForm.value.province_id as any)
  profileForm.value.district_id = ''
  profileForm.value.ward_id = ''
}

function onDistrictChange() {
  fetchWards(profileForm.value.district_id as any)
  profileForm.value.ward_id = ''
}

onMounted(() => {
  fetchProvinces()
})
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