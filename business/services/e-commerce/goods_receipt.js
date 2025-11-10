import BaseService from "../base";

class GoodsReceiptService extends BaseService {
  get entity() {
    return "ecommerce/goods-receipts";
  }

  apply(id) {
    return this.request().post(`${this.entity}/${id}/apply`);
  }

  unapply(id) {
    return this.request().post(`${this.entity}/${id}/unapply`);
  }
}

export default new GoodsReceiptService();


