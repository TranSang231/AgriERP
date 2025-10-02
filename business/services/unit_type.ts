import BaseService from "./base";
import { useOauthStore } from "@/stores/oauth";

class UnitTypeService extends BaseService {
  get entity() {
      return `unit-types`;
  }
}

export default new UnitTypeService();