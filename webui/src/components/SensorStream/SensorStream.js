import React, { useState, useEffect } from "react";
import axios from "axios";
import { Typography } from "@material-ui/core";
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

const handleDisconnectRequest = (event) => {
  axios.get(`${process.env.REACT_APP_API_URL}disconnect`).then((response) => {
    console.log(response.data);
  });
};

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

const handleStreamRequest = (event, url, setStreamCallback, columns) => {
  fetch(url, {
    method: "GET",
  }).then((response) => {
    const reader = response.body.getReader();
    const stream = new ReadableStream({
      start(controller) {
        // The following function handles each data chunk
        function push() {
          // "done" is a Boolean and value a "Uint8Array"
          reader.read().then(({ done, value }) => {
            // Is there no more data to read?
            if (done) {
              // Tell the browser that we have finished sending data
              controller.close();
              return;
            }
            var int16Array = new Int16Array(value.buffer);
            setStreamCallback(splitArray(int16Array, columns));
            push();
          });
        }

        push();
      },
    });

    return new Response(stream, { headers: { "Content-Type": "text/html" } });
  });
};

const SensorStream = (props) => {
  const classes = useStyles();
  const theme = useTheme();

  return (
    <div className={classes.details}>
      <div className={classes.section1}>
        <Grid container spacing={2} rows>
          <Grid item xs={8}>
            <Typography component="h3" variant="h3" color="secondary">
              Mode: Data Collection
            </Typography>
          </Grid>

          <Grid item>
            <div className={classes.controls}>
              <Button
                aria-label="disconnect"
                color="primary"
                variant="contained"
                onClick={() => {
                  handleStreamRequest(
                    "clicked",
                    `${process.env.REACT_APP_API_URL}stream`,
                    props.setStreamData,
                    props.columns
                  );
                }}
              >
                Stream
              </Button>
            </div>
          </Grid>
          <Grid item>
            <div className={classes.controls}>
              <Button
                color="secondary"
                variant="contained"
                aria-label="disconnect"
                onClick={() => {
                  handleDisconnectRequest("clicked");
                }}
              >
                Disconnect
              </Button>
            </div>
          </Grid>
        </Grid>
      </div>
      <Divider variant="middle" />
      <div className={classes.section2}>
        <Typography variant="subtitle1" color="textSecondary"></Typography>
      </div>
      <StreamChart data={props.streamData} />
    </div>
  );
};

export default SensorStream;
