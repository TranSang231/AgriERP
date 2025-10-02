import BaseService from "../base";
import { useBotsStore } from "@/stores/va/bots";
class BotService extends BaseService {
  get entity() {
    return "va/bots";
  }

  async fetch(force = false) {
    const store = useBotsStore();
    if (force || shouldFetch(store.bots)) {
      store.setBots({ ...store.bots, fetching: true });
      try {
        const response = await this.gets();
        const bots = createCachedEntry(response);
        store.setBots(bots);
      } catch (error) {
        throw error;
      }
    }
  }

  getTrainingData(id) {
    return this.request().get(`${this.entity}/${id}/training-data`);
  }
}

export default new BotService();
