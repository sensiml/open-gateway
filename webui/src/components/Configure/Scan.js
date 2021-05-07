import React, { useEffect, useState } from "react";
import Button from "@material-ui/core/Button";
import Dialog from "@material-ui/core/Dialog";
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";
import DialogTitle from "@material-ui/core/DialogTitle";
import FormControl from "@material-ui/core/FormControl";
import FormHelperText from "@material-ui/core/FormHelperText";
import { DataGrid } from "@material-ui/data-grid";
import axios from "axios";
import { makeStyles } from "@material-ui/core/styles";
import { DialogContentText } from "@material-ui/core";

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
  section1: {
    margin: theme.spacing(1, 1),
  },
}));

export default function AlertDialog(props) {
  const [open, setOpen] = React.useState(false);
  const [scanning, setIsScanning] = React.useState(false);
  const [deviceRows, setDeviceRows] = React.useState([]);
  const [scanHelperText, setScanHelperText] = React.useState("");
  const [error, setError] = React.useState(false);
  const classes = useStyles();
  const [scanningText, setScanningText] = React.useState("Scanning");

  let deviceColumns = [
    { field: "id", headerName: "ID", width: 0 },
    { field: "device_id", headerName: "Device ID", width: 240 },
    { field: "name", headerName: "Name", width: 240 },
  ];

  const handleClickOpen = (event) => {
    setDeviceRows([]);
    setOpen(true);
    event.preventDefault();
    handleDeviceScan();
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleDeviceScan = () => {
    setScanningText("Scanning for " + props.source + " Devices....");
    setIsScanning(true);
    axios
      .post(`${process.env.REACT_APP_API_URL}scan`, {
        source: props.source.toLowerCase(),
      })
      .then((response) => {
        console.log(response.data);
        setIsScanning(false);
        setDeviceRows(response.data);
        setScanningText("Scanning complete");
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
      <Button
        variant="outlined"
        color="primary"
        disabled={props.configuring}
        fullWidth={true}
        onClick={handleClickOpen}
        className={classes.button}
      >
        Scan for {props.source} Devices
      </Button>
      <Dialog open={open} onClose={handleClose} fullWidth="sm" maxWidth="sm">
        <DialogContent>
          <DialogContentText>{scanningText}</DialogContentText>

          <div style={{ height: 600, width: "100%" }}>
            <DataGrid
              rows={deviceRows}
              columns={deviceColumns}
              onRowSelected={props.handleRowSelection}
              pageSize={10}
            />
          </div>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose} color="primary" autoFocus>
            select
          </Button>
        </DialogActions>
      </Dialog>
    </div>
  );
}
