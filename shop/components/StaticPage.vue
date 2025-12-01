<template>
  <section class="max-w-4xl mx-auto w-full px-4 py-10 space-y-6">
    <nav class="flex items-center gap-2 text-sm text-gray-500">
      <NuxtLink to="/" class="text-primary hover:text-primary-600">
        {{ t('staticPages.common.breadcrumbs.home') }}
      </NuxtLink>
      <span>/</span>
      <span class="text-gray-700">{{ pageName }}</span>
    </nav>

    <div class="bg-white border border-gray-100 shadow-sm rounded-2xl p-8 space-y-4">
      <p class="text-sm font-semibold uppercase tracking-wide text-primary">
        {{ t('staticPages.common.intro') }}
      </p>
      <h1 class="text-3xl font-bold text-gray-900">{{ title }}</h1>
      <p class="text-gray-600 leading-relaxed">{{ description }}</p>
    </div>

    <div class="bg-primary/5 border border-primary/20 rounded-2xl p-6 text-primary-900">
      {{ t('staticPages.common.comingSoon') }}
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useHead } from 'nuxt/app'
import { useI18n } from 'vue-i18n'

const props = defineProps<{ pageKey: 'about' | 'contact' | 'help' | 'shipping' | 'returns' | 'faq' }>()

const { t } = useI18n()

const prefix = computed(() => `staticPages.${props.pageKey}`)
const pageName = computed(() => t(`${prefix.value}.pageName`))
const title = computed(() => t(`${prefix.value}.title`))
const description = computed(() => t(`${prefix.value}.description`))
const headTitle = computed(() => t(`${prefix.value}.headTitle`))
const metaDescription = computed(() => t(`${prefix.value}.metaDescription`))

useHead(() => ({
  title: headTitle.value,
  meta: [
    {
      name: 'description',
      content: metaDescription.value || description.value,
    },
  ],
}))
</script>
