<template>
  <div class="flex flex-col" @click.stop>
    <div class="flex flex-row items-center min-w-45 cursor-pointer" @click="toggleDetail">
      <el-avatar v-if="showAvatar" :icon="UserFilled" class="mx-2" />
      <p>{{ currentUser ? `${currentUser.first_name}` : 'Anonymous' }}</p>
      <p class="hidden sm:block pl-1">{{ currentUser ? `${currentUser.last_name}` : 'User' }}</p>
    </div>
    <div v-if="!isCollapse"
      class="absolute w-100 mt-12 drop-shadow bg-white border-1 border-solid, border-primary rounded">
      <div class="px-6 py-2 hover:bg-primary hover:text-white">
        <NuxtLink to="/change-password"><span>{{ $t('change_password') }}</span></NuxtLink>
      </div>
      <div class="px-6 py-2  hover:bg-primary hover:text-white" @click="logout"><span>Logout</span></div>
    </div>
  </div>
</template>

<script setup>
import { UserFilled } from '@element-plus/icons-vue'
import { useOauthStore } from '@/stores/oauth';
const { $api } = useNuxtApp()
import OAuthService from '@/services/oauth';

const props = defineProps({
  showAvatar: {
    type: Boolean,
    default: true
  },
})

const isCollapse = ref(true)

const toggleDetail = () => {
  isCollapse.value = !isCollapse.value;
}

const store = useOauthStore()
const currentUser = computed(() => {
  const { user } = store;
  return user;
})

const logout = async () => {
  OAuthService.logout()
    .then(response => {
      store.$reset()
    })
    .catch(error => {
      console.log(error);
      store.$reset()
    })
    .finally(() => {
      navigateTo("/");
    })
}

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