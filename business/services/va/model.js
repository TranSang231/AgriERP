import BaseService from "../base";
class ModelService extends BaseService {
  get entity() {
    return `va/models`;
  }

  getModelsByBotId(botId){
    return this.request().get(`${this.entity}/${botId}`)
  }
  loadRasaModel(serverModel){
    return this.request().put(`/rasa/model`, { "model_file": serverModel })
  }
}

export default new ModelService();
