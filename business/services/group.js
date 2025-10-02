import BaseService from "./base";
import { useGroupsStore } from "@/stores/groups";
import { useOauthStore } from '@/stores/oauth'
class GroupService extends BaseService {
  get entity() {
    return "groups"
  }

  async fetch(force = false) {
    const store = useGroupsStore();
    const oauthStore = useOauthStore();
    if (force || shouldFetch(store.groups)) {
      store.setGroups({ ...store.groups, fetching: true });
      try {
        const response = await this.tree({ business_id: oauthStore.businessId });
        const groups = createCachedEntry(response);
        store.setGroups(groups);
      } catch (error) {
        store.setGroups({ ...store.groups, fetching: false });
        throw error;
      }
    }
  }
}

export default new GroupService();
