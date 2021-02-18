import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Drawer from "@material-ui/core/Drawer";
import Toolbar from "@material-ui/core/Toolbar";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import ListItemText from "@material-ui/core/ListItemText";
import InboxIcon from "@material-ui/icons/MoveToInbox";
import SettingsIcon from "@material-ui/icons/Settings";
import InfoIcon from "@material-ui/icons/Info";
import AssessmentIcon from "@material-ui/icons/Assessment";
import AssignmentIcon from "@material-ui/icons/Assignment";
import { Grid } from "@material-ui/core";
import Button from "@material-ui/core/Button";

const drawerWidth = 240;

const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
  },
  appBar: {
    zIndex: theme.zIndex.drawer + 1,
  },
  drawer: {
    width: drawerWidth,
    flexShrink: 0,
  },
  drawerPaper: {
    width: drawerWidth,
  },
  drawerContainer: {
    overflow: "auto",
  },
  content: {
    flexGrow: 1,
    padding: theme.spacing(3),
  },
}));

const IconSelector = (props) => {
  switch (props.index) {
    case 0:
      return <InfoIcon />;
    case 1:
      return <AssessmentIcon />;
    case 2:
      return <SettingsIcon />;
    default:
      return <InboxIcon />;
  }
};

const Connected = (props) => {
  return (
    <Grid>
      {props.isConnected ? (
        <Button color="green" variant="contained" aria-label="disconnect">
          Connected
        </Button>
      ) : (
          <Button color="red" variant="contained" aria-label="disconnect">
            Disconnected
          </Button>
        )}
    </Grid>
  );
};

const NavBar = (props) => {
  const classes = useStyles();

  const handleMenu = (viewId) => (event) => {
    props.onChange(viewId);
  };

  return (
    <Drawer
      className={classes.drawer}
      variant="permanent"
      classes={{
        paper: classes.drawerPaper,
      }}
    >
      <Toolbar />
      <div className={classes.drawerContainer}>
        <List>
          {["Device Info", "Test Stream", "Configure Gateway"].map(
            (text, index) => (
              <ListItem button key={text} onClick={handleMenu(index)}>
                <ListItemIcon>
                  <IconSelector index={index}> </IconSelector>
                </ListItemIcon>
                <ListItemText primary={text} />
              </ListItem>
            )
          )}
          <ListItem>
            <Connected isConnected={props.isConnected}></Connected>
          </ListItem>
        </List>
      </div>
    </Drawer>
  );
};

export default NavBar;
