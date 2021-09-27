import { all, fork } from "redux-saga/effects";

import watchErrorSaga from "./errors";
import streamSagas from "./stream";
import sensorDataSagas from "./sensorData";
import classesSagas from "./classes";

export default function* rootSaga() {
  yield all([
    fork(streamSagas),
    fork(watchErrorSaga),
    fork(sensorDataSagas),
    fork(classesSagas),
  ]);
}
