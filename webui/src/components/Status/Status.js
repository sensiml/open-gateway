import { Grid } from "@material-ui/core";
import { makeStyles, useTheme } from "@material-ui/core/styles";
import React from "react";
import { SimpleCard } from "../SimpleCard";

const Status = (props) => {
  return (
    <Grid container rows spacing={4}>
      <Grid item xs={12} container rows spacing={2}>
        <SimpleCard name="Mode" xs="6" value={props.config.mode}></SimpleCard>
        <SimpleCard
          name="Source"
          xs="6"
          value={props.config.source}
        ></SimpleCard>
      </Grid>
      <Grid item xs={12} container rows spacing={2}>
        <SimpleCard
          name="Device ID"
          xs={6}
          value={props.config.device_id}
        ></SimpleCard>
        {props.config.mode === "data_capture" ? (
          <SimpleCard
            xs="6"
            name="Sample Rate"
            value={props.config.sample_rate}
          ></SimpleCard>
        ) : null}
      </Grid>
      <Grid item xs={12}>
        {props.config.mode === "data_capture" ? (
          <SimpleCard
            name="Sensor Columns"
            value={props.config.column_location}
            list={true}
          ></SimpleCard>
        ) : null}
      </Grid>
    </Grid>
  );
};

export default Status;
