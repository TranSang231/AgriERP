import BaseService from "../base";

class RegexsService extends BaseService {
  get entity() {
    return `va/regexs`;
  }

  getRegexsByBot(botId){
    return this.request().get(`va/bots/${botId}/regexs`)
  }
}

export default new RegexsService();
