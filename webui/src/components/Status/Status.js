import { CardContent, Grid, Typography } from "@material-ui/core";
import Button from "@material-ui/core/Button";
import Card from "@material-ui/core/Card";
import { makeStyles, useTheme } from "@material-ui/core/styles";
import axios from "axios";
import React, { useEffect, useState } from "react";
import { SimpleCard } from "../SimpleCard";

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
  },

  section1: {
    margin: theme.spacing(3, 2),
  },
}));

const Status = (props) => {
  const classes = useStyles();
  const theme = useTheme();

  return (
    <div class={classes.root}>
      <Grid container columns spacing={4}>
        <Grid item xs={12} container rows spacing={2}>
          <div className={classes.section1}>
            <Typography component="h3" variant="h3" color="secondary">
              Device Source
            </Typography>
          </div>
        </Grid>
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
    </div>
  );
};

export default Status;
