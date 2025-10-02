<template>
  <NuxtLoadingIndicator></NuxtLoadingIndicator>
  <div class="h-screen w-full flex justify-center items-center">
      <div class="lg:pt-7 pt-3 lg:px-12 px-6 lg:w-2/3 w-full lg:min-w-[800px] bg-white rounded-lg drop-shadow-md">
          <main class="w-full">
              <div class="w-full md:max-w-[550px] max-w-[360px] mx-auto min-h-[256px]">
                  <div class="flex text-center justify-center text-primary">
                      <IconAmoz style="width: auto; height: 100px" />
                  </div>
                  <div v-if="isSubmitted" class="mt-5 pb-5 ">
                      <p class="text-center">{{ $t('Password reset link sent to', { email: forgotPasswordForm.email }) }}</p>
                  </div>
                  <div v-else class="mt-5">
                      <h3 class="lg:text-2xl text-xl text-center font-bold">
                          {{ $t('Forgot your password?') }}
                      </h3>
                      <el-form class="mt-12 gap-2" ref="forgotPasswordFormRef" label-width="auto" :model="forgotPasswordForm"
                          :size="formSize" :rules="rules">
                          <el-form-item prop="email">
                              <el-input placeholder="Email" v-model="forgotPasswordForm.email" type="email" />
                          </el-form-item>
                          <div class="flex justify-center items-center mt-10">
                              <el-button @click="sendLink(forgotPasswordFormRef)" :class="isDisabled ? 'disabled-btn' : ''" v-loading="isLoading" :disabled="isDisabled"
                                  class="flex rounded-lg h-[32px] p-5 font-bold border bg-primary hover:bg-white text-white hover:text-primary hover:border-primary justify-center items-center">
                                  {{ $t('Send reset link') }}
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
import IconAmoz from '~/assets/icons/BigLogo.svg'
import OAuthService from '@/services/oauth';
import { ElNotification } from 'element-plus'
import { ref, watch } from 'vue'

definePageMeta({
  layout: 'anonymous'
})

import type { ComponentSize, FormInstance, FormRules } from 'element-plus'
const formSize = ref<ComponentSize>('default')
const forgotPasswordFormRef = ref<FormInstance>()
const forgotPasswordForm = ref({
  email: ''
})

const rules = reactive<FormRules>({
  email: [
      { required: true, message: 'Please enter your email', trigger: 'blur' },
      { type: 'email', message: 'Invalid email format', trigger: ['blur', 'change'] },
  ]
})

const isFormValid = ref(false)
const isDisabled = ref(true)
const validateForm = () => {
  forgotPasswordFormRef.value?.validate((valid) => {
      isDisabled.value = !valid
  })
  return true
}
watch(forgotPasswordForm, validateForm, { deep: true })
validateForm()
const isSubmitted = ref(false)
const isLoading = ref(false)

const sendLink = async (formInstance: FormInstance | undefined) => {
  if (!formInstance) return
  await formInstance.validate(async (valid, fields) => {
      if (valid) {
          isLoading.value = true
          try {
              await OAuthService.forgotPassword({ email: forgotPasswordForm.value.email })
              isSubmitted.value = true
              ElNotification({
                  title: 'Success',
                  message: 'Password reset link sent successfully',
                  type: 'success',
                  duration: 5000
              })
          } catch (error) {
              ElNotification({
                  title: 'Error',
                  message: 'Email does not exist or there was an error sending the reset link',
                  type: 'error',
                  duration: 5000
              })
          } finally {
              isLoading.value = false
          }
      } else {
          console.log('error submit!', fields)
      }
  })
}
</script>

<style scoped>
a {
  text-decoration: none;
}
.disabled-btn {
  @apply border-surface-dim bg-surface-dim text-white hover:bg-surface-dim hover:text-white
}
</style>
