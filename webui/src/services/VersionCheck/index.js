import axios from "axios";
import { BaseStreamHttpError } from "../StreamReader";
import store from "../../redux/store";
import { UPDATE_AVAILABLE, UPDATE_CLOUD_VERSION, UPDATE_LOCAL_VERSION } from "../../redux/actions/actionTypes";

export class VersionCheck {
  constructor(baseURL, cloudURL) {
    this.baseurl = baseURL;
    this.cloudurl = cloudURL;
    this.localVersion = "";
    this.cloudVersion = "";
    this.updateAvailable = false;
  }

  async checkUpdate() {
    let localResponse;
    let response;
    try {
      localResponse = await axios.get(`${this.baseurl}version`);
    } catch (error) {
      console.log(error);
      throw new BaseStreamHttpError(404, {
        detail: "Failed to fetch API service",
      });
    }
    if (localResponse.statusText !== "OK") {
      throw new BaseStreamHttpError(response.status, {
        detail: localResponse.statusText,
      });
    }
    this.localVersion = localResponse.data
    store.dispatch({ type: UPDATE_LOCAL_VERSION, payload: localResponse.data });

    try {
      let url = `${this.cloudurl}version/?format=json`
      response = await axios.get(url, {
        headers: { 'Content-Type': 'application/json' },
      });
    } catch (error) {
      console.log(error);
      return;
    }
    if (response.statusText !== "OK") {
      return;
    }
    let cloudResp = response.data;
    if (cloudResp.SensiML_Open_Gateway_Windows) {
      this.cloudVersion = cloudResp.SensiML_Open_Gateway_Windows;
      store.dispatch({ type: UPDATE_CLOUD_VERSION, payload: cloudResp.SensiML_Open_Gateway_Windows });
      store.dispatch({ type: UPDATE_AVAILABLE, payload: (this.localVersion < this.cloudVersion) });
    }

  }
}
