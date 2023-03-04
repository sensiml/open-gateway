export const APP_API_URL = 'http://127.0.0.1:5555/' || '/';
export const CLOUD_API_URL = process.env.REACT_APP_CLOUD_API_URL || 'https://sensiml.cloud/'
console.log("process.env.REACT_APP_API_URL", process.env.REACT_APP_API_URL)
export const apiHosts = {
  baseHost: APP_API_URL,
  cloudHost: CLOUD_API_URL,
};
