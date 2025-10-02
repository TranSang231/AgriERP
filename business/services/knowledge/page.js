import BaseService from "../base";

class PageService extends BaseService {
  get entity() {
    return "knowledge/pages";
  }

  async getNamespacePages(namespaceId, params = {}) {
    try {
      const queryParams = {
        namespace_id: namespaceId,
        ...params
      };
      
      const response = await this.gets(queryParams);
      return response;
    } catch (error) {
      console.error('Error fetching namespace pages:', error);
      throw error;
    }
  }
}
export default new PageService();