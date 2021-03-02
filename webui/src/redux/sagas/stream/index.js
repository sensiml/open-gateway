import { all, fork } from "redux-saga/effects";

import watchStreamSensorStart from "./watchStreamSensorStart";
import watchStreamSensorStop from "./watchStreamSensorStop";

export default function* streamSagas() {
  yield all([
    fork(watchStreamSensorStart),
    fork(watchStreamSensorStop),
  ]);
}

