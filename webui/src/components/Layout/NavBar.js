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

const InconSelector = (props) => {
  switch (props.index) {
    case 0:
      return <SettingsIcon />;
    case 1:
      return <InfoIcon />;
    case 2:
      return <AssessmentIcon />;
    case 3:
      return <AssignmentIcon />;
    default:
      return <InboxIcon />;
  }
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
          {["Configure Gateway", "Gateway Status", "View Results"].map(
            (text, index) => (
              <ListItem button key={text} onClick={handleMenu(index)}>
                <ListItemIcon>
                  <InconSelector index={index}> </InconSelector>
                </ListItemIcon>
                <ListItemText primary={text} />
              </ListItem>
            )
          )}
        </List>
      </div>
    </Drawer>
  );
};

export default NavBar;
