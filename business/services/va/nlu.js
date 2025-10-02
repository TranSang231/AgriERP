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
        console.log(host);
        const entry = createCachedEntry(host);
        store.setHost(entry);
      } catch (error) {
        store.setHost({ ...store.host, fetching: false });
        throw error;
      }
    }
  }

  //Todo: Move to backend side
  train(nluHost, data, callbackUrl) {
    const params = {
      save_to_default_model_directory: true,
      force_training: false,
      augmentation:50,
      num_threads:1,
      callback_url: callbackUrl
    }
    const headers = {
      'Content-Type': 'application/x-yaml'
    }
    return this.request().post(`${nluHost}/model/train`, data, params, headers);
  }

  //Todo: Move to backend side
  unloadModel(nluHost) {
    return this.request().delete(`${nluHost}/model`);
  }

  //Todo: Move to backend side
  loadModel(nluHost, payload) {
    return this.request().put(`${nluHost}/model`, payload);
  }

  gets(params = null) {
    if (params && Object.keys(params).length > 0) {
      return this.request().get(`${this.entity}`, params);
    }
    return this.request().get(`${this.entity}`);
  }
}

export default new NLUService();
