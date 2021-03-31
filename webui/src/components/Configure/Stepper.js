import Step from "@material-ui/core/Step";
import StepLabel from "@material-ui/core/StepLabel";
import Stepper from "@material-ui/core/Stepper";
import { makeStyles } from "@material-ui/core/styles";
import React from "react";

const useStyles = makeStyles((theme) => ({
  root: {
    width: "100%",
  },
  backButton: {
    marginRight: theme.spacing(1),
  },
  instructions: {
    marginTop: theme.spacing(1),
    marginBottom: theme.spacing(1),
  },
  stepIcon: {
    color: "primary",
  },
}));

function getSteps() {
  return [
    "Select Connection Type",
    "Select Device Mode",
    "Click Scan and Select Device ID",
    "Click Connect to Device",
  ];
}

const HorizontalLabelPositionBelowStepper = (props) => {
  const classes = useStyles();
  const steps = getSteps();

  let activeStep = null;

  return (
    <div className={classes.root}>
      <Stepper activeStep={activeStep} alternativeLabel>
        {steps.map((label) => (
          <Step key={label} color="primary">
            <StepLabel
              active={true}
              StepIconProps={{
                classes: { root: classes.stepIcon },
              }}
            >
              {label}
            </StepLabel>
          </Step>
        ))}
      </Stepper>
    </div>
  );
};

export default HorizontalLabelPositionBelowStepper;
