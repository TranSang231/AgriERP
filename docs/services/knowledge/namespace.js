import BaseService from "../base";
import { shouldFetch, createCachedEntry } from '@/utils/caching';
import { useNamespacesStore } from '@/stores/knowledge/namespaces';

class NamespaceService extends BaseService {
  get entity() {
    return "knowledge/namespaces";
  }

  async fetch(force=false) {
    const store = useNamespacesStore();
    if(force || shouldFetch(store.namespaces)) {
      store.setNamespaces({ ...store.namespaces, fetching: true });
      try {
        const response = await this.gets();
        const namespaces = createCachedEntry(response);
        store.setNamespaces(namespaces);
      } catch (error) {
        store.setNamespaces({ ...store.namespaces, fetching: false });
        throw error;
      }
    }     
  }
}

export default new NamespaceService();