import React, { useState, useEffect } from "react";
import axios from "axios";
import { Typography } from "@material-ui/core";
import { Grid } from "@material-ui/core";
import Button from "@material-ui/core/Button";
import { makeStyles, useTheme } from "@material-ui/core/styles";
import { createMuiTheme } from "@material-ui/core/styles";

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
    margin: theme.spacing(3, 2),
  },
  section2: {
    margin: theme.spacing(2),
    textAlign: "center",
  },
}));

const Connected = (props) => {
  return (
    <Grid>
      {props.isConnected ? (
        <Button color="green" variant="contained" aria-label="disconnect">
          Connected
        </Button>
      ) : (
        <Button color="red" variant="contained" aria-label="disconnect">
          Disconnected
        </Button>
      )}
    </Grid>
  );
};

const Status = (props) => {
  const classes = useStyles();
  const theme = useTheme();
  let [config, setConfig] = useState([]);

  useEffect(() => {
    axios
      .get(`${process.env.REACT_APP_API_URL}config`)
      .then((res) => setConfig(mapdata(res.data)));
  }, []);

  const handleDisconnectRequest = (event, setConfig) => {
    axios
      .get(`${process.env.REACT_APP_API_URL}disconnect`)
      .then((res) => setConfig(mapdata(res.data)));
  };

  const handleConnectRequest = (event, setConfig) => {
    axios
      .get(`${process.env.REACT_APP_API_URL}connect`)
      .then((res) => setConfig(mapdata(res.data)));
  };

  function mapdata(data) {
    if (data.mode) {
      props.setStreamingMode(data.mode);
    }
    data.streaming = data.streaming ? "Yes" : "No";
    props.setColumns(Object.keys(data.column_location).sort());
    props.setStreamingSource(data.source);
    props.setDeviceID(data.device_id);
    data.column_location =
      "column_location" in data
        ? Object.keys(data.column_location).sort().join(", ")
        : [];

    return data;
  }
  return (
    <Grid>
      <Grid container spacing={2} rows>
        <Grid item xs={8}>
          <Connected isConnected={config.streaming}></Connected>
        </Grid>
        <Grid item xs={4}>
          <div className={classes.controls}>
            <Grid container rows spacing={2}>
              <Grid item>
                <Button
                  color="secondary"
                  variant="contained"
                  aria-label="connect"
                  onClick={() => {
                    handleConnectRequest("clicked", setConfig);
                  }}
                >
                  Connect
                </Button>
              </Grid>
              <Grid item>
                <Button
                  color="secondary"
                  variant="contained"
                  aria-label="disconnect"
                  onClick={() => {
                    handleDisconnectRequest("clicked", setConfig);
                  }}
                >
                  Disconnect
                </Button>
              </Grid>
            </Grid>
          </div>
        </Grid>
      </Grid>

      <Grid xs={12}>
        <Grid>
          <Typography color="primary"> Configured Mode: </Typography>
          <Typography>{config.mode}</Typography>

          <Typography color="primary">Sensors: </Typography>
          <Typography>{config.source}</Typography>
          <Typography color="primary">Device ID: </Typography>
          <Typography>{config.device_id}</Typography>
        </Grid>
        {config.mode === "data_capture" ? (
          <Grid>
            <Typography color="primary">Sample Rate: </Typography>
            <Typography>{config.sample_rate}</Typography>
            <Typography color="primary">Columns:</Typography>
            <Typography>{config.column_location}</Typography>
          </Grid>
        ) : (
          <></>
        )}
      </Grid>
    </Grid>
  );
};

export default Status;
