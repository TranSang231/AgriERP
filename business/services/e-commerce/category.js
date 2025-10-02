import BaseService from "../base";
import { shouldFetch, createCachedEntry } from '@/utils/caching';
import { useProductCategoriesStore } from '@/stores/e-commerce/categories';

class ProductCategoryService extends BaseService {
  get entity() {
    return "ecommerce/product-categories";
  }

  async fetch(force=false) {
    const store = useProductCategoriesStore();
    if(force || shouldFetch(store.categories)) {
      store.setCategories({ ...store.categories, fetching: true });
      try {
        const response = await this.gets();
        const categories = createCachedEntry(response);
        store.setCategories(categories);
      } catch (error) {
        store.setCategories({ ...store.categories, fetching: false });
        throw error;
      }
    }     
  }
}

export default new ProductCategoryService();