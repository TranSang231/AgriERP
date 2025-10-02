<template>
  <div class="h-screen w-full flex justify-center items-center">
    <div class="lg:pt-7 pt-3 lg:px-12 px-6 lg:w-2/3 w-full lg:min-w-[800px] bg-white rounded-lg drop-shadow-md">
      <main class="w-full">
        <div class="w-full md:max-w-[550px] max-w-[360px] mx-auto min-h-[256px]">
          <h3 class="lg:text-2xl text-xl text-center font-bold">
            {{ $t('Change Your Password') }}
          </h3>
          <el-form
            class="mt-12 gap-2"
            ref="changePasswordFormRef"
            label-width="auto"
            :model="changePasswordForm"
            :size="formSize"
            :rules="rules"
          >
            <el-form-item prop="currentPassword">
              <el-input
                placeholder="Current Password"
                v-model="changePasswordForm.currentPassword"
                type="password"
              />
            </el-form-item>
            <el-form-item prop="newPassword">
              <el-input
                placeholder="New Password"
                v-model="changePasswordForm.newPassword"
                type="password"
              />
            </el-form-item>
            <el-form-item prop="confirmNewPassword">
              <el-input
                placeholder="Confirm New Password"
                v-model="changePasswordForm.confirmNewPassword"
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
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ElNotification } from 'element-plus'
import { ref, reactive, watch } from 'vue'
import type { ComponentSize, FormInstance, FormRules } from 'element-plus'

const formSize = ref<ComponentSize>('default')
const changePasswordFormRef = ref<FormInstance>()
const changePasswordForm = ref({
  currentPassword: '',
  newPassword: '',
  confirmNewPassword: ''
})

const rules = reactive<FormRules>({
  currentPassword: [
    { required: true, message: 'Please enter your current password', trigger: 'blur' }
  ],
  newPassword: [
    { required: true, message: 'Please enter your new password', trigger: 'blur' },
    { min: 6, message: 'The new password must be at least 6 characters long', trigger: 'blur' }
  ],
  confirmNewPassword: [
    { required: true, message: 'Please confirm your new password', trigger: 'blur' },
    { validator: validateConfirmNewPassword, trigger: 'blur' }
  ]
})

const isDisabled = ref(true)
const isLoading = ref(false)

function validateConfirmNewPassword(rule: any, value: string, callback: (error?: Error) => void) {
  if (value !== changePasswordForm.value.newPassword) {
    callback(new Error('Passwords do not match'))
  } else {
    callback()
  }
}

const validateForm = () => {
  changePasswordFormRef.value?.validate((valid: boolean) => {
    isDisabled.value = !valid
  })
}
watch(changePasswordForm, validateForm, { deep: true })
validateForm()

const changePassword = async () => {
  await changePasswordFormRef.value?.validate(async (valid: boolean, fields: any) => {
    if (valid) {
      isLoading.value = true
      try {
        // Thực hiện thao tác thay đổi mật khẩu ở đây nếu cần
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
    } else {
      console.log('Validation failed:', fields)
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
