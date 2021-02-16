import React, { useState, useEffect } from "react";
import axios from "axios";
import { Card, CardContent, Typography } from "@material-ui/core";
import { Button } from "@material-ui/core";
import StreamChart from "./StreamChart";
import { makeStyles, useTheme } from "@material-ui/core/styles";
import Divider from "@material-ui/core/Divider";
import { Grid } from "@material-ui/core";

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

function splitArray(data, columns) {
  var size = data.length / columns.length;
  var x_array = [...Array(size).keys()];
  var lines = columns.map((x) => {
    return {
      x: x_array,
      y: [],
      name: x,
    };
  });

  for (var i = 0; i < data.length; i += columns.length) {
    for (var col = 0; col < columns.length; col++) {
      lines[col].y.push(data[i + col]);
    }
  }
  return lines;
}

function convertToJson(data, columns, isRecording) {
  if (!isRecording) {
    {
      return;
    }
  }

  console.log("Columns", columns);
  var lines = {};
  for (col in columns) {
    lines[columns[col]] = [];
  }

  for (var k = 0; k < data.length; k++) {
    for (var i = 0; i < data[k].length; i += columns.length) {
      for (var col = 0; col < columns.length; col++) {
        lines[columns[col]].push(data[k][i + col]);
      }
    }
  }

  return lines;
}

function handleRecord(event, setIsRecording, setRecordBuffer) {
  console.log("set recording true");
  var int16Array = new Int16Array();
  setRecordBuffer(int16Array);
  setIsRecording(true);
}

function handleStopStreaming(event, reader, setIsStreaming, setIsRecording) {
  //debugger;
  console.log(reader);
  reader.cancel();
  setIsStreaming(false);
  setIsRecording(false);
}

const getReader = (
  event,
  url,
  setStreamCallback,
  setIsStreaming,
  setRecordBufferCallback,
  columns,
  setReader
) => {
  return fetch(url, {
    method: "GET",
  }).then((response) => {
    const reader = response.body.getReader();
    setReader(reader);
    const stream = new ReadableStream({
      start(controller) {
        // The following function handles each data chunk

        function push() {
          // "done" is a Boolean and value a "Uint8Array"
          reader.read().then(({ done, value }) => {
            // Is there no more data to read?
            if (done) {
              // Tell the browser that we have finished sending data
              setIsStreaming(false);
              controller.close();
              return;
            }

            var int16Array = new Int16Array(value.buffer);
            setStreamCallback(splitArray(int16Array, columns));
            //setRecordBufferCallback((x) => [...x, int16Array]);

            push();
          });
        }
        push();
      },
    });
  });
};

const SensorStream = (props) => {
  const classes = useStyles();
  const theme = useTheme();
  const [streamData, setStreamData] = React.useState([]);
  const [isStreaming, setIsStreaming] = React.useState(false);
  const [isRecording, setIsRecording] = React.useState(false);
  const [recordBuffer, setRecordBuffer] = React.useState([]);
  const [reader, setReader] = React.useState();

  const handleStreamRequest = (event, url) => {
    setIsStreaming(true);

    getReader(
      event,
      url,
      setStreamData,
      setIsStreaming,
      setRecordBuffer,
      props.columns,
      setReader
    );
  };

  function handleStopRecord(event) {
    event.preventDefault();
    // Prepare the file
    let output = JSON.stringify(
      convertToJson(recordBuffer, props.columns, isRecording),
      //{ test: "test" },
      null,
      4
    );
    var blob1 = new Blob([output], { type: "text/plain;charset=utf-8" });

    //Check the Browser.
    var isIE = false || !!document.documentMode;
    if (isIE) {
      window.navigator.msSaveBlob(blob1, "Customers.txt");
    } else {
      var url = window.URL || window.webkitURL;
      var link = url.createObjectURL(blob1);
      var a = document.createElement("a");
      a.download = "data.txt";
      a.href = link;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    }
    setIsRecording(false);
    var int16Array = new Int16Array();
    setRecordBuffer(int16Array);
  }

  return (
    <div className={classes.root}>
      <Card>
        <CardContent>
          <div className={classes.section1}>
            <Grid container spacing={2} rows>
              <Typography component="h3" variant="h3" color="secondary">
                Mode: Data Collection
              </Typography>
            </Grid>
          </div>
          <Divider variant="middle" />
          <div className={classes.section2}>
            <Typography variant="subtitle1" color="textSecondary"></Typography>
          </div>
          <StreamChart data={streamData} />

          <Grid container rows>
            <Grid item>
              <div className={classes.controls}>
                <Button
                  aria-label="disconnect"
                  color="primary"
                  variant="contained"
                  disabled={isStreaming}
                  onClick={() => {
                    handleStreamRequest(
                      "clicked",
                      `${process.env.REACT_APP_API_URL}stream`
                    );
                  }}
                >
                  Start Stream
                </Button>
              </div>
            </Grid>
            <Grid item>
              <div className={classes.controls}>
                <Button
                  aria-label="disconnect"
                  color="primary"
                  variant="contained"
                  disabled={!isStreaming}
                  onClick={() => {
                    handleStopStreaming(
                      "stopstreaming",
                      reader,
                      setIsStreaming,
                      setIsRecording
                    );
                  }}
                >
                  Stop Stream
                </Button>
              </div>
            </Grid>
          </Grid>
        </CardContent>
      </Card>
    </div>
  );
};

export default SensorStream;

/*

            <Grid item>
              <div className={classes.controls}>
                <Button
                  aria-label="disconnect"
                  color="primary"
                  variant="contained"
                  disabled={isStreaming ? (isRecording ? true : false) : true}
                  onClick={() => {
                    handleRecord("record", setIsRecording, setRecordBuffer);
                  }}
                >
                  Start Record
                </Button>
              </div>
            </Grid>
            <Grid item>
              <div className={classes.controls}>
                <Button
                  aria-label="disconnect"
                  color="primary"
                  variant="contained"
                  disabled={isStreaming ? (isRecording ? false : true) : true}
                  onClick={(e) => {
                    handleStopRecord(e);
                  }}
                >
                  Stop Record
                </Button>
              </div>
            </Grid>
*/
