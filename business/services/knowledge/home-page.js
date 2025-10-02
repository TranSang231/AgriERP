import BaseService from "../base";

class HomePageService extends BaseService {
  get entity() {
    return "knowledge/home-pages";
  }

  // Get homepage by namespace
  getByNamespace(namespaceId) {
    return this.request().get(`${this.entity}/namespaces/${namespaceId}`);
  }
}

export default new HomePageService();