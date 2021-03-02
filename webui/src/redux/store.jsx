import createSagaMiddleware from "redux-saga";

import { applyMiddleware, createStore } from "redux";
import { composeWithDevTools } from "redux-devtools-extension";

import rootSaga from "./sagas";
import createAppReducer from "./reducers";

const sagaMiddleware = createSagaMiddleware();
const enhancers = [];

const middleware = [
  sagaMiddleware,
];

const composedEnhancers = composeWithDevTools(
  applyMiddleware(...middleware),
  ...enhancers,
);

const appReducer = createAppReducer();

const store = createStore(
  appReducer,
  composedEnhancers,
);

sagaMiddleware.run(rootSaga);

export default store;
