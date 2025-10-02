import BaseService from "../base";
import { useProductsStore } from '@/stores/e-commerce/products';

class ProductService extends BaseService {
  get entity() {
    return "ecommerce/products";
  }

  async fetch(force=false) {
    const store = useProductsStore();
    if(force || shouldFetch(store.products)) {
      store.setProducts({ ...store.products, fetching: true });
      try {
        const response = await this.summary_list();
        const products = createCachedEntry(response);
        store.setProducts(products);
      } catch (error) {
        store.setProducts({ ...store.products, fetching: false });
        throw error;
      }
    }     
    }
}

export default new ProductService();