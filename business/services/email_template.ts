// import { useOauthStore } from '@/stores/oauth'
import BaseService from './base';

class EmailTemplateService extends BaseService {
    get entity() {
        try {
            // const store = useOauthStore()
            return `marketing/email-templates`;
        } catch (error) {
            return "roles";
        }
    }
}

export default new EmailTemplateService();