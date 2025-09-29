import { useApi } from "./api";

export interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  sale_price?: number;
  has_promotion?: boolean;
  discount_percentage?: number;
  image?: string;
  images?: Array<{
    id: number;
    image: string;
    alt_text?: string;
  }>;
  categories?: Array<{
    id: number;
    name: {
      origin?: string;
      translations?: any;
    };
    description?: string;
  }>;
  in_stock: number;
  weight?: number;
  length?: number;
  width?: number;
  height?: number;
  tax_rate?: number;
  created_at: string;
  updated_at: string;
}

export interface ProductCategory {
  id: number;
  name: {
    origin?: string;
    translations?: any;
  };
  description?: string;
  active_product_count?: number;
  product_count?: number;
  created_at: string;
  updated_at: string;
}

export interface ProductFilter {
  // Basic filters
  search?: string;
  page?: number;
  page_size?: number;

  // Price filters
  min_price?: number;
  max_price?: number;

  // Stock filters
  in_stock?: boolean;
  out_of_stock?: boolean;
  min_stock?: number;

  // Promotion filters
  has_promotion?: boolean;
  promotion_id?: number;
  min_discount?: number;

  // Category filters
  category_id?: number;
  category_ids?: string;
  category_name?: string;
  exclude_categories?: string;

  // Date filters
  created_after?: string;
  created_before?: string;

  // Physical properties
  min_weight?: number;
  max_weight?: number;

  // Sorting
  sort_by?:
    | "name"
    | "price"
    | "created_at"
    | "updated_at"
    | "in_stock"
    | "weight";
  sort_order?: "asc" | "desc";
}

export interface ShopStats {
  total_categories: number;
  total_products: number;
  products_on_sale: number;
  products_in_stock: number;
  price_range: {
    min: number;
    max: number;
    average: number;
  };
}

export interface ProductResponse {
  count: number;
  next?: string;
  previous?: string;
  results: Product[];
}

export function useProductsService() {
  const { request, publicRequest } = useApi();

  // Public API methods (no authentication required)
  const getProducts = (filters: ProductFilter = {}) => {
    const params = new URLSearchParams();

    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        params.append(key, String(value));
      }
    });

    const query = params.toString() ? `?${params.toString()}` : "";
    return publicRequest<ProductResponse>(`/products${query}`);
  };

  const getProductById = (id: number) => {
    return publicRequest<Product>(`/products/${id}/`);
  };

  const getFeaturedProducts = () => {
    return publicRequest<Product[]>(`/products/featured/`);
  };

  const getProductsOnSale = (filters: ProductFilter = {}) => {
    const params = new URLSearchParams();
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        params.append(key, String(value));
      }
    });
    const query = params.toString() ? `?${params.toString()}` : "";
    return publicRequest<ProductResponse>(`/products/on-sale/${query}`);
  };

  const getNewArrivals = (filters: ProductFilter = {}) => {
    const params = new URLSearchParams();
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        params.append(key, String(value));
      }
    });
    const query = params.toString() ? `?${params.toString()}` : "";
    return publicRequest<ProductResponse>(`/products/new-arrivals/${query}`);
  };

  const getProductsByCategory = (
    categoryId: number,
    filters: ProductFilter = {}
  ) => {
    const params = new URLSearchParams();
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        params.append(key, String(value));
      }
    });
    const query = params.toString() ? `?${params.toString()}` : "";
    return publicRequest<ProductResponse>(
      `/products/by-category/${categoryId}/${query}`
    );
  };

  const searchProducts = (searchQuery: string, filters: ProductFilter = {}) => {
    const params = new URLSearchParams();
    params.append("q", searchQuery);
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        params.append(key, String(value));
      }
    });
    const query = params.toString() ? `?${params.toString()}` : "";
    return publicRequest<ProductResponse>(`/products/search/${query}`);
  };

  const getProductsWithAdvancedFilters = (filters: ProductFilter) => {
    const params = new URLSearchParams();
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        params.append(key, String(value));
      }
    });
    const query = params.toString() ? `?${params.toString()}` : "";
    return publicRequest<ProductResponse>(`/products/filter/${query}`);
  };

  // Category methods
  const getCategories = () => {
    return publicRequest<ProductCategory[]>(`/categories/`);
  };

  const getCategoriesWithProducts = () => {
    return publicRequest<ProductCategory[]>(`/categories/with-products/`);
  };

  const getCategoryById = (id: number) => {
    return publicRequest<ProductCategory>(`/categories/${id}/`);
  };

  // Shop statistics
  const getShopStats = () => {
    return publicRequest<ShopStats>(`/categories/stats/`);
  };

  // Authenticated API methods (for admin/management features)
  const getProductsSummary = () => {
    return request<Product[]>("/products/summary-list/");
  };

  const getTrendingProducts = (filters: ProductFilter = {}) => {
    const params = new URLSearchParams();
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        params.append(key, String(value));
      }
    });
    const query = params.toString() ? `?${params.toString()}` : "";
    return request<ProductResponse>(`/products/trending/${query}`);
  };

  const getLowStockProducts = (threshold = 5, filters: ProductFilter = {}) => {
    const params = new URLSearchParams();
    params.append("threshold", String(threshold));
    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        params.append(key, String(value));
      }
    });
    const query = params.toString() ? `?${params.toString()}` : "";
    return request<ProductResponse>(`/products/low-stock/${query}`);
  };

  return {
    // Public methods
    getProducts,
    getProductById,
    getFeaturedProducts,
    getProductsOnSale,
    getNewArrivals,
    getProductsByCategory,
    searchProducts,
    getProductsWithAdvancedFilters,
    getCategories,
    getCategoriesWithProducts,
    getCategoryById,
    getShopStats,

    // Authenticated methods
    getProductsSummary,
    getTrendingProducts,
    getLowStockProducts,
  };
}
