import BaseService from "../base";

class OrderService extends BaseService {
  get entity() {
    return "ecommerce/orders";
  }
}

export default new OrderService();