import { call, put, takeLatest } from "redux-saga/effects";
import { streamSensorReader } from "../../repositories/StreamSensorReader";
import { SET_IS_STREAMING_SENSOR, STOP_STREAM_SENSOR_SAGA, } from "../../actions/actionTypes";


function* workerStreamStop(action) {
  try {
    yield call([streamSensorReader, 'stopStreaming']);
    yield put({ type: SET_IS_STREAMING_SENSOR, payload: false });
  } catch (e) {
    console.debug(e);
  }
}

export default function* watchStreamSensorStop() {
  yield takeLatest(STOP_STREAM_SENSOR_SAGA, workerStreamStop);
}
