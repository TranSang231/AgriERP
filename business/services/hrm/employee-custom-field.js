import BaseService from "../base";
import { useCustomFieldsStore } from '@/stores/business/custom-fields';

class EmployeeCustomFieldService extends BaseService {
  get entity() {
    return "employee-custom-fields";
  }
  
  async fetch(force=false) {
    const store = useCustomFieldsStore();
    if(force || shouldFetch(store.custom_fields)) {
      store.setCustomFields({ ...store.custom_fields, fetching: true });
      try {
        const response = await this.gets();
        const customFields = createCachedEntry(response);
        store.setCustomFields(customFields);
      } catch (error) {
        store.setCustomFields({ ...store.custom_fields, fetching: false });
        throw error;
      }
    }     
  }
}

export default new EmployeeCustomFieldService();