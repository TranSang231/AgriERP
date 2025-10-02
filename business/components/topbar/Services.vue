<template>
  <div class="flex flex-col" @click.stop>
    <div class="flex flex-row items-center min-w-45" @click="toggleDetail">
      <IconServices width="24" height="24" class="text-primary" />
    </div>
    <div v-if="!isCollapse" class="absolute self-center grid grid-cols-3 gap-2 text-sm mt-12 p-2 drop-shadow bg-white border-1 border-solid, border-primary rounded">
      <NuxtLink to="/websites" class="flex flex-col items-center align-top text-center">
        <IconWebsite width="28" height="28" class="text-primary"/>
        <span>Website</span>
      </NuxtLink>
      <NuxtLink to="/e-commerce" class="flex flex-col items-center align-top text-center">
        <IconEComerce width="28" height="28" class="text-primary"/>
        <span>{{ t('E_commerce') }}</span>
      </NuxtLink>
      <NuxtLink to="/hrm" class="flex flex-col items-center align-top text-center">
        <IconHumanResource width="28" height="28" class="text-primary"/>
        <span>{{ t('Human_resources') }}</span>
      </NuxtLink>
      <NuxtLink to="/va" class="flex flex-col items-center align-top text-center">
        <IconCRM width="28" height="28" class="text-primary"/>
        <span>{{ t('Virtual_assistants') }}</span>
      </NuxtLink>
      <NuxtLink to="/knowledge" class="flex flex-col items-center align-top text-center">
        <IconCafe width="28" height="28" class="text-primary"/>
        <span>{{ t('Knowledge') }}</span>
      </NuxtLink>
    </div>
  </div>
</template>

<script setup>
import IconServices from '@/assets/icons/services.svg';
import IconWebsite from '@/assets/icons/website.svg';
import IconEComerce from '@/assets/icons/e-commerce.svg';
import IconHumanResource from '@/assets/icons/human-resource.svg';
import IconCRM from '@/assets/icons/crm.svg';
import IconCafe from '@/assets/icons/cafe.svg';

const { t } = useI18n();

//Todo fetch and show the apps base on business's subscrition
const isCollapse = ref(true)

const toggleDetail = () => {
  isCollapse.value = !isCollapse.value;
}

//Todo handle event close when click outside the element
function handleClickOutside(event) {
  const dropdownElement = document.querySelector(".flex.flex-col");
  if (!dropdownElement.contains(event.target)) {
    isCollapse.value = true;
  }
}

onMounted(() => {
  document.addEventListener("click", handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener("click", handleClickOutside);
});
</script>