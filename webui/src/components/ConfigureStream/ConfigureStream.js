import React, { useState, useEffect } from "react";
import { makeStyles } from "@material-ui/core/styles";
import axios from "axios";
import { Typography } from "@material-ui/core";
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
import Switch from "@material-ui/core/Switch";
import { withStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
  formControl: {
    margin: theme.spacing(3),
  },
  button: {
    margin: theme.spacing(1, 1, 0, 0),
  },
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
}));

const ConfigureStream = () => {
  const classes = useStyles();
  const [source, setSource] = React.useState("Serial");
  const [modeUrl, setModeUrl] = React.useState("config");
  const [deviceID, setDeviceID] = React.useState("");
  const [error, setError] = React.useState(false);
  const [helperText, setHelperText] = React.useState("");
  const [deviceRows, setDeviceRows] = React.useState([]);
  const [deviceColumns, setDeviceColumns] = React.useState([
    { field: "id", headerName: "ID", width: 120 },
    { field: "device_id", headerName: "Device ID", width: 240 },
    { field: "name", headerName: "Name", width: 240 },
  ]);

  const handleRadioChange = (event) => {
    setSource(event.target.value);
  };

  const handleSwitchChange = (event) => {
    console.log("HEREREER");
    console.log(event.target.checked);
    if (event.target.checked) {
      setModeUrl("config-results");
    } else {
      setModeUrl("config");
    }
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
    console.log(source);
    console.log(deviceID);
    axios
      .post(`${process.env.REACT_APP_API_URL}` + modeUrl, {
        device_id: deviceID,
        source: source.toLowerCase(),
      })
      .then((response) => {
        console.log(response.data);
        setHelperText("Configured Device");
      })
      .catch(function (error) {
        if (error.response) {
          // Request made and server responded
          setHelperText(error.response.data.error.message[0]);
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

  const handleDeviceScan = () => {
    axios
      .post(`${process.env.REACT_APP_API_URL}scan`, {
        device_id: deviceID,
        source: source.toLowerCase(),
      })
      .then((response) => {
        console.log(response.data);
        setDeviceRows(response.data);
      });
  };

  // "Configure the gateway to  use a Serial Connection to  connect to the remote  node." />
  // "Configure the gateway to  use a BLE Connection to connect to remote node."
  // "Configure the gateway to mock a node sending test data."
  return (
    <Grid xs={12} container direction="columns">
      <Grid xs={4}>
        <form onSubmit={handleSubmit}>
          <FormControl
            component="fieldset"
            error={error}
            className={classes.formControl}
          >
            <FormLabel component="legend">Source:</FormLabel>
            <RadioGroup
              aria-label="source"
              name="source"
              value={source}
              onChange={handleRadioChange}
            >
              <FormControlLabel
                value="Serial"
                control={<Radio />}
                label="Serial"
              />
              <FormControlLabel value="BLE" control={<Radio />} label="BLE" />
              <FormControlLabel value="Test" control={<Radio />} label="Test" />
            </RadioGroup>
            <Typography component="div">
              <FormLabel component="legend">Mode:</FormLabel>
              <Grid component="label" container alignItems="center" spacing={1}>
                <Grid item>Sensor Data</Grid>
                <Grid item>
                  <Switch name="checkedC" onChange={handleSwitchChange} />
                </Grid>
                <Grid item>KP Results</Grid>
              </Grid>
            </Typography>
            <FormLabel component="legend">Device ID:</FormLabel>
            <TextField
              id="outlined-basic"
              variant="outlined"
              value={deviceID}
              onChange={handleDeviceIDChange}
            />
            <Button
              type="submit"
              variant="outlined"
              color="primary"
              className={classes.button}
            >
              Configure
            </Button>
            <FormHelperText>{helperText}</FormHelperText>
          </FormControl>
        </form>
      </Grid>
      <Grid xs={8}>
        <Button
          type="submit"
          variant="outlined"
          color="primary"
          className={classes.button}
          onClick={() => {
            handleDeviceScan("clicked", { source });
          }}
        >
          Scan
        </Button>
        <DataGrid
          rows={deviceRows}
          columns={deviceColumns}
          onRowSelected={handleRowSelection}
        />
      </Grid>
    </Grid>
  );
};

export default ConfigureStream;
