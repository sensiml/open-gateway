import { Button, Card, CardContent, Grid, Typography } from "@material-ui/core";
import Divider from "@material-ui/core/Divider";
import { makeStyles, useTheme } from "@material-ui/core/styles";
import axios from "axios";
import React from "react";
import Camera from "./Camera";
const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
  },
  details: {
    display: "flex",
    flexDirection: "column",
  },
  content: {
    flex: "1 0 auto",
  },
  controls: {
    display: "flex",
    alignItems: "center",
    paddingLeft: theme.spacing(1),
    paddingBottom: theme.spacing(1),
  },
  section1: {
    margin: theme.spacing(2, 0, 3, 0),
  },
  section2: {
    margin: theme.spacing(2),
    textAlign: "center",
  },
  divWrapper: {
    margin: theme.spacing(3),
    padding: theme.spacing(2, 2, 2, 2),
    maxWidth: 800,
    minHeight: 800,
  },
}));

const handleCameraRequest = (
  event,
  setCameraView,
  setIsCameraConnected,
  setCameraKey
) => {
  console.log(event);

  axios
    .post(`${process.env.REACT_APP_API_URL}config-video`, {
      camera_index: 0,
      event_type: event,
    })
    .then((response) => {
      console.log(response.data);
      if (event == "camera-on") {
        setCameraView(true);
        setIsCameraConnected(true);
        setCameraKey(Math.random().toString(36).substring(7));
        console.log("caera event");
        console.log(event);
      }
      if (event == "camera-off") {
        setCameraView(false);
        setIsCameraConnected(false);
        console.log("caera event");
        console.log(event);
      }
    });
};

const WebCamera = (props) => {
  const classes = useStyles();
  const [cameraView, setCameraView] = React.useState(false);
  const [cameraKey, setCameraKey] = React.useState("");

  /*  useEffect(() => {
    axios
      .get(`${process.env.REACT_APP_API_URL}config-video`, {})
      .then((response) => {
        setCameraView(response.data.camera_on);
        setRecording(response.data.camera_record);
        //console.log(response.data);
      });
  });
*/

  return (
    <div>
      <div className={classes.section1}>
        <Typography component="h3" variant="h3" color="secondary">
          Video Source
        </Typography>
      </div>
      <div className={classes.section1}>
        <Divider variant="middle" />
      </div>

      <Camera
        cameraKey={cameraKey}
        cameraView={props.isCameraConnected}
      ></Camera>
      <div className={classes.section2}>
        <Typography variant="subtitle1" color="textSecondary"></Typography>
      </div>

      <div className={classes.details}>
        <Grid container rows spacing={2}>
          <Grid item xs={12}>
            {props.isCameraConnected === false ? (
              <Button
                aria-label="Start Camera"
                variant="contained"
                color="primary"
                fullWidth={true}
                onClick={() => {
                  handleCameraRequest(
                    "camera-on",
                    setCameraView,
                    props.setIsCameraConnected,
                    setCameraKey
                  );
                }}
              >
                Connect to Camera
              </Button>
            ) : (
              <Button
                aria-label="Stop Camera"
                color="primary"
                variant="contained"
                fullWidth={true}
                onClick={() => {
                  handleCameraRequest(
                    "camera-off",
                    setCameraView,
                    props.setIsCameraConnected,
                    setCameraKey
                  );
                }}
              >
                Disconnect From Camera
              </Button>
            )}
          </Grid>
        </Grid>
      </div>
    </div>
  );
};

export default WebCamera;
