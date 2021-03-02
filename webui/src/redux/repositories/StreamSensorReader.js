import StreamReader from "../../services/StreamReader";
import { apiHosts } from "../../configs";

export let streamSensorReader = undefined;

export const initStreamSensorReader = () => {
  streamSensorReader = new StreamReader(`${ apiHosts.baseHost }/stream`);
};