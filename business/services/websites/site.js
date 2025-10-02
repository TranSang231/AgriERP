import BaseService from "../base";
import { shouldFetch, createCachedEntry } from '@/utils/caching';
import { useSitesStore } from '@/stores/websites/sites';

class SiteService extends BaseService {
  get entity() {
    return "websites/sites";
  }

  async fetch(force=false) {
    const store = useSitesStore();
    if(force || shouldFetch(store.sites)) {
      store.setSites({ ...store.sites, fetching: true });
      try {
        const response = await this.gets();
        const sites = createCachedEntry(response);
        store.setSites(sites);
      } catch (error) {
        store.setSites({ ...store.sites, fetching: false });
        throw error;
      }
    }     
  }
}

export default new SiteService();