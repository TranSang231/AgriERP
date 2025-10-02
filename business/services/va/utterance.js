import BaseService from "../base";

class UtterancetService extends BaseService {
  get entity() {
    return `va/utterances`;
  }
  getIntentsByBot(botId){
    return this.request().get(`va/bots/${botId}/utterances`)
  }
}

export default new UtterancetService();
