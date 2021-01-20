import * as React from "react";
import {
  AppBar,
  Toolbar,
  IconButton,
  List,
  ListItem,
  ListItemText,
  Container,
  Typography,
} from "@material-ui/core";
import { Home } from "@material-ui/icons";
import { makeStyles } from "@material-ui/core/styles";
import CssBaseline from "@material-ui/core/CssBaseline";

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

const Header = () => {
  const classes = useStyles();

  return (
    <AppBar position="static" className={classes.appBar}>
      <Toolbar>
        <Typography variant="h6">SensiML Streaming Gateway</Typography>
      </Toolbar>
    </AppBar>
  );
};
export default Header;
