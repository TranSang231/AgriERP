import BaseService from "./base";
import { useOauthStore } from '@/stores/oauth'
import { useEmployeesStore } from '@/stores/business/employee';
import { useOfficesStore } from "@/stores/offices";

class OfficeMembersService extends BaseService {
  get entity() {
    try {
      const store = useOfficesStore()
      return `offices/${store.current_office_id}/employees`;
    } catch (error) {
      return "roles";
    }
    
  }

  async fetch(force=false) {
    const store = useEmployeesStore();
    store.setEmployeesByOffice({
      ...createCachedEntry([], 0)
    });
    if(force || shouldFetch(store.employees_by_office)) {
      store.setEmployeesByOffice({ ...store.employees_by_office, fetching: true });
      try {
        const response = await this.gets();
        const employeesByOffice = createCachedEntry(response);
        store.setEmployeesByOffice(employeesByOffice);
      } catch (error) {
        store.setEmployeesByOffice({ ...store.employees_by_office, fetching: false });
        throw error;
      }
    }  
  }
  
  multipleDelete(ids) {
    return this.request().delete(`/${this.entity}/remove-employees`, { ids });
  }

  addMember(ids) {
    return this.request().put(`/${this.entity}/add-employees`, { ids });
  }

}

export default new OfficeMembersService();