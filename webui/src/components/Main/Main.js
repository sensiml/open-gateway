import React from "react";
import { Header, NavBar } from "../Layout";
import useStyles from "./MainStyles";
import { Grid } from "@material-ui/core";
import { Status } from "../Status";
import { Configure } from "../Configure";
import { SensorStream } from "../SensorStream";
import { Results } from "../Results";
import CssBaseline from "@material-ui/core/CssBaseline";

const Main = () => {
  const [activeView, setActiveView] = React.useState(0);
  const [streamingMode, setStreamingMode] = React.useState(0);
  const [streamingSource, setStreamingSource] = React.useState(0);
  const [columns, setColumns] = React.useState([]);
  const [deviceID, setDeviceID] = React.useState([]);
  const [isConnected, setIsConnected] = React.useState(false);

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
        <NavBar onChange={handleChange} isConnected={isConnected} />
        <main className={classes.content}>
          {activeView === 0 ? (
            <Status
              setStreamingMode={setStreamingMode}
              setColumns={setColumns}
              setStreamingSource={setStreamingSource}
              setDeviceID={setDeviceID}
              setIsConnected={setIsConnected}
              isConnected={isConnected}
            />
          ) : null}
          {activeView === 2 ? (
            <Configure
              setStreamingMode={setStreamingMode}
              streamingSource={streamingSource}
              streamingMode={streamingMode}
              deviceID={deviceID}
              setIsConnected={setIsConnected}
            />
          ) : null}
          {activeView === 1 ? (
            streamingMode == "results" ? (
              <Results />
            ) : (
              <SensorStream columns={columns} />
            )
          ) : null}
        </main>
      </Grid>
    </div>
  );
};

export default Main;
