import { useApi } from "./api";

export interface Inventory {
  id: string;
  current_quantity: number;
  min_quantity: number;
  max_quantity?: number;
  reserved_quantity: number;
  available_quantity: number;
  is_low_stock: boolean;
  is_out_of_stock: boolean;
  updated_at: string;
}

export interface Product {
  id: number;
  name: {
    origin: string;
    translates?: Array<{
      language: string;
      value: string;
    }>;
  };
  description: {
    origin: string;
    translates?: Array<{
      language: string;
      value: string;
    }>;
  };
  price: number;
  sale_price?: number;
  image: string;
  images?: string[];
  category?: {
    id: number;
    name: {
      origin: string;
      translates?: Array<{
        language: string;
        value: string;
      }>;
    };
    slug: string;
  };
  in_stock: number;
  inventory?: Inventory;
  rating?: number;
  reviews_count?: number;
  slug: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface ProductCategory {
  id: string;
  name: {
    origin: string;
    translates?: Array<{
      language: string;
      value: string;
    }>;
  };
  slug: string;
  description?: {
    origin: string;
    translates?: Array<{
      language: string;
      value: string;
    }>;
  };
  image?: string;
  parent?: number;
  is_active: boolean;
}

export interface ProductFilter {
  category?: string;
  search?: string;
  min_price?: number;
  max_price?: number;
  ordering?: string;
  page?: number;
  page_size?: number;
}

export interface ProductResponse {
  count: number;
  next?: string;
  previous?: string;
  results: Product[];
}

export function useProductsService() {
  const { request } = useApi();

  const getProducts = (filters: ProductFilter = {}) => {
    const params = new URLSearchParams();

    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        params.append(key, String(value));
      }
    });

    const query = params.toString() ? `?${params.toString()}` : "";
    // Request the summary-list endpoint exposed under /api/v1/ecommerce/products
    return request<ProductResponse>(`/ecommerce/products/summary-list${query}`);
  };

  const getProductById = (id: number) => {
    // Product detail from ecommerce ProductViewSet
    return request<Product>(`/ecommerce/products/${id}`);
  };

  const getProductsByCategory = (
    categoryId: string,
    filters: Omit<ProductFilter, "category"> = {}
  ) => {
    return getProducts({ ...filters, category: categoryId });
  };

  const searchProducts = (
    search: string,
    filters: Omit<ProductFilter, "search"> = {}
  ) => {
    return getProducts({ ...filters, search });
  };

  const getProductsSummary = () => {
    return request<Product[]>("/ecommerce/products/summary-list");
  };

  const getCategories = () => {
    return request<ProductCategory[]>("/ecommerce/product-categories");
  };

  const getCategoryById = (id: string) => {
    return request<ProductCategory>(`/ecommerce/product-categories/${id}`);
  };

  return {
    getProducts,
    getProductById,
    getProductsByCategory,
    searchProducts,
    getProductsSummary,
    getCategories,
    getCategoryById,
  };
}
