import { useApi } from "./api";

export interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  sale_price?: number;
  image: string;
  images?: string[];
  category?: {
    id: number;
    name: string;
    slug: string;
  };
  stock: number;
  rating?: number;
  reviews_count?: number;
  slug: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface ProductCategory {
    id: string;
  name: string;
  slug: string;
  description?: string;
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
    return request<ProductResponse>(`/products${query}`);
  };

  const getProductById = (id: number) => {
    return request<Product>(`/products/${id}`);
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
    return request<Product[]>("/products/summary-list");
  };

  const getCategories = () => {
    return request<ProductCategory[]>("/product-categories");
  };

  const getCategoryById = (id: string) => {
    return request<ProductCategory>(`/product-categories/${id}`);
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
