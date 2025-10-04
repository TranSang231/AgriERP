<template>
  <div class="relative">
    <select
      v-model="locale"
      class="cursor-pointer rounded border border-gray-300 bg-white px-3 py-2 text-gray-600 focus:outline-none focus:ring-2 focus:ring-orange-500"
    >
      <option v-for="lang in availableLocales" :key="lang.code" :value="lang.code">
        {{ lang.name }}
      </option>
    </select>
  </div>
</template>

<script setup lang="ts">
import { computed, watch, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'

const { locale, locales } = useI18n()

const availableLocales = computed(() => {
  if (Array.isArray(locales.value)) {
    return (locales.value as { code: string; name: string }[]).filter(i => i.code && i.name)
  }
  return []
})

onMounted(() => {
  console.log('Initial locale:', locale.value)
  console.log('Available locales:', locales.value)
})

watch(locale, (newLocale) => {
  console.log('Locale changed to:', newLocale)
})
</script>