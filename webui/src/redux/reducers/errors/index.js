import { SET_DATA_ERROR_MSG } from "../../actions/actionTypes";

const initialState = {
  errorDataMsg: null,
};

export default function rootData(state = initialState, action) {
  switch (action.type) {
    case SET_DATA_ERROR_MSG:
      return {
        ...state,
        errorDataMsg: action.payload,
      };
    default:
      return state;
  }
}