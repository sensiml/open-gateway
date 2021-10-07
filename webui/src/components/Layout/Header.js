import { AppBar, Button, Toolbar, Typography, Divider } from "@material-ui/core";
import { Update } from "@material-ui/icons";
import { makeStyles } from "@material-ui/core/styles";
import * as React from "react";

const useStyles = () =>
  makeStyles((theme) => ({
    navbarDisplayFlex: {
      display: `flex`,
      justifyContent: `space-between`,
    },
    navDisplayFlex: {
      display: `flex-right`,
      justifyContent: `space-between`,
    },
    linkText: {
      textDecoration: `none`,
      textTransform: `uppercase`,
      color: `white`,
    },
    appBar: {
      zIndex: theme.zIndex.drawer + 1,
    },

  }))();

const navLinks = [
  { title: `company`, path: `/sensiml` },
  { title: `contact`, path: `/contact` },
];



const Header = (props) => {
  const classes = useStyles();
  console.log(props.showUpdateLink)

  return (
    <AppBar position="static" className={classes.appBar}>
      <Toolbar>
        <Typography variant="h6">SensiML Gateway {props.gWVersion}</Typography>
      </Toolbar>
    </AppBar>
  );
};
export default Header;
