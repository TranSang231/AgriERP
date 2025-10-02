import Http from './http'
import { shouldFetch, createCachedEntry } from '@/utils/caching';
import { useConstantsStore } from '@/stores/constants';
class ConstantsService {
  entity = "constants";
  constructor() {
    this.entity = "constants"
  }

  request() {
    return new Http();
  }

  get(name: string|String) {
    return this.request().get(`${this.entity}/${name}`);
  }

  gets(params?: any) {
    if (params && Object.keys(params).length > 0) {
      return this.request().get(`${this.entity}`, params);
    }
    return this.request().get(`${this.entity}`);
  }

  async fetchConstant(name: string | String, force=false) {
    const store = useConstantsStore();
    const value = store.getConstant(name);
    if (force || shouldFetch(value)) {
      store.setConstant(name, { ...value, fetching: true });
      this.get(name)
      .then((response: any) => {
        store.setConstant(name, createCachedEntry(response));
      })
      .catch((error: any) => {
        console.error(error);
      });
    }
  }

  async fetchConstants(names: string[]) {
    const store = useConstantsStore();
    let patch = {}
    names.forEach((name) => {
      const value = store.getConstant(name);
      patch = { ...patch, [name]: { ...value, fetching: true }}
    });
    store.patch(patch);

    this.gets({names})
    .then((response: any) => {
      const entries = Object.entries(response);
      patch = {}
      for (const [key, value] of entries) {
        patch = { ...patch, [key]: createCachedEntry(value)}
      }
      store.patch(patch);
    })
    .catch((e) => {
      console.error(e);
    });
  }

  async fetch(names?: any, force=false) {
    if (typeof names === 'string' || names instanceof String) {
      this.fetchConstant(names)
    } else {
      const store = useConstantsStore();
      const entries = Object.entries(store.$state);
      let update_keys = []
      if (names && names.length > 0) {
        names.forEach((name: string|String) => {
          if (force || shouldFetch(store.getConstant(name))) {
            update_keys.push(name);
          }
        })
      }
      if (!names) {
        for (const [key, value] of entries) {
          if (force || shouldFetch(value)) {
            update_keys.push(key);
          }
        }
      }
      if (update_keys.length > 0) {
        this.fetchConstants(update_keys);
      }
    } 
  }
}

export default new ConstantsService();
