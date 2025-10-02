import BaseService from "../base";

class StoryService extends BaseService {
  get entity() {
    return `va/stories`;
  }

  getStoriesByBot(botId){
    return this.request().get(`va/bots/${botId}/stories`)
  }
}

export default new StoryService();
