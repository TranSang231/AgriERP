import BaseService from "../base";
import { shouldFetch, createCachedEntry } from '@/utils/caching';
import { useArticleCategoriesStore } from '@/stores/websites/categories';

class CategoryService extends BaseService {
  get entity() {
    return "websites/categories";
  }

  async fetch(force=false) {
    const store = useArticleCategoriesStore();
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

export default new CategoryService();