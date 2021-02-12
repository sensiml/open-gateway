import React, { useState, useEffect } from "react";
import axios from "axios";
import { Typography } from "@material-ui/core";
import { Grid } from "@material-ui/core";
import Button from "@material-ui/core/Button";




const Configure = (props) => {
  let [config, setConfig] = useState([]);


  useEffect(() => {
    axios
      .get(`${process.env.REACT_APP_API_URL}config`)
      .then((res) => setConfig(mapdata(res.data)));
  }, []);


  const handleDisconnectRequest = (event, setConfig) => {
    axios.get(`${process.env.REACT_APP_API_URL}disconnect`).then((res) => setConfig(mapdata(res.data)))
  };


  const handleConnectRequest = (event, setConfig) => {
    axios.get(`${process.env.REACT_APP_API_URL}connect`).then((res) => setConfig(mapdata(res.data)))
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
      <Grid xs={12}>
        <Grid>
          <Typography color="primary"> Configured Mode: </Typography>
          <Typography>{config.mode}</Typography>
          <Typography color="primary">Streaming: </Typography>
          <Typography>{config.streaming}</Typography>
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
      <Grid container rows spacing={2}>
        <Grid item>
          <Button
            color="secondary"
            variant="contained"
            aria-label="disconnect"
            onClick={() => {
              handleDisconnectRequest("clicked", setConfig);
            }}
          >
            Connect Source
        </Button>
        </Grid>
        <Grid item>
          <Button
            color="secondary"
            variant="contained"
            aria-label="disconnect"
            onClick={() => {
              handleConnectRequest("clicked", setConfig);
            }}
          >
            Disconnect Source
        </Button>
        </Grid>
      </Grid>

    </Grid>

  );
};

export default Configure;
