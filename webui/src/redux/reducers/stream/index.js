import { SET_IS_STREAMING_SENSOR, SET_IS_STREAMING_SENSOR_RECORDING, } from "../../actions/actionTypes";

const initialState = {
  isStreamingSensor: false,
  isStreamingSensorRecording: false,
};

export default function streamData(state = initialState, action) {
  switch (action.type) {
    case SET_IS_STREAMING_SENSOR:
      return {
        ...state,
        isStreamingSensor: action.payload,
      };
    case SET_IS_STREAMING_SENSOR_RECORDING:
      return {
        ...state,
        isStreamingSensorRecording: action.payload,
      };
    default:
      return state;
  }
}