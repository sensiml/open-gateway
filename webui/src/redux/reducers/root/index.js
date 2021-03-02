import {
  SET_GLOBAL_LOADER,
} from '../../actions/actionTypes';

const initialState = {
  globalLoader: false,
};


export default function rootData(state = initialState, action) {
  switch (action.type) {
    case SET_GLOBAL_LOADER:
      return {
        ...state,
        globalLoader: action.payload || false,
      };
    default:
      return state;
  }
}