import React from "react";
import { Header, NavBar } from "../Layout";
import useStyles from "./MainStyles";
import { Grid } from "@material-ui/core";
import { Configure } from "../Configure";
import { ConfigureStream } from "../ConfigureStream";
import { SensorStream } from "../SensorStream";
import { Results } from "../Results";
import CssBaseline from "@material-ui/core/CssBaseline";

const Main = () => {
  const [activeView, setActiveView] = React.useState(0);
  const [streamingMode, setStreamingMode] = React.useState(0);
  const [streamingSource, setStreamingSource] = React.useState(0);
  const [columns, setColumns] = React.useState([]);
  const [deviceID, setDeviceID] = React.useState([]);

  function handleChange(newValue) {
    if (activeView != newValue) {
      setActiveView(newValue);
    }
  }

  const classes = useStyles();
  return (
    <div className={classes.root}>
      <CssBaseline />
      <Grid container direction="column" justify="center" alignItems="center">
        <Header />
        <NavBar onChange={handleChange} />
        <main className={classes.content}>
          {activeView === 0 ? (
            <Configure
              setStreamingMode={setStreamingMode}
              setColumns={setColumns}
              setStreamingSource={setStreamingSource}
              setDeviceID={setDeviceID}
            />
          ) : null}
          {activeView === 1 ? (
            <ConfigureStream
              setStreamingMode={setStreamingMode}
              streamingSource={streamingSource}
              streamingMode={streamingMode}
              deviceID={deviceID}
            />
          ) : null}
          {activeView === 2 ? (
            streamingMode == "results" ? (
              <Results />
            ) : (
                <SensorStream
                  columns={columns}
                />
              )
          ) : null}
        </main>
      </Grid>
    </div>
  );
};

export default Main;
