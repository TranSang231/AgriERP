export default class Http {
  constructor() {
    const { $api } = useNuxtApp();
    this.api = $api;
  }

  get(path, params=null) {
    if (!params)
      return this.api(path);
    const query = Object.entries(params).reduce((c,o) => {
      const [key, val] = o;
      let conjunction = c.length > 0 ? "&" : "";
      if (Array.isArray(val)) {
        const param = val.map((v) => `${key}[]=${v}`).join('&');
        return c + conjunction + param;
      } else {
        return c + conjunction + `${key}=${val}`;
      }
    }, '');
    const url = `${path}?${query}`;
    return this.api(url);
  }

  post(path, data=null) {
    return this.api(path, {
      method: "POST",
      body: data
    });
  }

  put(path, data) {
    return this.api(path, {
      method: "PUT",
      body: data
    });
  }

  delete(path, data=null) {
    return this.api(path, {
      method: "DELETE",
      body: data
    });
  }
}
