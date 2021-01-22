import React, { useState, useEffect } from "react";
import axios from "axios";
import { Typography } from "@material-ui/core";
import { Grid } from "@material-ui/core";

function mapdata(data) {
  console.log(data);
  data.streaming = data.streaming ? "Yes" : "No";
  data.column_location =
    "column_location" in data
      ? Object.keys(data.column_location).sort().join(", ")
      : [];
  return data;
}

const Configure = () => {
  let [config, setConfig] = useState([]);

  useEffect(() => {
    axios
      .get(`${process.env.REACT_APP_API_URL}config`)
      .then((res) => setConfig(mapdata(res.data)));
  }, []);

  return (
    <Grid xs={12}>
      <Grid>
        <Typography color="primary"> Configured Mode: </Typography>
        <Typography>{config.mode}</Typography>
        <Typography color="primary">Streaming: </Typography>
        <Typography>{config.streaming}</Typography>
        <Typography color="primary">Sensors: </Typography>
        <Typography>{config.source}</Typography>
      </Grid>
      {config.mode === "streaming" ? (
        <Grid>
          <Typography color="primary">Sample Rate: </Typography>
          <Typography>{config.sample_rate}</Typography>
          <Typography color="primary">Columns:</Typography>
          <Typography>{config.column_location}</Typography>
        </Grid>
      ) : (
        <></>
      )}
    </Grid>
  );
};

export default Configure;
