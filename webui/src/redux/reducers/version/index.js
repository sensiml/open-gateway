import {
  UPDATE_CLOUD_VERSION,
  UPDATE_AVAILABLE,
  UPDATE_LOCAL_VERSION,
} from "../../actions/actionTypes";

const initialState = {
  localVersion: "",
  cloudVersion: "",
  updateAvailable: false
}

export default function versionData(state = initialState, action) {
  switch (action.type) {
    case UPDATE_CLOUD_VERSION:
      return {
        ...state,
        cloudVersion: action.payload
      };
    case UPDATE_AVAILABLE:
      return {
        ...state,
        updateAvailable: state.localVersion < state.cloudVersion
      };
    case UPDATE_LOCAL_VERSION:
      return {
        ...state,
        localVersion: action.payload,
      };
    default:
      return state;
  }
};
