import BaseService from '../base';
import { useNluStore } from '@/stores/va/nlu';
import { shouldFetch, createCachedEntry } from '@/utils/caching';

class NLUService extends BaseService {
  get entity() {
    return `va/nlu`;
  }

  getVersion(){
    return this.request().get(`${this.entity}/version`)
  }

  getStatus(){
    return this.request().get(`${this.entity}/status`)
  }

  getHost(){
    return this.request().get(`${this.entity}/nlu-host`)
  }

  async fetchHost(force = false) {
    const store = useNluStore();
    if (force || shouldFetch(store.host)) {
      store.setHost({ ...store.host, fetching: true });
      try {
        const { host } = await this.getHost();
        const entry = createCachedEntry(host);
        store.setHost(entry);
      } catch (error) {
        store.setHost({ ...store.host, fetching: false });
        throw error;
      }
    }
  }
}

export default new NLUService();
