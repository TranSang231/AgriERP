<template>
  <div class="w-full absolute space-x-* bg-on-primary flex flex-row align-middle py-2 px-8 justify-between border-b border-gray-200 z-10">
    <NuxtLink to="/" class="flex flex-row items-center">
      <AmozLogo class="mx-1 h-8 min-w-8 pl-10" />
      <span class="hidden sm:block text-black self-center text-2xl font-semibold whitespace-nowrap">Alpha</span>
    </NuxtLink>
    <div class="flex flex-row items-center gap-2">
      <LanguageSelector />
    </div>
  </div>
</template>

<script lang="ts" setup>
import AmozLogo from "~/assets/icons/Logo.svg";
import LanguageSelector from './LanguageSelector.vue'
</script>