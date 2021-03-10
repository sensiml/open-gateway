import { call, put, takeLatest } from "redux-saga/effects";

import { streamSensorReader } from "../../repositories/StreamSensorReader";
import { BaseStreamHttpError } from "../../../services/StreamReader";
import {
  FETCH_DATA_ERROR_MSG,
  SET_CHUNK_SENSOR_DATA_SAGA,
  SET_IS_STREAMING_SENSOR,
  START_STREAM_SENSOR_SAGA,
} from "../../actions/actionTypes";

function* workerStreamStart(action) {
  try {
    const { countSamples } = action?.payload;
    yield call([streamSensorReader, "startStreaming"]);
    yield put({ type: SET_IS_STREAMING_SENSOR, payload: true });
    yield call(
      [streamSensorReader, "readStreamToRedux"],
      SET_CHUNK_SENSOR_DATA_SAGA,
      countSamples
    );
  } catch (e) {
    console.debug(e);
    if (e instanceof BaseStreamHttpError) {
      yield put({ type: FETCH_DATA_ERROR_MSG, payload: e.detail });
    } else {
      yield put({
        type: FETCH_DATA_ERROR_MSG,
        payload: "Failed to read stream data",
      });
    }
  }
}

export default function* watchStreamSensorStart() {
  yield takeLatest(START_STREAM_SENSOR_SAGA, workerStreamStart);
}
