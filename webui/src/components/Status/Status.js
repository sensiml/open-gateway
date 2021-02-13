import React, { useState, useEffect } from "react";
import axios from "axios";
import { CardContent, Typography } from "@material-ui/core";
import { Grid } from "@material-ui/core";
import Button from "@material-ui/core/Button";
import { makeStyles, useTheme } from "@material-ui/core/styles";
import { createMuiTheme } from "@material-ui/core/styles";
import { SimpleCard } from "../SimpleCard";
import Card from "@material-ui/core/Card";

const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
    width: "700px",
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
  },
}));

const Status = (props) => {
  const classes = useStyles();
  const theme = useTheme();
  let [config, setConfig] = useState([]);

  useEffect(() => {
    axios.get(`${process.env.REACT_APP_API_URL}config`).then((res) => {
      setConfig(mapdata(res.data));
    });
  }, []);

  const handleDisconnectRequest = (event, setConfig) => {
    axios.get(`${process.env.REACT_APP_API_URL}disconnect`).then((res) => {
      console.log(res.data);
      setConfig(mapdata(res.data));
    });
  };

  const handleConnectRequest = (event, setConfig) => {
    axios.get(`${process.env.REACT_APP_API_URL}connect`).then((res) => {
      setConfig(mapdata(res.data));
    });
  };

  function mapdata(data) {
    if (data.mode) {
      props.setStreamingMode(data.mode);
    }
    props.setIsConnected(data.streaming);
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
    <div class={classes.root}>
      <Card>
        <CardContent>
          <Grid container columns spacing={4}>
            <Grid item xs={12} container rows spacing={2}>
              <SimpleCard name="Mode" xs="6" value={config.mode}></SimpleCard>
              <SimpleCard
                name="Source"
                xs="6"
                value={config.source}
              ></SimpleCard>
            </Grid>
            <Grid item xs={12} container rows spacing={2}>
              <SimpleCard
                name="Device ID"
                xs={6}
                value={config.device_id}
              ></SimpleCard>
              {config.mode === "data_capture" ? (
                <SimpleCard
                  xs="6"
                  name="Sample Rate"
                  value={config.sample_rate}
                ></SimpleCard>
              ) : null}
            </Grid>
            <Grid item xs={12}>
              {config.mode === "data_capture" ? (
                <SimpleCard
                  name="Sensor Columns"
                  value={config.column_location}
                  list={true}
                ></SimpleCard>
              ) : null}
            </Grid>
            <Grid item xs={12}>
              <div className={classes.controls}>
                {props.isConnected ? (
                  <Button
                    color="secondary"
                    variant="contained"
                    aria-label="disconnect"
                    fullWidth={true}
                    onClick={() => {
                      handleDisconnectRequest("clicked", setConfig);
                    }}
                  >
                    Disconnect
                  </Button>
                ) : (
                  <Button
                    color="secondary"
                    variant="contained"
                    aria-label="connect"
                    fullWidth={true}
                    onClick={() => {
                      handleConnectRequest("clicked", setConfig);
                    }}
                  >
                    Connect Device
                  </Button>
                )}
              </div>
            </Grid>
          </Grid>
        </CardContent>
      </Card>
    </div>
  );
};

export default Status;
