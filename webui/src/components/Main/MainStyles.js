import { makeStyles } from "@material-ui/core/styles";

const useStyles = () =>
  makeStyles((theme) => ({
    root: {
      display: "flex",
    },
    toolbar: {
      display: "flex",
      alignItems: "center",
      justifyContent: "flex-end",
      padding: theme.spacing(0, 1),
      ...theme.mixins.toolbar,
    },
    content: {
      flexGrow: 1,
      width: "100%",
      padding: theme.spacing(5, 5, 5, 35),
      justifyContent: "flex-end",
    },
  }))();

export default useStyles;
