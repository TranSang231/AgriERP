import BaseService from "../base";
import { useActionsStore } from "@/stores/va/actions";
class ActionsService extends BaseService {
  get entity() {
    return "actions";
  }

  async fetchActionsByBots(force = false, botId) {
      const store = useActionsStore();
      if (force || shouldFetch(store.actions)) {
        store.setActions({ ...store.actions, fetching: true });
        try {
          const response = await this.loadActionsAndResponse(botId);
          const actions = createCachedEntry(response.actions);
          store.setActions(actions);
          const responses = createCachedEntry(response.responses);
          store.setResponses(responses);
        } catch (error) {
          throw error;
        }
      }
    }
  loadActionsAndResponse(botId) {
    const data = {
      bot_id: botId,
    };
    return this.request().get(`${this.entity}`, data);
  }
  
  // createResponse (response_id, )
}

export default new ActionsService();
