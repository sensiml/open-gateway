import { Grid } from "@material-ui/core";
import Button from "@material-ui/core/Button";
import Drawer from "@material-ui/core/Drawer";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import ListItemText from "@material-ui/core/ListItemText";
import { makeStyles } from "@material-ui/core/styles";
import Toolbar from "@material-ui/core/Toolbar";
import AssessmentIcon from "@material-ui/icons/Assessment";
import InfoIcon from "@material-ui/icons/Info";
import InboxIcon from "@material-ui/icons/MoveToInbox";
import SettingsIcon from "@material-ui/icons/Settings";
import React from "react";
import Divider from "@material-ui/core/Divider";
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

  section1: {
    margin: theme.spacing(2, 1),
  },
}));

const InconSelector = (props) => {
  switch (props.index) {
    case 0:
      return <InfoIcon />;
    case 1:
      return <AssessmentIcon />;
    case 3:
      return <SettingsIcon />;
    case 4:
      return <InboxIcon />;
    default:
      return <InboxIcon />;
  }
};

const Connected = (props) => {
  return (
    <Grid>
      {props.isConnected ? (
        <Button color="primary" variant="contained" aria-label="connected">
          {props.text}: Connected
        </Button>
      ) : (
        <Button variant="contained" aria-label="disconnect" disabled={true}>
          {props.text}: Disconnected
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
          {["Gateway Status", "Test Mode", "Configure"].map((text, index) => (
            <ListItem button key={text} onClick={handleMenu(index)}>
              <ListItemIcon>
                <InconSelector index={index}> </InconSelector>
              </ListItemIcon>
              <ListItemText primary={text} />
            </ListItem>
          ))}
          <div className={classes.section1}>
            <Divider></Divider>
          </div>
          <ListItem>
            <Connected
              text="Device"
              isConnected={props.isConnected}
            ></Connected>
          </ListItem>
          <ListItem>
            <Connected
              text="Video"
              isConnected={props.isCameraConnected}
            ></Connected>
          </ListItem>
        </List>
      </div>
    </Drawer>
  );
};

export default NavBar;
