import BaseService from "../base";

class PromotionService extends BaseService {
  get entity() {
    return "ecommerce/promotions";
  }
}

export default new PromotionService();