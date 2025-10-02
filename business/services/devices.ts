import BaseService from "./base";
import { useOauthStore } from "@/stores/oauth";

class DeviceService extends BaseService {
  get entity() {
    return "devices";
  }

  verify(formData: any) {
    return this.request().post(`${this.entity}/verify`, formData);
  }

  invite(formData: any) {
    return this.request().post(`${this.entity}/invite`, formData);
  }
}

export default new DeviceService();
