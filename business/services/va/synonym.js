import BaseService from "../base";

class SynonymService extends BaseService {
  get entity() {
    return `va/synonyms`;
  }
  getIntentsByBot(botId){
    return this.request().get(`va/bots/${botId}/synonyms`)
  }
}

export default new SynonymService();
