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

  post(path, data=null, params=null, headers=null) {
    const query = params
      ? '?' + Object.entries(params).reduce((c,o) => {
          const [key, val] = o;
          let conjunction = c.length > 0 ? "&" : "";
          if (Array.isArray(val)) {
            const param = val.map((v) => `${key}[]=${v}`).join('&');
            return c + conjunction + param;
          } else {
            return c + conjunction + `${key}=${val}`;
          }
        }, '')
      : '';
    const url = `${path}${query}`;
    let options = {
      method: "POST",
      body: data
    }
    if (headers) {
      options = { ...options, headers }
      //Todo: use this.api instead
      return fetch(url, options);
    }
    if (headers) {
      return this.api(url, options, {headers});
    }
    
    return this.api(url, options);
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
