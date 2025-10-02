<template>
    <div class="h-screen w-full flex justify-center items-center">
      <div class="lg:pt-7 pt-3 lg:px-12 px-6 lg:w-2/3 w-full lg:min-w-[800px] bg-white rounded-lg drop-shadow-md">
        <main class="w-full">
          <div class="w-full md:max-w-[550px] max-w-[360px] mx-auto min-h-[256px]">
            <div class="flex text-center justify-center text-primary">
              <IconAmoz style="width: auto; height: 100px" />
            </div>
            <div v-if="isSubmitted" class="mt-5 pb-5">
              <p class="text-center">{{ $t('Password reset successfully') }}</p>
            </div>
            <div v-else class="mt-5">
              <h3 class="lg:text-2xl text-xl text-center font-bold">
                {{ $t('Reset Your Password') }}
              </h3>
              <el-form
                class="mt-12 gap-2"
                ref="resetPasswordFormRef"
                label-width="auto"
                :model="resetPasswordForm"
                :size="formSize"
                :rules="rules"
              >
                <el-form-item prop="password">
                  <el-input
                    placeholder="New Password"
                    v-model="resetPasswordForm.password"
                    type="password"
                  />
                </el-form-item>
                <el-form-item prop="confirmPassword">
                  <el-input
                    placeholder="Confirm New Password"
                    v-model="resetPasswordForm.confirmPassword"
                    type="password"
                  />
                </el-form-item>
                <div class="flex justify-center items-center mt-10">
                  <el-button
                    @click="changePassword"
                    :class="isDisabled ? 'disabled-btn' : ''"
                    v-loading="isLoading"
                    :disabled="isDisabled"
                    class="flex rounded-lg h-[32px] p-5 font-bold border bg-primary hover:bg-white text-white hover:text-primary hover:border-primary justify-center items-center"
                  >
                    {{ $t('Change Password') }}
                  </el-button>
                </div>
              </el-form>
            </div>
            <div class="flex justify-center pt-12 mb-5">
              <NuxtLink to="/" class="text-primary underline">
                {{ $t('Back to login') }}
              </NuxtLink>
            </div>
          </div>
        </main>
      </div>
    </div>
  </template>
  
  <script setup lang="ts">
  import { useRoute } from 'vue-router'
  import IconAmoz from '~/assets/icons/BigLogo.svg'
  import OAuthService from '@/services/oauth';
  import { ElNotification } from 'element-plus'
  import { ref, watch } from 'vue'
  
  definePageMeta({
    layout: 'anonymous' // Không yêu cầu xác thực
  })
  
  import type { ComponentSize, FormInstance, FormRules } from 'element-plus'
  const formSize = ref<ComponentSize>('default')
  const resetPasswordFormRef = ref<FormInstance>()
  const resetPasswordForm = ref({
    password: '',
    confirmPassword: ''
  })
  
  const rules = reactive<FormRules>({
  password: [
    { required: true, message: 'Please enter your new password', trigger: 'blur' },
    { min: 6, message: 'Password must be at least 6 characters', trigger: 'blur' }, 
  ],
  confirmPassword: [
    { required: true, message: 'Please confirm your new password', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' },
  ]
})

  
  const isDisabled = ref(true)
  const isSubmitted = ref(false)
  const isLoading = ref(false)
  
  function validateConfirmPassword(rule: any, value: string, callback: (error?: Error) => void) {
    if (value !== resetPasswordForm.value.password) {
      callback(new Error('Passwords do not match'))
    } else {
      callback()
    }
  }
  
  const validateForm = () => {
    resetPasswordFormRef.value?.validate((valid) => {
      isDisabled.value = !valid
    })
  }
  watch(resetPasswordForm, validateForm, { deep: true })
  validateForm()
  
  const route = useRoute() // Chuyển useRoute() vào setup()
  
  const changePassword = async () => {
    await resetPasswordFormRef.value?.validate(async (valid) => {
      if (valid) {
        isLoading.value = true
        try {
          const token = route.query.token as string
          await OAuthService.setPassword(token, resetPasswordForm.value.password)
          isSubmitted.value = true
          ElNotification({
            title: 'Success',
            message: 'Your password has been changed successfully',
            type: 'success',
            duration: 5000
          })
        } catch (error) {
          ElNotification({
            title: 'Error',
            message: 'There was an error changing your password',
            type: 'error',
            duration: 5000
          })
        } finally {
          isLoading.value = false
        }
      }
    })
  }
  </script>
  