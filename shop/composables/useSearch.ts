import { ref } from "vue";
import { useRouter } from "vue-router";

export const useSearch = () => {
  const router = useRouter();
  const searchQuery = ref("");
  const isSearching = ref(false);

  const performSearch = async (query?: string) => {
    const searchTerm = query || searchQuery.value;
    if (!searchTerm.trim()) return;

    isSearching.value = true;
    try {
      await router.push({
        path: "/products",
        query: { search: searchTerm.trim() },
      });
    } finally {
      isSearching.value = false;
    }
  };

  const clearSearch = () => {
    searchQuery.value = "";
  };

  return {
    searchQuery,
    isSearching,
    performSearch,
    clearSearch,
  };
};
