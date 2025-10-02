import BaseService from "../base";

class BuildService extends BaseService {
  get entity() {
    return "websites/builds";
  }

  getSiteBuilds(siteID, params=null) {
    const entity = `websites/sites/${siteID}/builds`;
    if (params && Object.keys(params).length > 0) {
      return this.request().get(entity, params);
    }
    return this.request().get(this.entity);
  }
}

export default new BuildService();