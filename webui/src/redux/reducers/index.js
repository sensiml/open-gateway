import { combineReducers } from "redux";
// modules
import rootData from "./root";
import errors from "./errors";
import streamData from "./stream";
import sensorData from "./sensorData";

const createAppReducer = () => combineReducers({
  root: rootData,
  errors,
  stream: streamData,
  sensorData,
});

export default createAppReducer;