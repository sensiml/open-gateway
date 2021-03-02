import DeleteForeverIcon from "@material-ui/icons/DeleteForever";
import { Box } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";
import { CSVLink } from "react-csv";

const useStyles = makeStyles((theme) => ({
  linkWrapper: {
    display: "flex",
    padding: theme.spacing(2),
    marginTop: theme.spacing(2),
  },
  link: {
    textDecoration: "none",
    display: "flex",
    alignItems: "center",
    color: "#0277bd",
  },

  icon: {
    marginLeft: theme.spacing(2),
    cursor: "pointer",
  },
}));

const LinkExportToCSV = (props) => {
  const { data, deleteFile, title } = props;
  const classes = useStyles();
  const csvReport = {
    data,
    filename: `data.csv`,
  };
  return (
    <Box className={classes.linkWrapper}>
      <CSVLink className={classes.link} {...csvReport}>
        {title}
      </CSVLink>
      <DeleteForeverIcon
        onClick={deleteFile}
        color="primary"
        className={classes.icon}
      />
    </Box>
  );
};

export default LinkExportToCSV;
