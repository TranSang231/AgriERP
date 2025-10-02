import BaseService from "../base";
import { useUnitTypesStore } from "@/stores/organization/unit-types";

class UnitTypesService extends BaseService {
  get entity() {
    return "unit-types";
  }

  async fetch(force = false) {
    const store = useUnitTypesStore();
    if (force || shouldFetch(store.unitTypes)) {
      store.setUnitTypes({ ...store.unitTypes, fetching: true });
      try {
        const response = await this.gets();
        const unitTypes = createCachedEntry(response);
        store.setUnitTypes(unitTypes);
      } catch (error) {
        store.setUnitTypes({ ...store.unitTypes, fetching: false });
        throw error;
      }
    }
  }
}

export default new UnitTypesService();
