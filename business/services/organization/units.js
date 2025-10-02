import BaseService from "../base";
import { useUnitsStore } from "@/stores/organization/units";

class UnitService extends BaseService {
  get entity() {
    return `units`;
  }

  async fetch(force = false) {
    const store = useUnitsStore();
    if (force || shouldFetch(store.units)) {
      store.setUnits({ ...store.units, fetching: true });
      try {
        const response = await this.tree();
        const units = createCachedEntry(response);
        store.setUnits(units);
      } catch (error) {
        store.setUnits({ ...store.units, fetching: false });
        throw error;
      }
    }
  }


  addMember(data) {
    return this.request().put(
      `${this.entity}/${data.unit_id}/add-member`,
      data
    );
  }

  removeMember(data) {
    return this.request().delete(
      `${this.entity}/${data.unit_id}/remove-member`,
      data
    );
  }
}

export default new UnitService();
