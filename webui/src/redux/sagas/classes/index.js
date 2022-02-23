/* eslint-disable require-yield */
import _ from "lodash";
import { put, takeEvery } from "redux-saga/effects";

import ApiService from "../../../services/api";
import {
  FETCH_CLASS_MAP_IMAGES,
  SET_CLASS_MAP_IMAGES,
} from "../../actions/actionTypes";

function* classesMapImagesSagas() {
  const reponse = yield ApiService.get("class-map-images");
  yield console.log("classesMapImagesSagas");
  if (!_.isEmpty(reponse.data)) {
    const payload = yield _.reduce(
      reponse.data,
      (acc, el) => {
        acc[el.name] = el.img;
        return acc;
      },
      [{}]
    );
    yield put({ type: SET_CLASS_MAP_IMAGES, payload });
  }
}

export default function* watchErrorSaga() {
  yield takeEvery(FETCH_CLASS_MAP_IMAGES, classesMapImagesSagas);
}
