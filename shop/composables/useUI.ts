import { ref } from "vue";

export const useUI = () => {
  const isLoading = ref(false);
  const showUserMenu = ref(false);
  const showMobileMenu = ref(false);

  const setLoading = (loading: boolean) => {
    isLoading.value = loading;
  };

  const toggleUserMenu = () => {
    showUserMenu.value = !showUserMenu.value;
    showMobileMenu.value = false;
  };

  const toggleMobileMenu = () => {
    showMobileMenu.value = !showMobileMenu.value;
    showUserMenu.value = false;
  };

  const closeMenus = () => {
    showUserMenu.value = false;
    showMobileMenu.value = false;
  };

  return {
    isLoading,
    showUserMenu,
    showMobileMenu,
    setLoading,
    toggleUserMenu,
    toggleMobileMenu,
    closeMenus,
  };
};
