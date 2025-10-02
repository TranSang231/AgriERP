import BaseService from "../base";

class SectionService extends BaseService {
  get entity() {
    return "websites/sections";
  }

  getSiteSections(siteID, params=null) {
    const entity = `websites/sites/${siteID}/sections`;
    if (params && Object.keys(params).length > 0) {
      return this.request().get(entity, params);
    }
    return this.request().get(entity);
  }
}

export default new SectionService();