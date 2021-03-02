import React, { useCallback, useEffect } from "react";

import { Header, NavBar } from "../Layout";
import useStyles from "./MainStyles";
import { Grid } from "@material-ui/core";
import { Status } from "../Status";
import { Configure } from "../Configure";
import { TestMode } from "../TestMode";
import CssBaseline from "@material-ui/core/CssBaseline";
import { useSnackbar } from "notistack";
import { useDispatch, useSelector } from "react-redux";
import { STOP_STREAM_SENSOR_SAGA } from "../../redux/actions/actionTypes";
import axios from "axios";

const Main = () => {
  const dispatch = useDispatch();
  const [activeView, setActiveView] = React.useState(0);
  const [streamingMode, setStreamingMode] = React.useState(0);
  const [streamingSource, setStreamingSource] = React.useState(0);
  const [columns, setColumns] = React.useState([]);
  const [deviceID, setDeviceID] = React.useState([]);
  const [isConnected, setIsConnected] = React.useState(false);
  const [isCameraConnected, setIsCameraConnected] = React.useState(false);
  const [isRecording, setIsRecording] = React.useState(false);

  const { enqueueSnackbar, closeSnackbar } = useSnackbar();
  const { isStreamingSensor } = useSelector((state) => state.stream);
  const { errorDataMsg } = useSelector((state) => state.errors);

  function handleChange(newValue) {
    if (activeView !== newValue) {
      setActiveView(newValue);
    }
  }

  useEffect(() => {
    axios.get(`${process.env.REACT_APP_API_URL}config`, {}).then((response) => {
      setIsCameraConnected(response.data.camera_on);
      setIsConnected(response.data.streaming);
      setIsRecording(response.data.recording);

      //console.log(response.data);
    });
  });

  const alertUser = (e) => {
    if (isStreamingSensor) {
      e.preventDefault();
      e.returnValue = "";
    }
  };

  const stopSensorStreaming = useCallback(
    () => dispatch({ type: STOP_STREAM_SENSOR_SAGA }),
    [dispatch]
  );

  // before leave handler
  useEffect(() => {
    if (isStreamingSensor) {
      window.addEventListener("beforeunload", alertUser);
      window.addEventListener("unload", stopSensorStreaming);
      return () => {
        window.removeEventListener("beforeunload", alertUser);
        window.removeEventListener("unload", stopSensorStreaming);
        stopSensorStreaming();
      };
    }
  }, [isStreamingSensor]);

  useEffect(() => {
    if (errorDataMsg) {
      enqueueSnackbar(errorDataMsg, { variant: "warning" });
    }
  }, [errorDataMsg]);

  const classes = useStyles();
  return (
    <div className={classes.root}>
      <CssBaseline />
      <Grid container direction="column" justify="center" alignItems="center">
        <Header />
        <NavBar
          onChange={handleChange}
          isConnected={isConnected}
          isCameraConnected={isCameraConnected}
        />
        <main className={classes.content}>
          {activeView === 0 ? (
            <Status
              setStreamingMode={setStreamingMode}
              setColumns={setColumns}
              setStreamingSource={setStreamingSource}
              setDeviceID={setDeviceID}
              setIsConnected={setIsConnected}
              isConnected={isConnected}
              setIsCameraConnected={setIsCameraConnected}
              isCameraConnected={isCameraConnected}
            />
          ) : null}
          {activeView === 1 ? (
            <TestMode
              columns={columns}
              streamingMode={streamingMode}
              isRecording={isRecording}
              isCameraConnected={isCameraConnected}
            />
          ) : null}
          {activeView === 2 ? (
            <Configure
              setStreamingMode={setStreamingMode}
              streamingSource={streamingSource}
              streamingMode={streamingMode}
              deviceID={deviceID}
              setIsConnected={setIsConnected}
            />
          ) : null}
        </main>
      </Grid>
    </div>
  );
};

export default Main;
