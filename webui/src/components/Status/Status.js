import { CardContent, Grid, Typography } from "@material-ui/core";
import Button from "@material-ui/core/Button";
import Card from "@material-ui/core/Card";
import { makeStyles, useTheme } from "@material-ui/core/styles";
import axios from "axios";
import React, { useEffect, useState } from "react";
import { SimpleCard } from "../SimpleCard";
import Divider from "@material-ui/core/Divider";

const useStyles = makeStyles((theme) => ({
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
  },
  section1: {
    margin: theme.spacing(2, 0, 2, 0),
  },
}));

const Status = (props) => {
  const classes = useStyles();
  const theme = useTheme();

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
