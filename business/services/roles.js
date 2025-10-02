import BaseService from "./base";
import { shouldFetch, createCachedEntry } from '@/utils/caching';
import { useOauthStore } from '@/stores/oauth';
import { useRolesStore } from '@/stores/oauth/roles';

class RoleService extends BaseService {
  get entity() {
    return "roles";
  }
  async fetch(force=false) {
    const store = useRolesStore();
    if(force || shouldFetch(store.roles)) {
      store.setRoles({ ...store.roles, fetching: true });
      try {
        const response = await this.gets();
        const roles = createCachedEntry(response);
        store.setRoles(roles);
      } catch (error) {
        store.setRoles({ ...store.scopes, fetching: false });
        throw error;
      }
    }     
  }
}

export default new RoleService();