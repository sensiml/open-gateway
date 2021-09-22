import _ from "lodash";
import { APP_API_URL } from "../../../configs";

export const selectClassImage = className => (state) => {
  const { classMapImages } = state.classes;
  const classNameValid = _.toString(className);

  if (classMapImages && classNameValid) {
    const imgPath = classMapImages[classNameValid];
    if (imgPath) {
      console.log("imgPath", imgPath)
      return `${APP_API_URL}${imgPath}`;
    }
    return "";
  }
  return "";
};
