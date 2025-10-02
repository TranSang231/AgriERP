import BaseService from "../base";
class ExpressionsService extends BaseService {
  get entity() {
    return `va/expressions`;
  }

  getExpressionsByIntent(intentId){
    return this.request().get(`/intents/${intentId}/expressions`)
  }

  getExpressionsByIntents(intentIds){
    return this.gets({intentIds})
  }
}

export default new ExpressionsService();
