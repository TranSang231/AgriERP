import BaseService from "../base";

class RuleService extends BaseService {
  get entity() {
    return `va/rules`;
  }

  getRulesByBot(botId){
    return this.request().get(`va/bots/${botId}/rules`)
  }
}

export default new RuleService();
