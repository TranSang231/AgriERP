<template>
  <div class="relative">
    <select
      v-model="selectedLanguage"
      class="cursor-pointer rounded border border-gray-300 bg-white px-3 py-2 text-gray-600 focus:outline-none focus:ring-2 focus:ring-orange-500"
    >
      <option v-for="lang in localeStore.supportedLanguages" :key="lang.code" :value="lang">
        {{ lang.name }}
      </option>
    </select>
  </div>
</template>

<script setup lang="ts">
import { computed, watch, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useLocaleStore } from '@/stores/locale'
import { useNuxtApp } from 'nuxt/app'

const { locale } = useI18n()
const localeStore = useLocaleStore()
const { $i18n } = useNuxtApp()

// Sync with i18n locale
if (locale && localeStore && locale.value !== localeStore.currentLangue.code) {
  ($i18n as any).setLocale(localeStore.currentLangue.code);
}

const selectedLanguage = computed({
  get: () => localeStore.currentLangue,
  set: (newLang) => {
    localeStore.setCurrentLangue(newLang);
    ($i18n as any).setLocale(newLang.code);
  }
})

onMounted(() => {
  console.log('Initial locale:', locale.value)
  console.log('Current language:', localeStore.currentLangue)
})

watch(selectedLanguage, (newLang) => {
  console.log('Language changed to:', newLang)
})
</script>