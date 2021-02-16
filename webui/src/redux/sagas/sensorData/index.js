import { all, fork } from "redux-saga/effects";

import watchSetChunkSensorData from "./watchSetChunkSensorData";

export default function* sensorDataSagas() {
  yield all([
    fork(watchSetChunkSensorData),
  ]);
}
