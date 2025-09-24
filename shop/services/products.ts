import { useApi } from "./api";
import { useRuntimeConfig } from 'nuxt/app'

export interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  sale_price?: number;
  image: string;
  images?: string[];
  category: {
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
  parent?: string;
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
  const config = useRuntimeConfig()

  const toAbsolute = (path?: string) => {
    if (!path) return "";
    if (path.startsWith("http://") || path.startsWith("https://")) return path;
    return `${config.public.defaultHost}${path.startsWith('/') ? '' : '/'}${path}`;
  };

  // Backend types
  type BEShort = { origin?: string } | string | null | undefined

  const getShort = (s: BEShort): string => {
    if (!s) return "";
    if (typeof s === 'string') return s;
    return s.origin || "";
  };

  function mapBEProduct(p: any): Product {
    const firstCategory = Array.isArray(p.categories) && p.categories.length > 0 ? p.categories[0] : null;
    const categoryName = firstCategory ? getShort(firstCategory.name) : "";
    const slugify = (txt: string) => txt.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');

    return {
      id: p.id,
      name: getShort(p.name),
      description: getShort(p.description),
      price: p.price ?? 0,
      sale_price: undefined,
      image: toAbsolute(p.thumbnail),
      images: (p.images || []).map((img: any) => toAbsolute(img.image)),
      category: firstCategory ? {
        id: firstCategory.id,
        name: categoryName,
        slug: slugify(categoryName),
      } : { id: 0, name: "", slug: "" },
      stock: p.in_stock ?? 0,
      rating: undefined,
      reviews_count: undefined,
      slug: slugify(getShort(p.name)),
      is_active: true,
      created_at: p.created_at,
      updated_at: p.updated_at,
    };
  }

  function mapBECategory(c: any): ProductCategory {
    const name = getShort(c.name);
    const slugify = (txt: string) => txt.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
    return {
      id: c.id,
      name,
      slug: slugify(name),
      description: c.description || undefined,
      image: undefined,
      parent: undefined,
      is_active: true,
    }
  }

  const getProducts = (filters: ProductFilter = {}) => {
    const params = new URLSearchParams();

    Object.entries(filters).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        const str = String(value)
        if (str !== "") params.append(key, str);
      }
    });

    const query = params.toString() ? `?${params.toString()}` : "";
    return request<ProductResponse>(`/products${query}`).then((res: any) => {
      if (res.data?.value) {
        const be = res.data.value as any
        be.results = (be.results || []).map(mapBEProduct)
      }
      return res
    });
  };

  const getProductById = (id: number) => {
    return request<Product>(`/products/${id}`).then((res: any) => {
      if (res.data?.value) res.data.value = mapBEProduct(res.data.value)
      return res
    });
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
    return request<Product[]>("/products/summary-list").then((res: any) => {
      if (res.data?.value) res.data.value = (res.data.value as any[]).map(mapBEProduct)
      return res
    });
  };

  const getCategories = () => {
    return request<ProductCategory[]>("/product-categories").then((res: any) => {
      if (res.data?.value) res.data.value = (res.data.value as any[]).map(mapBECategory)
      return res
    });
  };

  const getCategoryById = (id: string) => {
    return request<ProductCategory>(`/product-categories/${id}`).then((res: any) => {
      if (res.data?.value) res.data.value = mapBECategory(res.data.value)
      return res
    });
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
