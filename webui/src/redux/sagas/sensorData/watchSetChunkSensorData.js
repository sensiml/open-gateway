import { put, select, takeLatest } from "redux-saga/effects";
import {
  SET_CHUNK_SENSOR_DATA_SAGA,
  SET_STREAM_SENSOR_DATA,
  SET_STREAM_SENSOR_RECORD_DATA,
} from "../../actions/actionTypes";

function* workerSetStreamChunkSensorData(action) {
  try {
    const { chunk, countSamples } = action.payload;
    const chunkLength = (chunk && chunk.length) || 0;
    let updatedSensorSimpleData = [];

    const { sensorSimpleData, sensorRecordedData } = yield select(
      (state) => state.sensorData
    );
    const { isStreamingSensorRecording } = yield select(
      (state) => state.stream
    );
    console.log("called", chunkLength / (2 * 6));

    // when chunk greater than max of count samples set all chunk data or if countSamples == 0
    if (chunkLength >= countSamples) {
      updatedSensorSimpleData = [...chunk];
    } else if (sensorSimpleData.length >= countSamples) {
      // when reach countSamples limit
      updatedSensorSimpleData = [...sensorSimpleData];
      let [left, right, chunkI] = [0, sensorSimpleData.length, 0];
      while (left < right) {
        if (right - left > chunkLength) {
          updatedSensorSimpleData[left] = sensorSimpleData[left + chunkLength];
        } else {
          updatedSensorSimpleData[left] = chunk[chunkI];
          chunkI++;
        }
        left++;
      }
    } else {
      updatedSensorSimpleData = [...sensorSimpleData, ...chunk];
    }

    yield put({
      type: SET_STREAM_SENSOR_DATA,
      payload: updatedSensorSimpleData,
    });
    // update whole list if recording
    if (isStreamingSensorRecording) {
      yield put({
        type: SET_STREAM_SENSOR_RECORD_DATA,
        payload: [...sensorRecordedData, ...chunk],
      });
    }
  } catch (e) {
    console.debug(e);
  }
}

export default function* watchSetChunkSensorData() {
  yield takeLatest(SET_CHUNK_SENSOR_DATA_SAGA, workerSetStreamChunkSensorData);
}
