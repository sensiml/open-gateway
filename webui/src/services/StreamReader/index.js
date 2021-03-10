import { BaseStreamHttpError } from "./errors";

import store from "../../redux/store";

class StreamReader {
  /* *
   * StreamReader class based on browser fetch method for handling stream data to
   * @constructs
   * @param {string} fetchUrl - endpoint fetch url
   * */
  constructor(fetchUrl) {
    /* @param {string} fetchUrl - endpoint fetch url */
    this.reader = undefined;
    this.fetchUrl = fetchUrl;
  }

  async startStreaming() {
    /*
      fetch streaming endpoint and setup this.reader
    */
    let response;
    console.log("getting response");
    try {
      response = await fetch(this.fetchUrl);
    } catch (error) {
      console.log(error);
      throw new BaseStreamHttpError(404, {
        detail: "Failed to fetch API service",
      });
    }
    if (!response.ok) {
      throw new BaseStreamHttpError(response.status, {
        detail: response.statusText,
      });
    }
    console.log("getting reader");
    this.reader = response.body.getReader();
  }

  async stopStreaming() {
    if (this.reader) {
      this.reader.cancel();
      this.reader = undefined;
    }
  }

  async readStreamToRedux(actionType, countSamples = 0) {
    /*
      read and write array by chunk to redux
      @param {string} actionType - redux action const name
      @param {number} maxLength - max length of redux streamed array
    * */
    while (true) {
      const { value, done } = await this.reader.read();
      if (done) break;
      store.dispatch({
        type: actionType,
        payload: { chunk: new Int16Array(value.buffer), countSamples },
      });
    }
  }
}

export { BaseStreamHttpError };
export default StreamReader;
