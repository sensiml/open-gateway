import { Button, Grid, Typography } from "@material-ui/core";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import Divider from "@material-ui/core/Divider";
import Slider from "@material-ui/core/Slider";
import { makeStyles, useTheme } from "@material-ui/core/styles";
import { DataGrid } from "@material-ui/data-grid";
import React from "react";
import ResultsFilter from "./ResultsFilter";

var id_counter = 0;

const useStyles = makeStyles((theme) => ({
  controls: {
    display: "flex",
    alignItems: "center",
    paddingLeft: theme.spacing(1),
    paddingBottom: theme.spacing(1),
  },
  root: {
    width: "800px",
  },
  sliderroot: {
    width: "100%",
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

function bin2String(array) {
  var results = String.fromCharCode.apply(null, array).split("\n");
  results.pop();

  return results.map((x) => {
    return JSON.parse(x);
  });
}

const handleStreamRequest = (
  event,
  url,
  setStreamCallback,
  setIsStreaming,
  setReader
) => {
  id_counter = 0;
  setStreamCallback([]);
  setIsStreaming(true);
  fetch(url, {
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

function handleStopStreaming(event, reader, setIsStreaming) {
  //debugger;
  console.log(reader);
  reader.cancel();
  setIsStreaming(false);
}

const Results = (props) => {
  const [deviceRows, setDeviceRows] = React.useState([]);
  const [isStreaming, setIsStreaming] = React.useState(false);
  const [reader, setReader] = React.useState();
  let deviceColumns = [
    { field: "id", headerName: "ID", width: 70 },
    { field: "source", headerName: "Device ID", width: 240 },
    { field: "ModelNumber", headerName: "Model ID", width: 240 },
    { field: "Classification", headerName: "Classification", width: 240 },
  ];
  const [filterLength, setfilterLength] = React.useState(1);

  const classes = useStyles();
  const theme = useTheme();

  const handleFilterLengthSliderChange = (event, newValue) => {
    console.log(newValue);
    setfilterLength(newValue);
  };

  return (
    <Card>
      <CardContent>
        <div className={classes.section1}>
          <Grid item xs={12}>
            <Typography
              align="center"
              component="h2"
              variant="h2"
              color="secondary"
            >
              Test Mode: Recognition
            </Typography>
          </Grid>

          <div className={classes.section1}>
            <Divider variant="middle" />
          </div>

          <Grid item xs={12}>
            {isStreaming ? (
              <div className={classes.controls}>
                <Button
                  aria-label="disconnect"
                  color="primary"
                  variant="contained"
                  fullWidth={true}
                  onClick={() => {
                    handleStopStreaming(
                      "stopstreaming",
                      reader,
                      setIsStreaming
                    );
                  }}
                >
                  Stop Stream
                </Button>
              </div>
            ) : (
              <div className={classes.controls}>
                <Button
                  aria-label="disconnect"
                  color="primary"
                  variant="contained"
                  fullWidth={true}
                  onClick={() => {
                    handleStreamRequest(
                      "clicked",
                      `${process.env.REACT_APP_API_URL}results`,
                      setDeviceRows,
                      setIsStreaming,
                      setReader
                    );
                  }}
                >
                  Start Stream
                </Button>
              </div>
            )}
          </Grid>
        </div>

        <Grid item alignContent="center" xs={12}>
          <ResultsFilter
            data={deviceRows}
            filter_length={filterLength}
          ></ResultsFilter>
        </Grid>

        <div className={classes.section1}>
          <Divider variant="middle" />
        </div>

        <Typography align="left" color="primary" component="h5" variant="h5">
          Post Processing
        </Typography>

        <div className={classes.section1}>
          <Divider variant="middle" />
        </div>

        <Grid container spacing={4} rows alignItems="center">
          <Grid item xs={4}>
            <Typography align="center" component="h6" variant="h6">
              Buffer
            </Typography>
          </Grid>

          <Grid item xs={6}>
            <div className={classes.sliderroot}>
              <Slider
                value={typeof filterLength === "number" ? filterLength : 1}
                onChange={handleFilterLengthSliderChange}
                aria-labelledby="input-slider"
                min={1}
                max={10}
              />
            </div>
          </Grid>

          <Grid item xs={1}>
            <Typography align="center" component="h6" variant="h6">
              {filterLength}
            </Typography>
          </Grid>
        </Grid>
        <div className={classes.section1}>
          <div style={{ height: 600, width: "100%" }}>
            <DataGrid
              rows={deviceRows}
              columns={deviceColumns}
              pageSize={15}
              sortModel={[{ field: "id", sort: "desc" }]}
            />
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default Results;
