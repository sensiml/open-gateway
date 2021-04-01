import {
  Button,
  Card,
  CardContent,
  Grid,
  Typography,
  Tooltip,
} from "@material-ui/core";
import Divider from "@material-ui/core/Divider";
import { useTheme } from "@material-ui/core/styles";
import TextField from "@material-ui/core/TextField";
import axios from "axios";
import React from "react";
import { makeStyles } from "@material-ui/core/styles";

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

const Record = (props) => {
  const classes = useStyles();
  const theme = useTheme();
  const [recording, setRecording] = React.useState(props.isRecording);
  const [filename, setFilename] = React.useState("filename");
  const [recordDistabled, setRecordDistabled] = React.useState(false);
  console.log("Connected Camera");
  console.log(props.isCameraConnected);

  const handleRecordRequest = (event, url, setRecording, filename) => {
    setRecordDistabled(true);
    console.log(event);

    if (filename === "") {
      filename = "test";
    }
    console.log(filename);
    axios
      .post(`${process.env.REACT_APP_API_URL}` + url, {
        filename: filename,
        event_type: event,
      })
      .then((response) => {
        console.log(response.data);
        if (event == "record-start") {
          setRecording(true);
          console.log(event);
        }
        if (event == "record-stop") {
          setRecording(false);
          console.log(event);
        }
        setRecordDistabled(false);
      })
      .catch((error) => {
        console.log(error);
        setRecordDistabled(false);
      });
  };

  const handleDownloadRequest = (event, filename) => {
    console.log(`${process.env.REACT_APP_API_URL}download/` + filename);
    fetch(`${process.env.REACT_APP_API_URL}download/` + filename, {
      method: "GET",
      headers: { "Content-Type": "application/zip" },
    })
      .then((response) => response.blob())
      .then((blob) => {
        // Create blob link to download
        const url = window.URL.createObjectURL(new Blob([blob]));
        const link = document.createElement("a");
        link.href = url;
        link.setAttribute("download", filename + ".zip");

        // Append to html link element page
        document.body.appendChild(link);

        // Start download
        link.click();

        // Clean up and remove the link
        link.parentNode.removeChild(link);
      });
  };
  const handleFileNameChange = (event) => {
    setFilename(event.target.value);
  };

  return (
    <Card>
      <CardContent>
        <div className={classes.section1}>
          <Typography component="h4" variant="h4" color="secondary">
            Record to Gateway
          </Typography>
        </div>
        <Divider variant="middle" />
        <div className={classes.section2}>
          <Typography variant="subtitle1" color="textSecondary"></Typography>
        </div>

        <Grid container columns spacing={6}>
          <Grid item xs={12}>
            <TextField
              id="outlined-basic"
              variant="outlined"
              value={filename}
              onChange={handleFileNameChange}
              fullWidth={true}
              disabled={recording}
            />
          </Grid>
          <Grid item xs={6}>
            {recording === false ? (
              <Tooltip
                title="This will record the device sensor data in .csv format to the gateway.
                  If video source is connected, the video source will also be recorded.
                  "
                aria-label="record"
              >
                <Button
                  aria-label="Record"
                  variant="contained"
                  fullWidth={true}
                  disabled={recordDistabled}
                  onClick={() => {
                    handleRecordRequest(
                      "record-start",
                      props.isCameraConnected ? "record" : "record-device",
                      setRecording,
                      filename
                    );
                  }}
                >
                  Record
                </Button>
              </Tooltip>
            ) : (
              <Button
                aria-label="Stop "
                variant="contained"
                fullWidth={true}
                disabled={recordDistabled}
                onClick={() => {
                  handleRecordRequest(
                    "record-stop",
                    props.isCameraConnected ? "record" : "record-device",
                    setRecording
                  );
                }}
              >
                Stop Recording
              </Button>
            )}
          </Grid>

          <Grid item xs={6}>
            <Tooltip
              title="Download the recorded .csv and .mp4 for this capture from the gateway. A .dcli file will also be generated describing the data.
                  "
              aria-label="record"
            >
              <Button
                aria-label="Download "
                variant="contained"
                fullWidth={true}
                disabled={recordDistabled}
                onClick={() => {
                  handleDownloadRequest("download", filename);
                }}
              >
                Download
              </Button>
            </Tooltip>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};

export default Record;
