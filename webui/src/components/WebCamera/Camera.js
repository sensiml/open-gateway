import React, { useState, useEffect } from "react";
import { Grid } from "@material-ui/core";

const Camera = (props) => {
  console.log(props);
  return (
    <img
      src={"http://localhost:5555/stream-video" + "?" + props.cameraKey}
      alt="Camera Not Started."
    />
  );
};

export default Camera;
