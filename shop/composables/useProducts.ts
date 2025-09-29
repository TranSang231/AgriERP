import { computed } from "vue";
import { useProductsStore } from "~/stores/products";
import type { ProductFilter } from "~/services/products";

export const useProducts = () => {
  const store = useProductsStore();

  // Reactive state
  const products = computed(() => store.products);
  const featuredProducts = computed(() => store.featuredProducts);
  const onSaleProducts = computed(() => store.onSaleProducts);
  const newArrivals = computed(() => store.newArrivals);
  const categories = computed(() => store.categories);
  const categoriesWithProducts = computed(() => store.categoriesWithProducts);
  const currentProduct = computed(() => store.currentProduct);
  const shopStats = computed(() => store.shopStats);
  const loading = computed(() => store.loading);
  const error = computed(() => store.error);
  const pagination = computed(() => store.pagination);
  const filters = computed(() => store.filters);

  // Getters
  const totalPages = computed(() => store.totalPages);
  const hasNextPage = computed(() => store.hasNextPage);
  const hasPreviousPage = computed(() => store.hasPreviousPage);
  const activeCategories = computed(() => store.activeCategories);
  const priceRange = computed(() => store.priceRange);

  // Actions
  const fetchProducts = (filters?: ProductFilter) =>
    store.fetchProducts(filters);
  const fetchProductsWithFilters = (filters: ProductFilter) =>
    store.fetchProductsWithFilters(filters);
  const fetchFeaturedProducts = () => store.fetchFeaturedProducts();
  const fetchOnSaleProducts = (filters?: ProductFilter) =>
    store.fetchOnSaleProducts(filters);
  const fetchNewArrivals = (filters?: ProductFilter) =>
    store.fetchNewArrivals(filters);
  const fetchProductById = (id: number) => store.fetchProductById(id);
  const searchProducts = (query: string, filters?: ProductFilter) =>
    store.searchProducts(query, filters);
  const fetchProductsByCategory = (
    categoryId: number,
    filters?: ProductFilter
  ) => store.fetchProductsByCategory(categoryId, filters);
  const fetchCategories = () => store.fetchCategories();
  const fetchCategoriesWithProducts = () => store.fetchCategoriesWithProducts();
  const fetchShopStats = () => store.fetchShopStats();

  // Filter actions
  const filterByPrice = (minPrice?: number, maxPrice?: number) =>
    store.filterByPrice(minPrice, maxPrice);
  const filterByStock = (
    inStock?: boolean,
    outOfStock?: boolean,
    minStock?: number
  ) => store.filterByStock(inStock, outOfStock, minStock);
  const filterByPromotion = (
    hasPromotion?: boolean,
    promotionId?: number,
    minDiscount?: number
  ) => store.filterByPromotion(hasPromotion, promotionId, minDiscount);
  const filterByCategory = (
    categoryId?: number,
    categoryIds?: string,
    excludeCategories?: string
  ) => store.filterByCategory(categoryId, categoryIds, excludeCategories);
  const sortProducts = (
    sortBy: ProductFilter["sort_by"],
    sortOrder?: ProductFilter["sort_order"]
  ) => store.sortProducts(sortBy, sortOrder);

  // Pagination
  const loadMore = () => store.loadMore();
  const goToPage = (page: number) => store.goToPage(page);

  // Utility
  const setFilters = (filters: ProductFilter) => store.setFilters(filters);
  const clearFilters = () => store.clearFilters();
  const clearCurrentProduct = () => store.clearCurrentProduct();
  const initializeShop = () => store.initializeShop();

  return {
    // State
    products,
    featuredProducts,
    onSaleProducts,
    newArrivals,
    categories,
    categoriesWithProducts,
    currentProduct,
    shopStats,
    loading,
    error,
    pagination,
    filters,

    // Getters
    totalPages,
    hasNextPage,
    hasPreviousPage,
    activeCategories,
    priceRange,

    // Actions
    fetchProducts,
    fetchProductsWithFilters,
    fetchFeaturedProducts,
    fetchOnSaleProducts,
    fetchNewArrivals,
    fetchProductById,
    searchProducts,
    fetchProductsByCategory,
    fetchCategories,
    fetchCategoriesWithProducts,
    fetchShopStats,

    // Filters
    filterByPrice,
    filterByStock,
    filterByPromotion,
    filterByCategory,
    sortProducts,

    // Pagination
    loadMore,
    goToPage,

    // Utility
    setFilters,
    clearFilters,
    clearCurrentProduct,
    initializeShop,
  };
};
