<template>
  <div class="w-full absolute space-x-* bg-on-primary flex flex-row align-middle py-2 px-8 justify-between border-b border-gray-200 z-10">
    <NuxtLink to="/" class="flex flex-row items-center">
      <AmozLogo class="mx-1 h-8 min-w-8 pl-10" />
      <span class="hidden sm:block text-black self-center text-2xl font-semibold whitespace-nowrap">Alpha</span>
    </NuxtLink>
    <div class="flex flex-row items-center gap-2">
      <slot name="right" />
      <Services v-if="authenticated" />
      <CurrentUser v-if="authenticated" />
      <LanguageSelector />
    </div>
  </div>
</template>

<script lang="ts" setup>
import AmozLogo from "~/assets/icons/Logo.svg";
import Services from './Services.vue';
import CurrentUser from './CurrentUser.vue';
import LanguageSelector from './LanguageSelector.vue'
import { useOauthStore } from '@/stores/oauth';
const oauthStore = useOauthStore()
const authenticated = computed(() => {
    const { tokenInfo } = oauthStore;
    if (!tokenInfo) return false;
    const { access_token } = tokenInfo;
    if (!access_token) return false;
    return access_token.length > 0;
})

</script>