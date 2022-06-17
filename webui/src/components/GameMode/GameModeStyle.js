import { makeStyles, useTheme } from "@material-ui/core/styles";
import { colorbar } from "plotly.js/lib/bar";

const GameModeStyle = makeStyles((theme) => ({
  gameWrapper: {
    height: "100vh",
    width: "100%",
    position: "relative",
    display: "flex",
    flexDirection: "column",
    justifyContent: "space-between"
  },

  topContainerWrapper: {
    padding: "2rem",
    minHeight: "60vh"
  },
  gameWrapperCloseIcon: {
    position: "absolute",
    right: "0",
    top: "0",
    fontSize: "3rem",
  },
  headerWrapper: {
    height: "100%",
  },
  headerImg: {
    maxWidth: "300px",
    marginBottom: "1rem"
  },
  headetTitle: {
    fontFamily: "Calibri",
    fontWeight: 600,
    marginBottom: theme.spacing(1),
  },
  headerWrap: {
    display: "flex",
    alignItems: "flex-end",
    gap: theme.spacing(4),
    height: "30%",
    paddingBottom: "1rem",
  },

  timingWrapper: {
    display: "flex",
    flexDirection: "column",
    justifyContent: "space-between",
    alignItems: "center",
    padding: theme.spacing(4),
    height: "70%",
    width: "100%",
    margin: "auto",
  },
  
  timingButtonsWrapper: {
    display: "flex",
    justifyContent: "center",
    width: "100%",
    "& > button": {
      width: "25%",
      margin: `0 1rem`,
    }
  },

  bellImg: {
    animation: `$myEffect 1000ms ${theme.transitions.easing.easeInOut}`,
    animationDuration: "4s",
    animationIterationCount: "infinite"
  },
  "@keyframes myEffect": {
    "0%": {
      opacity: 1,
      transform: "scale(1)",
    },
    "25%": {
      opacity: 1,
      transform: "scale(0.9)",
    },
    "75%": {
      opacity: 1,
      transform: "scale(1.1)",
    },
    "100%": {
      opacity: 1,
      transform: "scale(1)",
    },
  },
  resultGridWrap: {
    display: "flex",
    height: "100%",
  },
  resultWrapper: {
    display: "flex",
    height: "100%",
    width: "95%",
    marginLeft: "auto",
    flexDirection: "column",
    alignItems: "center",
  },
  classImageWrapper: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    height: "100%",
    width: "60%",
    backgroundSize: "contain",
    backgroundRepeat: "no-repeat",
    backgroundPosition: "center",
    margin: "1rem",
  },
  clsassImageAnimated: {
    animation: `$classAnimation 500ms ${theme.transitions.easing.easeInOut}`,
    animationDuration: "500ms",
  },
  "@keyframes classAnimation": {
    "0%": {
      transform: "scale(1)",
    },
    "100%": {
      transform: "scale(1.15)",
    },
  },
  statsWrapper: {
    marginBottom: "2rem",
    padding: "2rem"
  },

  scoreWrapper: {
    display: "flex",
    margin: "auto",
    justifyContent: "space-between",
    aliginItems: "center",
    flexWrap: "wrap",
    gap: "1rem",
  },
  scoreHeader: {
    color: theme.palette.primary.main,
    marginBottom: theme.spacing(1),
    fontWeight: 600,
  },
  scoreItemImgBox: {
    display: "flex",
    width: "100%",
    minHeight: "130px",
    backgroundRepeat: "no-repeat",
    backgroundSize: "contain",
    backgroundPosition: "center",
    marginBottom: theme.spacing(1),
  },
  scoreItem: {
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
    flex: "1",
    padding: "1rem"
  },

  scoreItemNumber: {
    color: theme.palette.primary.main,
  },
  scoreItemNumberAnimated: {
    animation: `$rotateFullY 800ms ${theme.transitions.easing.easeInOut}`,
    color: theme.palette.primary.main,
  },

  "@keyframes rotateFullY": {
    "0%": { 
      transform: "rotateY(0)"
     },
    "100%": { transform: "rotateY(360deg)" }
  },
  

  resultBox: {
    fontSize: "6rem",
    margin: "0",
    display: "flex",
    height: "100%",
    alignItems: "center",
    justifyContent: "center",
    fontWeight: 600,
    "& > img": {
      width: "60%"
    },
  },
  backdrop: {
    zIndex: theme.zIndex.drawer + 1,
    backgroundColor: "rgba(255, 255, 255, 0.9)",
  },
  winnerBox: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    "& > img": {
      width: "400px",
    },
  },
  winnerTypography: {
    animation: `$colorChange 1000ms ${theme.transitions.easing.easeInOut}`,
    animationIterationCount: "infinite",
    marginBottom: theme.spacing(2),
    marginTop: theme.spacing(2),
  },
  loserTypography: {
    marginBottom: theme.spacing(2),
    marginTop: theme.spacing(2),
  },
  "@keyframes colorChange": {
    "0%": { color: "#0071c5" },
    "100%": { color: "#ffd215" }
  }
}));


export default GameModeStyle;