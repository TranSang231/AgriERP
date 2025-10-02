import BaseService from "../base";

class StatisticService extends BaseService {
  get entity() {
    return "knowledge/statistics";
  }

  /**
   * Get general statistics (total users, namespaces, pages)
   */
  getGeneralStatistics() {
    return this.request().get(`${this.entity}/general`);
  }

  /**
   * Get pages created count, grouped by date
   * @param {Object} params - Query parameters
   * @param {string} params.start_date - Start date (YYYY-MM-DD)
   * @param {string} params.end_date - End date (YYYY-MM-DD)
   */
  getPagesCreatedByDate(params = {}) {
    return this.request().get(`${this.entity}/pages-created-by-date`, params);
  }
}

export default new StatisticService();