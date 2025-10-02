import Http from './http';

export default class BaseService {
  constructor() {
    if (!this.entity) {
      throw new Error("Child service class not provide entity");
    }
  }

  request() {
    return new Http();
  }

  get(id) {
    return this.request().get(`${this.entity}/${id}`);
  }

  create(obj) {
    return this.request().post(`${this.entity}`, obj);
  }

  delete(id) {
    return this.request().delete(`${this.entity}/${id}`);
  }

  multipleDelete(ids) {
    return this.request().delete(`${this.entity}`, { ids });
  }

  update(obj) {
    const id = (obj instanceof FormData) ? obj.get("id") : obj.id;
    return this.request().put(`${this.entity}/${id}`, obj);
  }

  sync(array) {
    return this.request().put(`${this.entity}`, array);
  }

  gets(params = null) {
    if (params && Object.keys(params).length > 0) {
      return this.request().get(`${this.entity}`, params);
    }
    return this.request().get(`${this.entity}`);
  }

  tree(params) {
    if (params) {
      return this.request().get(`${this.entity}/tree`,
        params,
      );
    }
    return this.request().get(`${this.entity}/tree`);
  }

  summary_list(params) {
    if (params) {
      return this.request().get(`${this.entity}/summary-list`,
        params,
      );
    }
    return this.request().get(`${this.entity}/summary-list`);
  }

  import(data) {
    return this.request().post(`${this.entity}/import`, data);
  }
}
