import React, { useState, useEffect } from "react";
import axios from "axios";
import { Typography } from "@material-ui/core";
import { Button } from "@material-ui/core";
import { Grid } from "@material-ui/core";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import { makeStyles, useTheme } from "@material-ui/core/styles";
import { DataGrid } from "@material-ui/data-grid";

var id_counter = 0;

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

function bin2String(array) {
  var results = String.fromCharCode.apply(null, array).split("\n");
  results.pop();

  return results.map((x) => {
    return JSON.parse(x);
  });
}

const handleStreamRequest = (event, url, setStreamCallback) => {
  id_counter = 0;
  setStreamCallback([]);
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
            var results = bin2String(value);
            for (var i = 0; i < results.length; i++) {
              console.log(results[i]);
              results[i].id = id_counter;
              id_counter += 1;
              setStreamCallback((x) => [...x, results[i]]);
            }

            push();
          });
        }

        push();
      },
    });

    return new Response(stream, { headers: { "Content-Type": "text/html" } });
  });
};

const Results = (props) => {
  const [deviceColumns, setDeviceColumns] = React.useState([
    { field: "id", headerName: "ID", width: 70 },
    { field: "ModelNumber", headerName: "Model ID", width: 240 },
    { field: "Classification", headerName: "Classification", width: 240 },
  ]);

  const classes = useStyles();
  const theme = useTheme();

  return (
    <Grid>
      <div className={classes.details}>
        <Typography component="h5" variant="h5">
          Model Result
        </Typography>
        <Typography variant="subtitle1" color="textSecondary"></Typography>
        <div className={classes.controls}>
          <Button
            aria-label="disconnect"
            onClick={() => {
              handleStreamRequest(
                "clicked",
                `${process.env.REACT_APP_API_URL}results`,
                props.setDeviceRows
              );
            }}
          >
            Connect
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
      </div>
      <div style={{ height: 600, width: "100%" }}>
        <DataGrid
          rows={props.deviceRows}
          columns={deviceColumns}
          pageSize={15}
          sortModel={[{ field: "id", sort: "desc" }]}
        />
      </div>
    </Grid>
  );
};

export default Results;
