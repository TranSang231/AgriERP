import { defineStore } from "pinia";
import {
  useProductsService,
  type Product,
  type ProductCategory,
  type ProductFilter,
  type ProductResponse,
  type ShopStats,
} from "~/services/products";

interface ProductsState {
  products: Product[];
  featuredProducts: Product[];
  onSaleProducts: Product[];
  newArrivals: Product[];
  categories: ProductCategory[];
  categoriesWithProducts: ProductCategory[];
  currentProduct: Product | null;
  shopStats: ShopStats | null;
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
    featuredProducts: [],
    onSaleProducts: [],
    newArrivals: [],
    categories: [],
    categoriesWithProducts: [],
    currentProduct: null,
    shopStats: null,
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
    productsOnSale: (state) => state.onSaleProducts,
    totalPages: (state) =>
      Math.ceil(state.pagination.count / state.pagination.pageSize),
    hasNextPage: (state) => state.pagination.next !== null,
    hasPreviousPage: (state) => state.pagination.previous !== null,
    activeCategories: (state) =>
      state.categoriesWithProducts.filter(
        (cat) => cat.active_product_count && cat.active_product_count > 0
      ),
    priceRange: (state) =>
      state.shopStats?.price_range || { min: 0, max: 1000, average: 0 },
  },

  actions: {
    // Main product fetching with advanced filters
    async fetchProducts(filters: ProductFilter = {}) {
      this.loading = true;
      this.error = null;

      try {
        const { getProducts } = useProductsService();
        const { data } = await getProducts({ ...this.filters, ...filters });

        if (data.value) {
          const response = data.value as ProductResponse;
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

    // Fetch products with advanced filtering
    async fetchProductsWithFilters(filters: ProductFilter) {
      this.loading = true;
      this.error = null;

      try {
        const { getProductsWithAdvancedFilters } = useProductsService();
        const { data } = await getProductsWithAdvancedFilters(filters);

        if (data.value) {
          const response = data.value as ProductResponse;
          this.products = response.results || [];
          this.pagination.count = response.count || 0;
          this.pagination.next = response.next || null;
          this.pagination.previous = response.previous || null;
          this.pagination.currentPage = filters.page || 1;
        }
      } catch (error: any) {
        this.error = error.message || "Failed to fetch filtered products";
      } finally {
        this.loading = false;
      }
    },

    // Fetch featured products
    async fetchFeaturedProducts() {
      try {
        const { getFeaturedProducts } = useProductsService();
        const { data } = await getFeaturedProducts();

        if (data.value) {
          this.featuredProducts = data.value as Product[];
        }
      } catch (error: any) {
        this.error = error.message || "Failed to fetch featured products";
      }
    },

    // Fetch products on sale
    async fetchOnSaleProducts(filters: ProductFilter = {}) {
      try {
        const { getProductsOnSale } = useProductsService();
        const { data } = await getProductsOnSale(filters);

        if (data.value) {
          const response = data.value as ProductResponse;
          this.onSaleProducts = response.results || [];
        }
      } catch (error: any) {
        this.error = error.message || "Failed to fetch sale products";
      }
    },

    // Fetch new arrivals
    async fetchNewArrivals(filters: ProductFilter = {}) {
      try {
        const { getNewArrivals } = useProductsService();
        const { data } = await getNewArrivals(filters);

        if (data.value) {
          const response = data.value as ProductResponse;
          this.newArrivals = response.results || [];
        }
      } catch (error: any) {
        this.error = error.message || "Failed to fetch new arrivals";
      }
    },

    // Fetch single product
    async fetchProductById(id: number) {
      this.loading = true;
      this.error = null;

      try {
        const { getProductById } = useProductsService();
        const { data } = await getProductById(id);

        if (data.value) {
          this.currentProduct = data.value as Product;
        }
      } catch (error: any) {
        this.error = error.message || "Failed to fetch product";
      } finally {
        this.loading = false;
      }
    },

    // Search products
    async searchProducts(searchQuery: string, filters: ProductFilter = {}) {
      this.loading = true;
      this.error = null;

      try {
        const { searchProducts } = useProductsService();
        const { data } = await searchProducts(searchQuery, filters);

        if (data.value) {
          const response = data.value as ProductResponse;
          this.products = response.results || [];
          this.pagination.count = response.count || 0;
          this.pagination.next = response.next || null;
          this.pagination.previous = response.previous || null;
          this.pagination.currentPage = filters.page || 1;
        }
      } catch (error: any) {
        this.error = error.message || "Failed to search products";
      } finally {
        this.loading = false;
      }
    },

    // Fetch products by category
    async fetchProductsByCategory(
      categoryId: number,
      filters: ProductFilter = {}
    ) {
      this.loading = true;
      this.error = null;

      try {
        const { getProductsByCategory } = useProductsService();
        const { data } = await getProductsByCategory(categoryId, filters);

        if (data.value) {
          const response = data.value as ProductResponse;
          this.products = response.results || [];
          this.pagination.count = response.count || 0;
          this.pagination.next = response.next || null;
          this.pagination.previous = response.previous || null;
          this.pagination.currentPage = filters.page || 1;
        }
      } catch (error: any) {
        this.error = error.message || "Failed to fetch products by category";
      } finally {
        this.loading = false;
      }
    },

    // Fetch all categories
    async fetchCategories() {
      try {
        const { getCategories } = useProductsService();
        const { data } = await getCategories();

        if (data.value) {
          this.categories = data.value as ProductCategory[];
        }
      } catch (error: any) {
        this.error = error.message || "Failed to fetch categories";
      }
    },

    // Fetch categories with products
    async fetchCategoriesWithProducts() {
      try {
        const { getCategoriesWithProducts } = useProductsService();
        const { data } = await getCategoriesWithProducts();

        if (data.value) {
          this.categoriesWithProducts = data.value as ProductCategory[];
        }
      } catch (error: any) {
        this.error =
          error.message || "Failed to fetch categories with products";
      }
    },

    // Fetch shop statistics
    async fetchShopStats() {
      try {
        const { getShopStats } = useProductsService();
        const { data } = await getShopStats();

        if (data.value) {
          this.shopStats = data.value as ShopStats;
        }
      } catch (error: any) {
        this.error = error.message || "Failed to fetch shop stats";
      }
    },

    // Filter actions
    async filterByPrice(minPrice?: number, maxPrice?: number) {
      const filters: ProductFilter = { ...this.filters, page: 1 };
      if (minPrice !== undefined) filters.min_price = minPrice;
      if (maxPrice !== undefined) filters.max_price = maxPrice;

      await this.fetchProductsWithFilters(filters);
    },

    async filterByStock(
      inStock?: boolean,
      outOfStock?: boolean,
      minStock?: number
    ) {
      const filters: ProductFilter = { ...this.filters, page: 1 };
      if (inStock !== undefined) filters.in_stock = inStock;
      if (outOfStock !== undefined) filters.out_of_stock = outOfStock;
      if (minStock !== undefined) filters.min_stock = minStock;

      await this.fetchProductsWithFilters(filters);
    },

    async filterByPromotion(
      hasPromotion?: boolean,
      promotionId?: number,
      minDiscount?: number
    ) {
      const filters: ProductFilter = { ...this.filters, page: 1 };
      if (hasPromotion !== undefined) filters.has_promotion = hasPromotion;
      if (promotionId !== undefined) filters.promotion_id = promotionId;
      if (minDiscount !== undefined) filters.min_discount = minDiscount;

      await this.fetchProductsWithFilters(filters);
    },

    async filterByCategory(
      categoryId?: number,
      categoryIds?: string,
      excludeCategories?: string
    ) {
      const filters: ProductFilter = { ...this.filters, page: 1 };
      if (categoryId !== undefined) filters.category_id = categoryId;
      if (categoryIds !== undefined) filters.category_ids = categoryIds;
      if (excludeCategories !== undefined)
        filters.exclude_categories = excludeCategories;

      await this.fetchProductsWithFilters(filters);
    },

    async sortProducts(
      sortBy: ProductFilter["sort_by"],
      sortOrder: ProductFilter["sort_order"] = "asc"
    ) {
      const filters: ProductFilter = {
        ...this.filters,
        sort_by: sortBy,
        sort_order: sortOrder,
        page: 1,
      };

      await this.fetchProductsWithFilters(filters);
    },

    // Pagination
    async loadMore() {
      if (this.hasNextPage) {
        const nextPage = this.pagination.currentPage + 1;
        await this.fetchProducts({ ...this.filters, page: nextPage });
      }
    },

    async goToPage(page: number) {
      await this.fetchProducts({ ...this.filters, page });
    },

    // Utility actions
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

    // Initialize shop data
    async initializeShop() {
      await Promise.all([
        this.fetchFeaturedProducts(),
        this.fetchCategoriesWithProducts(),
        this.fetchShopStats(),
        this.fetchNewArrivals({ page_size: 8 }),
        this.fetchOnSaleProducts({ page_size: 8 }),
      ]);
    },
  },

  persist: true,
});
