import BaseService from "../base";
import { useEmployeesStore } from '@/stores/business/employee';

class EmployeeService extends BaseService {
  get entity() {
    return "employees";
  }

  async fetch(force=false) {
    const store = useEmployeesStore();
    if(force || shouldFetch(store.employees)) {
      store.setEmployees({ ...store.employees, fetching: true });
      try {
        const response = await this.gets();
        const employees = createCachedEntry(response);
        store.setEmployees(employees);
      } catch (error) {
        store.setEmployees({ ...store.employees, fetching: false });
        throw error;
      }
    }  
  }
  
  sendInvitation(id){
    return this.request().post(`${this.entity}/${id}/invite`);
  }

  verify(data){
    return this.request().post(`${this.entity}/verify`, data);
  }
}

export default new EmployeeService();