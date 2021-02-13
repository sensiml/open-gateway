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
}));

function getSteps() {
  return [
    "Select Connection Type",
    "Scan and Select Device",
    "Select Mode",
    "Configure Gateway",
  ];
}

function getStepContent(stepIndex) {
  switch (stepIndex) {
    case 0:
      return "Scan and select Devicee";
    case 1:
      return "Scan and select Device";
    case 2:
      return "Select Mode";
    case 3:
      return "Configure Gateway";
    default:
      return "";
  }
}

const HorizontalLabelPositionBelowStepper = (props) => {
  const classes = useStyles();
  const [activeStep, setActiveStep] = React.useState(-1);
  const steps = getSteps();

  return (
    <div className={classes.root}>
      <Stepper activeStep={activeStep} alternativeLabel>
        {steps.map((label) => (
          <Step key={label} color="primary">
            <StepLabel>{label}</StepLabel>
          </Step>
        ))}
      </Stepper>
      <div>
        <Typography className={classes.instructions}>
          {getStepContent(activeStep)}
        </Typography>
      </div>
    </div>
  );
};

export default HorizontalLabelPositionBelowStepper;
