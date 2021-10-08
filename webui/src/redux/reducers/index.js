import { combineReducers } from "redux";
// modules
import rootData from "./root";
import errors from "./errors";
import streamData from "./stream";
import sensorData from "./sensorData";
import classesData from "./classes";
import versionData from "./version";

const createAppReducer = () => combineReducers({
  root: rootData,
  errors,
  stream: streamData,
  sensorData,
  versionData,
  classes: classesData,
});

export default createAppReducer;
