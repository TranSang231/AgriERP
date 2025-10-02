import BaseService from "../base";

class ArticleService extends BaseService {
  get entity() {
    return "websites/articles";
  }

  getSiteArticles(siteID, params=null) {
    const entity = `websites/sites/${siteID}/articles`;
    if (params && Object.keys(params).length > 0) {
      return this.request().get(entity, params);
    }
    return this.request().get(entity);
  }
}

export default new ArticleService();