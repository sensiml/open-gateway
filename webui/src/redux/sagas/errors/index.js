import { call, delay, put, takeEvery } from "redux-saga/effects";

import {
  FETCH_DATA_ERROR_MSG,
  SET_DATA_ERROR_MSG,
} from "../../actions/actionTypes";

function* handleErrorMsg(action) {
  yield put({ type: SET_DATA_ERROR_MSG, payload: action.payload });
  yield delay(1000);
  yield put({ type: SET_DATA_ERROR_MSG, payload: null });
}

export default function* watchErrorSaga() {
  yield takeEvery(FETCH_DATA_ERROR_MSG, handleErrorMsg);
}
