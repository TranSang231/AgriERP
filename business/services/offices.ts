import BaseService from "./base";

import { useOfficesStore } from '@/stores/offices';

class OfficeService extends BaseService {
  get entity() {
    return "offices";
  }

  async fetch(force=false) {
    const store = useOfficesStore();
    if(force || shouldFetch(store.offices)) {
      store.setOffices({ ...store.offices, fetching: true });
      try {
        const response = await this.gets();
        const offices = createCachedEntry(response);
        store.setOffices(offices);
      } catch (error) {
        store.setOffices({ ...store.offices, fetching: false });
        throw error;
      }
    }
  }
}

export default new OfficeService();
