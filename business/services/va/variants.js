import BaseService from "../base";

class VariantsService extends BaseService {
  get entity() {
    return `va/variants`;
  }

  getVariantsBySynonym(synonymId){
    return this.request().get(`va/synonyms/${synonymId}/variants`)
  }
}

export default new VariantsService();
