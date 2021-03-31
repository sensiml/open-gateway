import { CardContent, Grid, Typography } from "@material-ui/core";
import Button from "@material-ui/core/Button";
import Card from "@material-ui/core/Card";
import { makeStyles, useTheme } from "@material-ui/core/styles";
import axios from "axios";
import React, { useEffect, useState } from "react";
import { SimpleCard } from "../SimpleCard";
import { WebCamera } from "../WebCamera";

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
  },

  section1: {
    margin: theme.spacing(3, 2),
  },
}));

const Status = (props) => {
  const classes = useStyles();
  const theme = useTheme();
  let [deviceDisabled, setDeviceDisabled] = useState(false);

  const handleDisconnectRequest = (event) => {
    setDeviceDisabled(true);
    axios.get(`${process.env.REACT_APP_API_URL}disconnect`).then((res) => {
      console.log(res.data);
      mapdata(res.data);
      props.setDeviceDisabled(false);
    });
  };

  const handleConnectRequest = (event) => {
    setDeviceDisabled(true);
    axios.get(`${process.env.REACT_APP_API_URL}connect`).then((res) => {
      mapdata(res.data);
      setDeviceDisabled(false);
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
    props.setIsCameraConnected(data.camera_on);
    data.column_location =
      "column_location" in data
        ? Object.keys(data.column_location).sort().join(", ")
        : [];

    props.setConfig(data);
  }
  return (
    <div class={classes.root}>
      <Grid container rows spacing={6}>
        <Grid item xs={6}>
          <Card>
            <CardContent>
              <div className={classes.section1}>
                <Typography component="h3" variant="h3" color="secondary">
                  Device Source
                </Typography>
              </div>
              <Grid container columns spacing={4}>
                <Grid item xs={12} container rows spacing={2}>
                  <SimpleCard
                    name="Mode"
                    xs="6"
                    value={props.config.mode}
                  ></SimpleCard>
                  <SimpleCard
                    name="Source"
                    xs="6"
                    value={props.config.source}
                  ></SimpleCard>
                </Grid>
                <Grid item xs={12} container rows spacing={2}>
                  <SimpleCard
                    name="Device ID"
                    xs={6}
                    value={props.config.device_id}
                  ></SimpleCard>
                  {props.config.mode === "data_capture" ? (
                    <SimpleCard
                      xs="6"
                      name="Sample Rate"
                      value={props.config.sample_rate}
                    ></SimpleCard>
                  ) : null}
                </Grid>
                <Grid item xs={12}>
                  {props.config.mode === "data_capture" ? (
                    <SimpleCard
                      name="Sensor Columns"
                      value={props.config.column_location}
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
                        disabled={deviceDisabled}
                        onClick={() => {
                          handleDisconnectRequest("clicked");
                        }}
                      >
                        Disconnect From Device
                      </Button>
                    ) : (
                      <Button
                        color="secondary"
                        variant="contained"
                        aria-label="connect"
                        fullWidth={true}
                        disabled={deviceDisabled}
                        onClick={() => {
                          handleConnectRequest("clicked");
                        }}
                      >
                        Connect To Device
                      </Button>
                    )}
                  </div>
                </Grid>
              </Grid>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={6}>
          <WebCamera
            setIsCameraConnected={props.setIsCameraConnected}
            isCameraConnected={props.isCameraConnected}
          />
        </Grid>
      </Grid>
    </div>
  );
};

export default Status;
