import React, { useCallback, useEffect, useLayoutEffect, useState } from "react";
import _ from "lodash";
import { GameMode } from "components/GameMode";

import { Header, NavBar } from "../Layout";
import useStyles from "./MainStyles";
import { Grid } from "@material-ui/core";
import { Configure } from "../Configure";
import { TestMode } from "../TestMode";
import CssBaseline from "@material-ui/core/CssBaseline";
import { useSnackbar } from "notistack";
import { useDispatch, useSelector, } from "react-redux";
import { STOP_STREAM_SENSOR_SAGA, FETCH_CLASS_MAP_IMAGES } from "../../redux/actions/actionTypes";
import axios from "axios";


const Main = (props) => {

  const dispatch = useDispatch();
  const [activeView, setActiveView] = React.useState(0);
  const [streamingMode, setStreamingMode] = React.useState('DATA_CAPTURE');
  const [streamingSampleRate, setStreamingSampleRate] = React.useState("16000");
  const [streamingSource, setStreamingSource] = React.useState(null);
  const [columns, setColumns] = React.useState([]);
  const [deviceID, setDeviceID] = React.useState([]);
  const [isConnected, setIsConnected] = React.useState(false);
  const [isCameraConnected, setIsCameraConnected] = React.useState(false);
  const [isRecording, setIsRecording] = React.useState(false);
  const [baudRate, setBaudRate] = React.useState(null);
  const [config, setConfig] = React.useState({});
  const [firstLoad, setFirstLoad] = React.useState(null);
  const [dataType, setDataType] = React.useState('int16');
  const [gameModeAssets, setGameModeAssets] = useState({});

  const { enqueueSnackbar, closeSnackbar } = useSnackbar();
  const { isStreamingSensor } = useSelector((state) => state.stream);
  const { classMapImages } = useSelector((state) => state.classes);
  const { errorDataMsg } = useSelector((state) => state.errors);

  function handleChange(newValue) {
    if (activeView !== newValue) {
      setActiveView(newValue);
    }
  }

  function mapdata(data) {
    if (data.mode) {
      setStreamingMode(data.mode);
    }
    if (data.sample_rate) {
      setStreamingSampleRate(data.sample_rate);
    }
    setIsConnected(data.streaming);
    setColumns(Object.keys(data.column_location).sort());
    setStreamingSource(data.source?.toUpperCase());
    setDeviceID(data.device_id);
    setIsCameraConnected(data.camera_on);
    setBaudRate(data.baud_rate);

    switch (data.data_type) {
      case ('int16'):
        setDataType('int16');
        break;
      case ('float'):
        setDataType('float');
        break;
      default:
        setDataType('int16');
    }

    data.column_location =
      "column_location" in data
        ? Object.keys(data.column_location).sort().join(", ")
        : [];

    setConfig(data);
  }

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

  const fetchClassMapImages = useCallback(
    () => dispatch({ type: FETCH_CLASS_MAP_IMAGES }),
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


  useEffect(() => {
    if (activeView === 2) {
      axios.get(`${process.env.REACT_APP_API_URL}game-demo-asset`, {}).then((response) => {
        setGameModeAssets(response.data);
        console.log("setGameModeAssets", response.data);
      });
    }

    axios.get(`${process.env.REACT_APP_API_URL}config`, {}).then((response) => {
      mapdata(response.data);
      console.log(response.data)
    });
    fetchClassMapImages();
  }, [activeView]);

  useLayoutEffect(() => {
    axios.get(`${process.env.REACT_APP_API_URL}config`, {}).then((response) => {
      mapdata(response.data);
    });
  }, []);

  const classes = useStyles();

  return (
    <div className={classes.root}>
      <CssBaseline />
      {activeView === 2 && !_.isEmpty(gameModeAssets) ?
        <GameMode
          classMapImages={classMapImages}
          audioAction={gameModeAssets.action_audio && `${process.env.REACT_APP_API_URL}${gameModeAssets.action_audio}`}
          audioSuccess={gameModeAssets.winner_audio && `${process.env.REACT_APP_API_URL}${gameModeAssets.winner_audio}`}
          audioFail={gameModeAssets.loser_audio && `${process.env.REACT_APP_API_URL}${gameModeAssets.loser_audio}`}
          winnerImg={gameModeAssets.winner_img && `${process.env.REACT_APP_API_URL}${gameModeAssets.winner_img}`}
          loserImg={gameModeAssets.loser_img && `${process.env.REACT_APP_API_URL}${gameModeAssets.loser_img}`}
          countdownTimeDefault={gameModeAssets.countdown_timer}
          winnerCountThreshold={gameModeAssets.winner_classification_count_threshold}
          winnerText={gameModeAssets.loser_text}
          loserText={gameModeAssets.winner_text}
          onClose={() => handleChange(1)}
        />
        :
        <Grid container direction="column" justify="center" alignItems="center">
          <Header />
          <NavBar
            onChange={handleChange}
            isConnected={isConnected}
            isCameraConnected={isCameraConnected}

          />
          <main className={classes.content}>
            {activeView === 0 ? (
              <Configure
                streamingMode={streamingMode}
                streamingSampleRate={streamingSampleRate}
                deviceID={deviceID}
                setStreamingMode={setStreamingMode}
                setStreamingSampleRate={setStreamingSampleRate}
                setColumns={setColumns}
                setStreamingSource={setStreamingSource}
                setDeviceID={setDeviceID}
                setIsConnected={setIsConnected}
                isConnected={isConnected}
                setIsCameraConnected={setIsCameraConnected}
                isCameraConnected={isCameraConnected}
                config={config}
                setConfig={setConfig}
                streamingSource={streamingSource}
                baudRate={baudRate}
                setBaudRate={setBaudRate}
              />
            ) : null}
            {activeView === 1 ? (
              <TestMode
                columns={columns}
                streamingMode={streamingMode}
                streamingSampleRate={streamingSampleRate}
                isConnected={isConnected}
                isRecording={isRecording}
                isCameraConnected={isCameraConnected}
                setIsCameraConnected={setIsCameraConnected}
                samplerate={config.samplerate}
                dataType={dataType}
              />
            ) : null}
          </main>
        </Grid>
      }
    </div>
  );
};

export default Main;
