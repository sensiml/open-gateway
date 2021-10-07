import axios from "axios";
import store from "../../redux/store";
import {BaseStreamHttpError} from "../StreamReader";
import {createProxyMiddleware} from "http-proxy-middleware";

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
        this.localVersion = localResponse.data;

        try {
            let url = `${this.cloudurl}version/?format=json`
            response = await axios.get(url, {
                headers: {'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'},
                crossdomain:true,
                proxy: createProxyMiddleware({target: `${this.cloudurl}`, changeOrigin: true})
            });
        } catch (error) {
            console.log(error);
            this.cloudVersion = "";
            return;
        }
        if (response.statusText !== "OK") {
            this.cloudVersion = "";
            return;
        }
        var cloudjson = response.data;
        if(cloudjson.SensiML_Open_Gateway_Windows) {
            this.cloudVersion = cloudjson.SensiML_Open_Gateway_Windows;
        }
        this.updateAvailable = this.localVersion < this.cloudVersion;
    }
}
