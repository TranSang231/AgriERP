import BaseService from "../base";
class ResponseService extends BaseService {
  get entity() {
    return "va/responses";
  }

  getResponsesByBot(botId){
    return this.request().get(`va/bots/${botId}/responses`)
  }
}

export default new ResponseService();
