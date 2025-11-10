import { defineStore } from "pinia";
import {
  useProductsService,
  type Product,
  type ProductCategory,
  type ProductFilter,
  type ProductResponse,
} from "~/services/products";

interface ProductsState {
  products: Product[];
  categories: ProductCategory[];
  currentProduct: Product | null;
  loading: boolean;
  error: string | null;
  pagination: {
    count: number;
    next: string | null;
    previous: string | null;
    currentPage: number;
    pageSize: number;
  };
  filters: ProductFilter;
}

export const useProductsStore = defineStore("products", {
  state: (): ProductsState => ({
    products: [],
    categories: [],
    currentProduct: null,
    loading: false,
    error: null,
    pagination: {
      count: 0,
      next: null,
      previous: null,
      currentPage: 1,
      pageSize: 20,
    },
    filters: {
      page: 1,
      page_size: 20,
    },
  }),

  getters: {
    featuredProducts: (state) =>
      state.products.filter((p) => p.is_active).slice(0, 8),
    productsByCategory: (state) => (categoryId: number) =>
      state.products.filter((p) => p.category.id === categoryId),
    totalPages: (state) =>
      Math.ceil(state.pagination.count / state.pagination.pageSize),
    hasNextPage: (state) => state.pagination.next !== null,
    hasPreviousPage: (state) => state.pagination.previous !== null,
  },

  actions: {
    async fetchProducts(filters: ProductFilter = {}) {
      this.loading = true;
      this.error = null;

      try {
        const { getProducts } = useProductsService();
        const { data } = await getProducts({ ...this.filters, ...filters });

        if (data.value) {
          const response = data.value as any;
          this.products = response.results || [];
          this.pagination.count = response.count || 0;
          this.pagination.next = response.next || null;
          this.pagination.previous = response.previous || null;
          this.pagination.currentPage = filters.page || this.filters.page || 1;
        }
      } catch (error: any) {
        this.error = error.message || "Failed to fetch products";
      } finally {
        this.loading = false;
      }
    },

    async fetchProductById(id: number) {
      this.loading = true;
      this.error = null;

      try {
        const { getProductById } = useProductsService();
        const { data } = await getProductById(id);

        if (data.value) {
          this.currentProduct = data.value as any;
        }
      } catch (error: any) {
        this.error = error.message || "Failed to fetch product";
      } finally {
        this.loading = false;
      }
    },

    async fetchCategories() {
      try {
        const { getCategories } = useProductsService();
        const { data } = await getCategories();

        if (data.value) {
          this.categories = data.value as any;
        }
      } catch (error: any) {
        this.error = error.message || "Failed to fetch categories";
      }
    },

    async searchProducts(search: string) {
      await this.fetchProducts({ ...this.filters, search, page: 1 });
    },

    async filterByCategory(categoryId: number) {
      await this.fetchProducts({
        ...this.filters,
        category: String(categoryId),
        page: 1,
      });
    },

    async filterByPrice(minPrice?: number, maxPrice?: number) {
      await this.fetchProducts({
        ...this.filters,
        min_price: minPrice,
        max_price: maxPrice,
        page: 1,
      });
    },

    async sortProducts(ordering: string) {
      await this.fetchProducts({ ...this.filters, ordering, page: 1 });
    },

    async loadMore() {
      if (this.hasNextPage) {
        await this.fetchProducts({
          ...this.filters,
          page: this.pagination.currentPage + 1,
        });
      }
    },

    setFilters(filters: ProductFilter) {
      this.filters = { ...this.filters, ...filters };
    },

    clearFilters() {
      this.filters = { page: 1, page_size: 20 };
      this.fetchProducts();
    },

    clearCurrentProduct() {
      this.currentProduct = null;
    },
  },

  persist: true,
});
