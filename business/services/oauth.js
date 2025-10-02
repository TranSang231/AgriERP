import BaseService from "./base";
import { useOauthStore } from '@/stores/oauth'
import { shouldFetch, createCachedEntry } from '@/utils/caching';

class OAuthService extends BaseService {
  get entity() {
    return "employees";
  }

  login({ username, password}) {
    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);
    return this.request().post(`${this.entity}/login`, formData);
  }

  logout() {
    const store = useOauthStore();
    const { tokenInfo } = store;
    const { access_token, refresh_token } = tokenInfo;
    const formData = new FormData();
    formData.append("access_token", access_token);
    formData.append("refresh_token", refresh_token);
    return this.request().post(`${this.entity}/logout`, formData);
  }

  userinfo() {
    return this.request().get(`${this.entity}/userinfo`);
  }

  forgotPassword(email) {
    return this.request().post(`${this.entity}/forgot-password`, email);
  }

  getScopes() {
    return this.request().get(`${this.entity}/scopes`);
  }

  async fetchScopes(force=false) {
    const store = useOauthStore();
    if(force || shouldFetch(store.scopes) || shouldFetch(store.default_scopes)) {
      store.setScopes({ ...store.scopes, fetching: true });
      try {
        const response = await this.getScopes();
        const { scopes, default_scopes } = response;
        const scopes_entry = createCachedEntry(scopes);
        const default_scopes_entry = createCachedEntry(default_scopes);
        store.setScopes(scopes_entry);
        store.setDefaultScopes(default_scopes_entry);
      } catch (error) {
        store.setScopes({ ...store.scopes, fetching: false });
        store.setDefaultScopes({ ...store.default_scopes, fetching: false });
        throw error;
      }
    }     
  }


  setPassword(token, password) {
    const formData = new FormData();
    formData.append("token", token);
    formData.append("password", password);
    return this.request().post(`${this.entity}/set-password`, formData);
  }
  

}

export default new OAuthService();