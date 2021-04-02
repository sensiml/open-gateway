import { Grid, Typography } from "@material-ui/core";
import { green, red, grey } from '@material-ui/core/colors';
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
import HomeIcon from "@material-ui/icons/Home";
import React from "react";
import Divider from "@material-ui/core/Divider";
import FiberManualRecordIcon from '@material-ui/icons/FiberManualRecord';
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
      return <HomeIcon />;
    case 1:
      return <AssessmentIcon />;
    default:
      return <InboxIcon />;
  }
};

const Connected = (props) => {
  return (
    <Grid>
      {props.isConnected ? (
        <Typography> <FiberManualRecordIcon   style={{  fontSize: 16, color: green[500] }}></FiberManualRecordIcon> Connected  </Typography> 
        
      ) : (
        <Typography> <FiberManualRecordIcon   style={{  fontSize: 16, color: grey[500] }}> </FiberManualRecordIcon>  Not Connected </Typography>  
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
          {["Home", "Test Mode"].map((text, index) => (
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
            <Typography color='primary'>Device Status</Typography>
          </ListItem>
          <ListItem>
            <Connected
              text="Device"
              isConnected={props.isConnected}
            ></Connected>
          </ListItem>
          <ListItem>
            <Typography color='primary'>Video Status</Typography>
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
