import {
  Box,
  Button,
  Card,
  CardContent,
  Grid,
  Switch,
  Typography,
} from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import React, { useCallback, useEffect, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import {
  SET_STREAM_SENSOR_DATA_RESET,
  START_STREAM_SENSOR_SAGA,
  STOP_STREAM_SENSOR_SAGA,
} from "../../redux/actions/actionTypes";
import {
  sensorDataForChart,
  sensorRecordedDataToCsv,
} from "../../redux/selectors/sensorData";
import SensorDataChart from "./SensorDataChart";

const useStyles = makeStyles((theme) => ({
  cardWrapper: {
    padding: theme.spacing(2),
  },
  dataWrapper: {
    padding: theme.spacing(2),
  },
  chartWrapper: {
    width: "100%",
    margin: theme.spacing(1),
  },
  buttonWrapper: {
    display: "flex",
    marginTop: theme.spacing(2),
  },
  button: {
    marginLeft: theme.spacing(2),
  },
  zeroOpacity: {
    opacity: "0",
  },
}));

const SensorStream = (props) => {
  const COUNT_SAMPLES = 1000;
  const { columns } = props;
  const classes = useStyles();
  const dispatch = useDispatch();
  const [isSplitCharts, SetIsSplitCharts] = useState(false);
  const { isStreamingSensor, isStreamingSensorRecording } = useSelector(
    (state) => state.stream
  );
  const sensorData = useSelector(sensorDataForChart(columns));

  const startSensorStreaming = useCallback(
    // max array is COUNT_SAMPLES * count of data types
    () =>
      dispatch({
        type: START_STREAM_SENSOR_SAGA,
        payload: {
          countSamples: COUNT_SAMPLES * ((columns && columns?.length) || 1),
        },
      }),
    [dispatch]
  );

  const stopSensorStreaming = useCallback(
    () => dispatch({ type: STOP_STREAM_SENSOR_SAGA }),
    [dispatch]
  );

  const setClearStream = useCallback(
    () => dispatch({ type: SET_STREAM_SENSOR_DATA_RESET, payload: [] }),
    [dispatch]
  );

  const switchSplitChart = () => {
    SetIsSplitCharts(!isSplitCharts);
  };

  const manageStream = () => {
    console.log("streaming", isStreamingSensor);
    if (isStreamingSensor) {
      stopSensorStreaming();
    } else {
      setClearStream();
      startSensorStreaming();
    }
  };

  useEffect(() => {
    if (!props.isConnected && isStreamingSensor){
        stopSensorStreaming();
        setClearStream();      
      } 

  }, []);

  return (
    <Card>
      <CardContent>
        <Typography component="h3" variant="h3" color="secondary">
          Test Mode: Data Capture
        </Typography>
        <Box className={classes.dataWrapper}>
          <Box className={classes.chartWrapper}>
            <Box className={!isStreamingSensor && classes.zeroOpacity}>
              <Switch
                checked={isSplitCharts}
                onChange={() => switchSplitChart()}
                inputProps={{ "aria-label": "secondary checkbox" }}
              />{" "}
              Split charts
            </Box>
            {sensorData && sensorData.length && isSplitCharts ? (
              sensorData.map((data) => (
                <SensorDataChart
                  title={data.name}
                  countSamples={COUNT_SAMPLES}
                  sensorData={[data]}
                  isStreamingSensor={isStreamingSensor}
                />
              ))
            ) : (
              <SensorDataChart
                countSamples={COUNT_SAMPLES}
                sensorData={sensorData}
                isStreamingSensor={isStreamingSensor}
              />
            )}
          </Box>
          <Box className={classes.buttonWrapper}>
            <Button
              variant="contained"
              color="primary"
              className={classes.button}
              onClick={() => manageStream()}
            >
              {isStreamingSensor ? "Stop" : "View"}
            </Button>
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
};

export default SensorStream;
