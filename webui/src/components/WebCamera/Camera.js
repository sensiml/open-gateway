import React from "react";
import {
  Box,
} from "@material-ui/core";


const Camera = ({ cameraKey, classes, isCameraConnected }) => {
  return (
    <Box className={classes.cameraViewWrapper}>
    { isCameraConnected ?
      <img
        src={`http://localhost:5555/stream-video?${cameraKey}`}
        alt="Camera"
      />
      : "Video Source is not connected"
    }
    </Box>
  );
};

export default Camera;
