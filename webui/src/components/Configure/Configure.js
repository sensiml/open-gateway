import { Grid } from "@material-ui/core";
import Button from "@material-ui/core/Button";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import FormControl from "@material-ui/core/FormControl";
import FormControlLabel from "@material-ui/core/FormControlLabel";
import FormHelperText from "@material-ui/core/FormHelperText";
import FormLabel from "@material-ui/core/FormLabel";
import Radio from "@material-ui/core/Radio";
import RadioGroup from "@material-ui/core/RadioGroup";
import { makeStyles } from "@material-ui/core/styles";
import TextField from "@material-ui/core/TextField";
import { DataGrid } from "@material-ui/data-grid";
import axios from "axios";
import React from "react";
import HorizontalLabelPositionBelowStepper from "./Stepper";

const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
  },
  formControl: {
    margin: theme.spacing(3),
    minWidth: 600,
  },
  button: {
    margin: theme.spacing(1, 1, 0, 0),
  },
}));

const Configure = (props) => {
  const classes = useStyles();
  const [source, setSource] = React.useState(props.streamingSource);
  const [mode, setMode] = React.useState(
    props.streamingMode === "recognition" ? "RECOGNITION" : "DATA_CAPTURE"
  );
  const [deviceID, setDeviceID] = React.useState(props.deviceID);
  const [error, setError] = React.useState(false);
  const [scanHelperText, setScanHelperText] = React.useState("");
  const [helperText, setHelperText] = React.useState("");
  const [deviceRows, setDeviceRows] = React.useState([]);
  const [configuring, setIsConfiguring] = React.useState(false);
  const [scanning, setIsScanning] = React.useState(false);
  let deviceColumns = [
    { field: "id", headerName: "ID", width: 0 },
    { field: "device_id", headerName: "Device ID", width: 240 },
    { field: "name", headerName: "Name", width: 240 },
  ];

  const handleRadioChange = (event) => {
    console.log("handle radio");
    setSource(event.target.value);
  };

  const handleModeChange = (event) => {
    console.log("handle mode");
    setMode(event.target.value);
  };

  const handleDeviceIDChange = (event) => {
    console.log("handle device id");
    setDeviceID(event.target.value);
    setHelperText(" ");
    setError(false);
  };

  const handleRowSelection = (event) => {
    console.log(event.data.device_id);
    setDeviceID(event.data.device_id);
  };

  const handleSubmit = (event) => {
    setIsConfiguring(true);
    event.preventDefault();
    if (deviceID === "") {
      setHelperText("Must Set DeviceID");
      setIsConfiguring(false);
      return;
    }
    console.log(source);
    console.log(deviceID);
    axios
      .post(`${process.env.REACT_APP_API_URL}config`, {
        device_id: deviceID,
        source: source.toLowerCase(),
        mode: mode,
      })
      .then((response) => {
        console.log(response.data);
        console.log(props);
        props.setStreamingMode(response.data.mode);
        props.setIsConnected(true);
        setHelperText("Gateway Connected to device, now ready to stream.");
        setIsConfiguring(false);
      })
      .catch(function (error) {
        setIsConfiguring(false);
        if (error.response) {
          setHelperText(error.response.data.detail.join(", "));
          console.log(error.response.data);
          console.log(error.response.status);
          console.log(error.response.headers);
        } else if (error.request) {
          // The request was made but no response was received
          console.log(error.request);
        } else {
          // Something happened in setting up the request that triggered an Error
          console.log("Error", error.detail);
        }
      });
  };

  const handleDeviceScan = (event) => {
    console.log(event);
    setIsScanning(true);
    event.preventDefault();
    axios
      .post(`${process.env.REACT_APP_API_URL}scan`, {
        source: source.toLowerCase(),
      })
      .then((response) => {
        console.log(response.data);
        setIsScanning(false);
        setDeviceRows(response.data);
      })
      .catch(function (error) {
        setIsScanning(false);
        if (error.response) {

          // Request made and server responded
          setScanHelperText(error.response.data.detail.join(", "));
          console.log(error.response.data);
          console.log(error.response.status);
          console.log(error.response.headers);
        } else if (error.request) {
          // The request was made but no response was received
          console.log(error.request);
        } else {
          // Something happened in setting up the request that triggered an Error
          console.log("Error", error.detail);
        }
      });
  };

  return (
    <div>
      
      <Grid container rows spacing={4}>
        <Grid item>
          <Card>
          <HorizontalLabelPositionBelowStepper />
            <CardContent>            
              <form onSubmit={handleSubmit}>
                <FormControl component="fieldset" disabled={configuring} error={error} className={classes.formControl}>
                  <div>
                    <FormLabel>Connection Type</FormLabel>
                    <RadioGroup
                      aria-label="source"
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
                  </div>
                  <div>
                    <FormLabel component="legend">
                      Device Mode:
                            </FormLabel>
                    <RadioGroup
                      aria-label="mode"
                      name="Streaming Source"
                      value={mode}
                      onChange={handleModeChange}
                      row
                    >
                      <FormControlLabel
                        value="DATA_CAPTURE"
                        control={<Radio />}
                        label="Data Capture"
                      />
                      <FormControlLabel
                        value="RECOGNITION"
                        control={<Radio />}
                        label="Recognition"
                      />
                    </RadioGroup>
                  </div>
                  <div>
                    <FormLabel component="legend">Device ID:</FormLabel>
                    <TextField
                      id="outlined-basic"
                      variant="outlined"
                      value={deviceID}
                      onChange={handleDeviceIDChange}
                      fullWidth={true}
                    />
                  </div>
                  <div>
                    <Button
                      type="submit"
                      variant="contained"
                      color="primary"
                      disabled={configuring}
                      fullWidth={true}
                      className={classes.button}
                    >
                      Configure Gateway
                    </Button>
                  </div>
                </FormControl>
              </form>
            </CardContent>
          </Card>
        </Grid>
        <Grid item>
          <Card>
            <CardContent>
              <form onSubmit={handleDeviceScan}>
                <FormControl
                  component="fieldset"
                  error={error}
                  className={classes.formControl}
                >
                  <Button
                    type="submit"
                    variant="contained"
                    color="secondary"
                    fullWidth={true}
                    disabled={scanning}
                  >
                    Scan For {source} Devices
                        </Button>
                  <div style={{ height: 600, width: 600 }}>
                    <DataGrid
                      rows={deviceRows}
                      columns={deviceColumns}
                      onRowSelected={handleRowSelection}
                      pageSize={10}
                    />
                  </div>
                  <FormHelperText>{scanHelperText}</FormHelperText>
                </FormControl>
              </form>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

    </div>
  );
};

export default Configure;
