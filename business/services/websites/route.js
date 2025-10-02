import BaseService from "../base";

class RouteService extends BaseService {
  get entity() {
    return "websites/routes";
  }

  getSiteRoutes(siteID, params=null) {
    const entity = `websites/sites/${siteID}/routes`;
    if (params && Object.keys(params).length > 0) {
      return this.request().get(entity, params);
    }
    return this.request().get(entity);
  }
}

export default new RouteService();