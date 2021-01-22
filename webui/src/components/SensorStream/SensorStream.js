import React, { useState, useEffect } from "react";
import axios from "axios";
import { Typography } from "@material-ui/core";
import { Button } from "@material-ui/core";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import StreamChart from "./StreamChart";
import { makeStyles, useTheme } from "@material-ui/core/styles";

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
}));

const handleDisconnectRequest = (event) => {
  axios.get(`${process.env.REACT_APP_API_URL}disconnect`).then((response) => {
    console.log(response.data);
  });
};

const handleStreamRequest = (event, url, setStreamCallback) => {
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
            // Get the data and send it to the browser via the controller
            var int16Array = new Int16Array(value.buffer);
            setStreamCallback([
              {
                x: [...Array(int16Array.length).keys()],
                y: int16Array,
                name: "Line 1",
              },
            ]);
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
    <Card className={classes.root}>
      <div className={classes.details}>
        <CardContent className={classes.content}>
          <Typography component="h5" variant="h5">
            Sensor Data
          </Typography>
          <Typography variant="subtitle1" color="textSecondary"></Typography>
          <StreamChart data={props.streamData} />
          <div className={classes.controls}>
            <Button
              aria-label="disconnect"
              onClick={() => {
                handleStreamRequest(
                  "clicked",
                  `${process.env.REACT_APP_API_URL}stream`,
                  props.setStreamData
                );
              }}
            >
              Stream
            </Button>
            <Button
              aria-label="disconnect"
              onClick={() => {
                handleDisconnectRequest("clicked");
              }}
            >
              Disconnect
            </Button>
          </div>
        </CardContent>
      </div>
    </Card>
  );
};

export default SensorStream;
