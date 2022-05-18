import React, { useState } from "react";
import { Grid, Box, Paper } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import { SensorStream } from "../SensorStream";
import { Results } from "../Results";
import { Record } from "../Record";

import { useSelector } from "react-redux";
import { selectClassImage } from "../../redux/selectors/classes";

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

  classImageWrapper: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    padding: "1rem",
    marginBottom: "1rem",
    minHeight: "450px",
  },

  classImage: {
    width: "90%",
  },

  section1: {
    margin: theme.spacing(3, 2),
  },
}));

const TestMode = (props) => {
  const classes = useStyles();
  const [currentClass, setCurrentClass] = useState("");
  const classImage = useSelector(selectClassImage(currentClass));

  const handleLastValue = (value) => {
    setCurrentClass(value || "");
  };

  return (
    <Grid container rows spacing={6}>
      {props.streamingMode !== "recognition" ? (
        <>
          <Grid item lg={8} md={12}>
            <SensorStream
              columns={props.columns}
              isConnected={props.isConnected}
              dataType={props.dataType}
            />
          </Grid>
          <Grid item md={12} lg={4}>
            <Record
              isCameraConnected={props.isCameraConnected}
              isRecording={props.isRecording}
            />
          </Grid>
        </>
      ) : (
        <>
          <Grid item md={12} lg={6}>
            <Results setLastValue={handleLastValue} />
          </Grid>
          <Grid item md={12} lg={6}>
            <Paper className={classes.imageWrapperCard}>
              <Box className={classes.classImageWrapper}>
                {classImage ? (
                  <img
                    className={classes.classImage}
                    src={classImage}
                    alt={currentClass}
                  />
                ) : currentClass ? (
                  `No Image for ${currentClass}`
                ) : (
                  ""
                )}
              </Box>
            </Paper>

            <Record
              isCameraConnected={props.isCameraConnected}
              isRecording={props.isRecording}
            />
          </Grid>
        </>
      )}
    </Grid>
  );
};

export default TestMode;
