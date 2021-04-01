import { Grid } from "@material-ui/core";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import List from "@material-ui/core/List";
import ListItem from "@material-ui/core/ListItem";
import ListItemText from "@material-ui/core/ListItemText";
import { makeStyles } from "@material-ui/core/styles";
import Typography from "@material-ui/core/Typography";
import React from "react";

const useStyles = makeStyles({
  root: {
    minWidth: 275,
  },
  bullet: {
    transform: "scale(1.0)",
  },
  title: {
    fontSize: 20,
    backgroundColor: "#e0e0e0",
  },
  pos: {
    marginBottom: 2,
    marginTop: 2,
  },
});

const SimpleCard = (props) => {
  const classes = useStyles();
  return (
    <Grid item xs={props.xs}>
      <Typography align="center" className={classes.title} color="textPrimary">
        {props.name}
      </Typography>
      {props.list ? (
        <div className={classes.bullet}>
          <List dense={true}>
            {props.value.split(",").map((value) => (
              <ListItem>
                <ListItemText align="center" primary={value} />
              </ListItem>
            ))}
          </List>
        </div>
      ) : (
        <Typography
          align="center"
          className={classes.pos}
          color="textSecondary"
        >
          {props.value}
        </Typography>
      )}
    </Grid>
  );
};

export default SimpleCard;
