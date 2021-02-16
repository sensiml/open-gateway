import axios from "axios";


const ApiService = {
  // Stores the 401 interceptor position so that it can be later ejected when needed
  interceptor_401: null,
  refreshUrl: '/auth/refresh',

  init(baseURL) {
    axios.defaults.baseURL = baseURL;
  },

  mount401Interceptor() {
    this.interceptor_401 = axios.interceptors.response.use((response) => response,
      async (error) => {
        if (error.request.status === 401) {
          if (error.config.url.includes('auth')) {
            // Refresh token has failed or auth endpoint return 401 => Logout the user
            throw error;
          } else {
            // refresh token
          }
        }
        // If error was not 401 just reject as is
        throw error;
      });
  },
  

  unmount401Interceptor() {
    // Eject the interceptor
    axios.interceptors.response.eject(this.interceptor_401);
  },
  
  setCustomAuthHeader(key) {
    axios.defaults.headers.common.Authorization = key;
  },

  setContentType(type) {
    axios.defaults.headers.contentType = type;
  },

  removeHeader() {
    axios.defaults.headers.common = {};
  },

  get(resource) {
    return axios.get(resource);
  },

  post(resource, data) {
    return axios.post(resource, data);
  },

  put(resource, data) {
    return axios.put(resource, data);
  },

  delete(resource) {
    return axios.delete(resource);
  },

  customRequest(data) {
    return axios(data);
  },

  customJsonRequest(data) {
    this.setAuthHeader();
    this.setContentType('application/json');
    return axios(data);
  },

};

export default ApiService;
