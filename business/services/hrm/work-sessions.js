import BaseService from "../base";
import { useOfficesStore } from '@/stores/offices';
import { useWorkSessionsStore } from '@/stores/work-session';
class WorkSessionService extends BaseService {
  get entity() {
    try {
      const store = useOfficesStore()
      return `offices/${store.currentOfficeId}/work-sessions`;
    } catch (error) {
      return "offices/work-sessions";
    }
  }

  async fetch(force=false) {
    const store = useWorkSessionsStore();
    if(force || shouldFetch(store.work_sessions)) {
      store.setWorkSessions({ ...store.work_sessions, fetching: true });
      try {
        const response = await this.gets();
        const work_sessions = createCachedEntry(response);
        store.setWorkSessions(work_sessions);
      } catch (error) {
        store.setWorkSessions({ ...store.work_sessions, fetching: false });
        throw error;
      }
    }  
  }
}

export default new WorkSessionService();