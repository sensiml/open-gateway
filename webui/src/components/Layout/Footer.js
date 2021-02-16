import { Paper, Tabs } from "@material-ui/core/";
import { makeStyles } from "@material-ui/core/styles";
import Tab from "@material-ui/core/Tab";
import React from "react";

const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
  },
}));

function Footer() {
  const [value, setValue] = React.useState(0);

  const classes = useStyles();
  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  return (
    <div>
      <Paper className={classes.root}>
        <Tabs
          value={value}
          onChange={handleChange}
          indicatorColor="primary"
          textColor="primary"
          centered
        >
          <Tab label="Item One" />
          <Tab label="Item Two" />
          <Tab label="Item Three" />
        </Tabs>
      </Paper>
    </div>
  );
}

export default Footer;
