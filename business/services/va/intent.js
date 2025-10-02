import BaseService from "../base";

class IntentService extends BaseService {
  get entity() {
    return `va/intents`;
  }
  getIntentsByBot(botId){
    return this.request().get(`va/bots/${botId}/intents`)
  }
}

export default new IntentService();
