import BaseService from "../base";
import { useCustomersStore } from '@/stores/e-commerce/customers';
import { shouldFetch, createCachedEntry } from '@/utils/caching';

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

  async createCustomer(customerData) {
    try {
      const response = await this.create(customerData);
      // Refresh the store after creating
      await this.fetch(true);
      return response;
    } catch (error) {
      throw error;
    }
  }

  async updateCustomer(customerData) {
    try {
      const response = await this.update(customerData);
      // Refresh the store after updating
      await this.fetch(true);
      return response;
    } catch (error) {
      throw error;
    }
  }

  async deleteCustomer(customerId) {
    try {
      const response = await this.delete(customerId);
      // Refresh the store after deleting
      await this.fetch(true);
      return response;
    } catch (error) {
      throw error;
    }
  }

  async getCustomer(customerId) {
    try {
      return await this.get(customerId);
    } catch (error) {
      throw error;
    }
  }

  async searchCustomers(searchParams) {
    try {
      return await this.gets(searchParams);
    } catch (error) {
      throw error;
    }
  }
}

export default new CustomerService();