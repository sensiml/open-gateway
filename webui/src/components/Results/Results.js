import React, { useState, useEffect } from "react";
import axios from "axios";
import { Typography } from "@material-ui/core";
import { Button } from "@material-ui/core";
import { Grid } from "@material-ui/core";
import { makeStyles, useTheme } from "@material-ui/core/styles";
import { DataGrid } from "@material-ui/data-grid";
import ResultsFilter from "./ResultsFilter";
import Slider from "@material-ui/core/Slider";
import Divider from "@material-ui/core/Divider";

var id_counter = 0;

const useStyles = makeStyles((theme) => ({
  controls: {
    display: "flex-right",
    alignItems: "center",
    paddingLeft: theme.spacing(1),
    paddingBottom: theme.spacing(1),
  },
  sliderroot: {
    width: 250,
  },
  sliderinput: {
    width: 42,
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
  const [filterLength, setfilterLength] = React.useState(1);

  const classes = useStyles();
  const theme = useTheme();

  const handleFilterLengthSliderChange = (event, newValue) => {
    console.log(newValue);
    setfilterLength(newValue);
  };

  return (
    <Grid>
      <div className={classes.section1}>
        <Grid container spacing={2} rows>
          <Grid item xs={8}>
            <Typography component="h3" variant="h3" color="secondary">
              Model Result
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
                    `${process.env.REACT_APP_API_URL}results`,
                    props.setDeviceRows
                  );
                }}
              >
                Connect
              </Button>
            </div>
          </Grid>
          <Grid item>
            <div className={classes.controls}>
              <Button
                aria-label="disconnect"
                color="secondary"
                variant="contained"
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
        <Grid alignContent="center">
          <ResultsFilter
            data={props.deviceRows}
            filter_length={filterLength}
          ></ResultsFilter>
        </Grid>
      </div>
      <Divider variant="middle" />
      <div className={classes.section1}>
        <Grid container spacing={3} alignItems="center">
          <Grid item> Filter Length </Grid>
          <div className={classes.sliderroot}>
            <Grid item xs>
              <Slider
                value={typeof filterLength === "number" ? filterLength : 1}
                onChange={handleFilterLengthSliderChange}
                aria-labelledby="input-slider"
                min={1}
                max={10}
              />
            </Grid>
          </div>
          <Grid item> {filterLength} </Grid>
        </Grid>
      </div>
      <Divider variant="middle" />

      <div className={classes.section1}>
        <div style={{ height: 600, width: "100%" }}>
          <DataGrid
            rows={props.deviceRows}
            columns={deviceColumns}
            pageSize={15}
            sortModel={[{ field: "id", sort: "desc" }]}
          />
        </div>
      </div>
    </Grid>
  );
};

export default Results;
