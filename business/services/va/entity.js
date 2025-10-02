import BaseService from "../base";
class EntityService extends BaseService {
  get entity() {
    return `va/entities`;
  }
  getEntitiesByBot(botId){
    return this.request().get(`va/bots/${botId}/entities`)
  }
}

export default new EntityService();
