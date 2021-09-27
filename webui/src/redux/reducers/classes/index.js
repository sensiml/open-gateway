import { SET_CLASS_MAP_IMAGES } from "../../actions/actionTypes";

const initialState = {
  classMapImages: {},
};

export default function classesData(state = initialState, action) {
  switch (action.type) {
    case SET_CLASS_MAP_IMAGES:
      return {
        ...state,
        classMapImages: action.payload,
      };
    default:
      return state;
  }
};
