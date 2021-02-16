import React, { useState, useEffect, useRef } from "react";
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
    width: "100%",
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

function splitArrays(data, columns) {
  var l = 0;
  for (var i = 0; i < data.length; i++) {
    l += data[i].length;
  }
  var size = l / columns.length;
  var x_array = [...Array(size).keys()];
  var lines = columns.map((x) => {
    return {
      x: x_array,
      y: [],
      name: x,
    };
  });

  for (var k = 0; k < data.length; k++) {
    for (var i = 0; i < data[[k]].length; i += columns.length) {
      for (var col = 0; col < columns.length; col++) {
        lines[col].y.push(data[k][i + col]);
      }
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

function convertToCSV(data, columns, isRecording) {
  if (!isRecording) {
    {
      return;
    }
  }

  let csv = "";
  for (col in columns) {
    csv += columns[col] + ",";
  }
  csv += "\n";

  var marker = columns.length - 1;
  for (var k = 0; k < data.length; k++) {
    for (var i = 0; i < data[k].length; i += columns.length) {
      for (var col = 0; col < columns.length; col++) {
        csv += data[k][i + col].toString();
        if (col != marker) {
          csv += ",";
        }
      }
      csv += "\n";
    }
  }

  return csv;
}

function useInterval(callback, delay) {
  const savedCallback = useRef();

  // Remember the latest callback.
  useEffect(() => {
    savedCallback.current = callback;
  }, [callback]);

  // Set up the interval.
  useEffect(() => {
    function tick() {
      savedCallback.current();
    }
    if (delay !== null) {
      let id = setInterval(tick, delay);
      return () => clearInterval(id);
    }
  }, [delay]);
}

function handleRecord(event, setIsRecording, setRecordBuffer) {
  console.log("set recording true");
  var int16Array = new Int16Array();
  setRecordBuffer(int16Array);
  setIsRecording(true);
}

function handleStopStreaming(
  event,
  reader,
  setIsStreaming,
  setIsRecording,
  set
) {
  //debugger;
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
            setStreamCallback((x) => [...x, int16Array]);
            setRecordBufferCallback((x) => [...x, int16Array]);

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
  const [chartData, setChartData] = React.useState([]);
  const [isStreaming, setIsStreaming] = React.useState(false);
  const [isRecording, setIsRecording] = React.useState(false);
  const [recordBuffer, setRecordBuffer] = React.useState([]);
  const [reader, setReader] = React.useState();

  useInterval(() => {
    if (!isRecording) {
      var int16Array = new Int16Array();
      setRecordBuffer(int16Array);
    }
    if (isStreaming) {
      setChartData(splitArrays(streamData, props.columns));
      if (streamData.length > 40) {
        setStreamData(streamData.slice(streamData.length - 40));
      }
    } else {
      setStreamData([]);
    }
  }, 100);

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
    let output = convertToCSV(recordBuffer, props.columns, isRecording);

    /* FOR JSON OUTPUT
    let output = JSON.stringify(
      convertToJson(recordBuffer, props.columns, isRecording),
      //{ test: "test" },
      null,
      4
    );
    */

    var blob1 = new Blob([output], { type: "text/plain;charset=utf-8" });

    //Check the Browser.
    var isIE = false || !!document.documentMode;
    if (isIE) {
      window.navigator.msSaveBlob(blob1, "data.json");
    } else {
      var url = window.URL || window.webkitURL;
      var link = url.createObjectURL(blob1);
      var a = document.createElement("a");
      a.download = "data.json";
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
    <Grid xs={12}>
      <Card>
        <CardContent>
          <div className={classes.section1}>
            <Typography component="h3" variant="h3" color="secondary">
              Test Mode: Data Stream
            </Typography>
          </div>
          <Divider variant="middle" />
          <div className={classes.section2}>
            <Typography variant="subtitle1" color="textSecondary"></Typography>
          </div>
          <StreamChart data={chartData} />

          <Grid container rows spacing={3}>
            {!isStreaming ? (
              <Grid item xs={3}>
                <div className={classes.controls}>
                  <Button
                    aria-label="disconnect"
                    color="primary"
                    variant="contained"
                    fullWidth={true}
                    onClick={() => {
                      handleStreamRequest(
                        "clicked",
                        `${process.env.REACT_APP_API_URL}stream`
                      );
                    }}
                  >
                    Start Streaming
                  </Button>
                </div>
              </Grid>
            ) : (
              <Grid item xs={3}>
                <div className={classes.controls}>
                  <Button
                    aria-label="disconnect"
                    color="secondary"
                    variant="contained"
                    fullWidth={true}
                    onClick={() => {
                      handleStopStreaming(
                        "stopstreaming",
                        reader,
                        setIsStreaming,
                        setIsRecording
                      );
                    }}
                  >
                    Stop Streaming
                  </Button>
                </div>
              </Grid>
            )}
            {!isRecording ? (
              <Grid item xs={3}>
                <div className={classes.controls}>
                  <Button
                    aria-label="disconnect"
                    color="primary"
                    variant="contained"
                    fullWidth={true}
                    disabled={isStreaming ? (isRecording ? true : false) : true}
                    onClick={() => {
                      handleRecord("record", setIsRecording, setRecordBuffer);
                    }}
                  >
                    Begin Record
                  </Button>
                </div>
              </Grid>
            ) : (
              <Grid item xs={3}>
                <div className={classes.controls}>
                  <Button
                    aria-label="disconnect"
                    color="secondary"
                    variant="contained"
                    fullWidth={true}
                    disabled={isStreaming ? (isRecording ? false : true) : true}
                    onClick={(e) => {
                      handleStopRecord(e);
                    }}
                  >
                    Stop Record
                  </Button>
                </div>
              </Grid>
            )}
          </Grid>
        </CardContent>
      </Card>
    </Grid>
  );
};

export default SensorStream;
