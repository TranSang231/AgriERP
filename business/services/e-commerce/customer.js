import BaseService from "../base";
import { useCustomersStore } from '@/stores/e-commerce/customers';

class CustomerService extends BaseService {
  get entity() {
    return "ecommerce/customers";
  }

  async fetch(force=false) {
    const store = useCustomersStore();
    if(force || shouldFetch(store.customers)) {
      store.setCustomers({ ...store.customers, fetching: true });
      try {
        const response = await this.gets();
        const customers = createCachedEntry(response);
        store.setCustomers(customers);
      } catch (error) {
        store.setCustomers({ ...store.customers, fetching: false });
        throw error;
      }
    }     
    }
}

export default new CustomerService();