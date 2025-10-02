import BaseService from "../base";
class ParamsService extends BaseService {
  get entity() {
    return `va/parameters`;
  }

  getParamsByIntentId(intentId) {
    return this.request().get(`va/intents/${intentId}/parameters`);
  }

  getParamsByExpressionId(expressionId) {
    return this.request().get(`va/expressions/${expressionId}/parameters`);
  }

  updateParameterEntity(parameter_id, entity_id) {
    const data = {
      parameter_id: parameter_id,
      entity_id: entity_id,
    };
    
    return this.request().put(`va/parameters/${parameter_id}`, data);
  }
}

export default new ParamsService();
