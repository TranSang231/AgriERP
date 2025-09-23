import BaseService from "../base";

class GoodsReceiptService extends BaseService {
  get entity() {
    return "ecommerce/goods-receipts";
  }

  apply(id) {
    return this.request().post(`${this.entity}/${id}/apply`);
  }
}

export default new GoodsReceiptService();


