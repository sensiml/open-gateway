import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Stepper from "@material-ui/core/Stepper";
import Step from "@material-ui/core/Step";
import StepLabel from "@material-ui/core/StepLabel";
import Button from "@material-ui/core/Button";
import Typography from "@material-ui/core/Typography";

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
    "Scan and Select Device ID",
    "Select Mode",
    "Click Configure Gateway",
  ];
}

function getStepContent(stepIndex) {
  switch (stepIndex) {
    case 0:
      return "Select Connection Type";
    case 1:
      return "Scan and Select Device ID";
    case 2:
      return "Select Device Mode";
    case 3:
      return "Click Configure Gateway";
    default:
      return "";
  }
}

const HorizontalLabelPositionBelowStepper = (props) => {
  const classes = useStyles();
  const [activeStep, setActiveStep] = React.useState();
  const steps = getSteps();

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
