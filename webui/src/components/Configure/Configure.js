import React, { useState, useEffect } from "react";
import { makeStyles } from "@material-ui/core/styles";
import axios from "axios";
import { Grid } from "@material-ui/core";
import Radio from "@material-ui/core/Radio";
import RadioGroup from "@material-ui/core/RadioGroup";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import FormControl from "@material-ui/core/FormControl";
import FormHelperText from "@material-ui/core/FormHelperText";
import FormLabel from "@material-ui/core/FormLabel";
import Button from "@material-ui/core/Button";
import TextField from "@material-ui/core/TextField";
import { DataGrid } from "@material-ui/data-grid";
import HorizontalLabelPositionBelowStepper from "./Stepper";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";

const useStyles = makeStyles((theme) => ({
  formControl: {
    margin: theme.spacing(3),
  },
  root: {
    display: "flex",
  },
}));

const Configure = (props) => {
  const classes = useStyles();
  const [source, setSource] = React.useState(props.streamingSource);
  const [modeUrl, setModeUrl] = React.useState(
    props.streamingMode === "results" ? "config-results" : "config"
  );
  const [deviceID, setDeviceID] = React.useState(props.deviceID);
  const [error, setError] = React.useState(false);
  const [scanHelperText, setScanHelperText] = React.useState("");
  const [helperText, setHelperText] = React.useState("");
  const [deviceRows, setDeviceRows] = React.useState([]);
  const [deviceColumns, setDeviceColumns] = React.useState([
    { field: "id", headerName: "ID", width: 0 },
    { field: "device_id", headerName: "Device ID", width: 240 },
    { field: "name", headerName: "Name", width: 240 },
  ]);

  const handleRadioChange = (event) => {
    setSource(event.target.value);
  };

  const handleModeChange = (event) => {
    setModeUrl(event.target.value);
  };

  const handleDeviceIDChange = (event) => {
    setDeviceID(event.target.value);
    setHelperText(" ");
    setError(false);
  };

  const handleRowSelection = (event) => {
    console.log(event.data.device_id);
    setDeviceID(event.data.device_id);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if (deviceID === "") {
      setHelperText("Must Set DeviceID");
      return;
    }
    console.log(source);
    console.log(deviceID);
    axios
      .post(`${process.env.REACT_APP_API_URL}` + modeUrl, {
        device_id: deviceID,
        source: source.toLowerCase(),
      })
      .then((response) => {
        console.log(response.data);
        console.log(props);
        props.setStreamingMode(response.data.mode);
        setHelperText("Configured Device");
      })
      .catch(function (error) {
        if (error.response) {
          // Request made and server responded
          setHelperText(error.response.data.error.message.join(", "));
          console.log(error.response.data);
          console.log(error.response.status);
          console.log(error.response.headers);
        } else if (error.request) {
          // The request was made but no response was received
          console.log(error.request);
        } else {
          // Something happened in setting up the request that triggered an Error
          console.log("Error", error.message);
        }
      });
  };

  const handleDeviceScan = (event) => {
    console.log(event);
    event.preventDefault();
    axios
      .post(`${process.env.REACT_APP_API_URL}scan`, {
        source: source.toLowerCase(),
      })
      .then((response) => {
        console.log(response.data);
        setDeviceRows(response.data);
      })
      .catch(function (error) {
        if (error.response) {
          // Request made and server responded
          setScanHelperText(error.response.data.error.message.join(", "));
          console.log(error.response.data);
          console.log(error.response.status);
          console.log(error.response.headers);
        } else if (error.request) {
          // The request was made but no response was received
          console.log(error.request);
        } else {
          // Something happened in setting up the request that triggered an Error
          console.log("Error", error.message);
        }
      });
  };

  // "Configure the gateway to  use a Serial Connection to  connect to the remote  node." />
  // "Configure the gateway to  use a BLE Connection to connect to remote node."
  // "Configure the gateway to mock a node sending test data."
  return (
    <Card>
      <CardContent>
        <Grid xs={12} container rows>
          <HorizontalLabelPositionBelowStepper />
          <Grid item xs={12}>
            <form onSubmit={handleDeviceScan}>
              <FormControl
                component="fieldset"
                error={error}
                className={classes.formControl}
              >
                <FormLabel>Select Source</FormLabel>
                <RadioGroup
                  aria-label="source"
                  name="source"
                  value={source}
                  onChange={handleRadioChange}
                  row
                >
                  <FormControlLabel
                    value="SERIAL"
                    control={<Radio />}
                    label="Serial"
                  />
                  <FormControlLabel
                    value="BLE"
                    control={<Radio />}
                    label="BLE"
                  />
                  <FormControlLabel
                    value="TCPIP"
                    control={<Radio />}
                    label="TCP/IP"
                  />
                  <FormControlLabel
                    value="TEST"
                    control={<Radio />}
                    label="Test"
                  />
                </RadioGroup>

                <Grid item>
                  <Button
                    type="submit"
                    variant="contained"
                    color="secondary"
                    fullWidth={true}
                  >
                    Scan Devices
                  </Button>
                </Grid>
                <FormHelperText>{scanHelperText}</FormHelperText>
              </FormControl>
            </form>
            <div style={{ height: 350, width: "100%" }}>
              <DataGrid
                rows={deviceRows}
                columns={deviceColumns}
                onRowSelected={handleRowSelection}
                pageSize={4}
              />
            </div>
          </Grid>
          <Grid item xs={12}>
            <form onSubmit={handleSubmit}>
              <FormControl
                component="fieldset"
                error={error}
                className={classes.formControl}
              >
                <Grid item>
                  <FormLabel component="legend">Mode:</FormLabel>
                  <RadioGroup
                    aria-label="mode"
                    name="Streaming Source"
                    value={modeUrl}
                    onChange={handleModeChange}
                    row
                  >
                    <FormControlLabel
                      value="config"
                      control={<Radio />}
                      label="Data Collection"
                    />
                    <FormControlLabel
                      value="config-results"
                      control={<Radio />}
                      label="Recognition"
                    />
                  </RadioGroup>
                  <FormLabel component="legend">Device ID:</FormLabel>
                  <TextField
                    id="outlined-basic"
                    variant="outlined"
                    value={deviceID}
                    onChange={handleDeviceIDChange}
                  />
                </Grid>
                <Grid item>
                  <Button
                    type="submit"
                    variant="contained"
                    color="primary"
                    fullWidth={true}
                  >
                    Configure
                  </Button>
                </Grid>
                <FormHelperText>{helperText}</FormHelperText>
              </FormControl>
            </form>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};

export default Configure;
