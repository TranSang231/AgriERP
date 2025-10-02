import BaseService from "../base";

class MenuService extends BaseService {
  get entity() {
    return "websites/menus";
  }

  getSiteMenus(siteID, params=null) {
    const entity = `websites/sites/${siteID}/menus`;
    if (params && Object.keys(params).length > 0) {
      return this.request().get(entity, params);
    }
    return this.request().get(entity);
  }
}

export default new MenuService();