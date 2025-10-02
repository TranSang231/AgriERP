import BaseService from '../base';

class EcommerceStatisticService extends BaseService {
  get entity() {
    return `ecommerce/statistics`;
  }

  getGeneralStats() {
    return this.request().get(`${this.entity}/general`);
  }

  getSalesData(period = '30d') {
    return this.request().get(`${this.entity}/sales`, { period });
  }

  getOrderStatusData() {
    return this.request().get(`${this.entity}/order-status`);
  }

  getRecentOrders() {
    return this.request().get(`${this.entity}/recent-orders`);
  }

  getTopProducts() {
    return this.request().get(`${this.entity}/top-products`);
  }

  getInventoryAlerts() {
    return this.request().get(`${this.entity}/inventory-alerts`);
  }
}

export default new EcommerceStatisticService();
