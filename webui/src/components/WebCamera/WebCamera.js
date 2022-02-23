import _ from "lodash";
import React, { useEffect, useCallback } from "react";
import {
  Button,
  Tooltip,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Grid,
  FormHelperText,
  IconButton,
  Typography,
  Box,
} from "@material-ui/core";
import Divider from "@material-ui/core/Divider";
import CachedIcon from "@material-ui/icons/Cached";
import { makeStyles } from "@material-ui/core/styles";
import axios from "axios";
import Camera from "./Camera";

const SOURCE_SCREEN_INDEX = -1;

const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
  },
  details: {
    display: "flex",
    flexDirection: "column",
  },
  content: {
    flex: "1 0 auto",
  },
  controls: {
    display: "flex",
    alignItems: "center",
    paddingLeft: theme.spacing(1),
    paddingBottom: theme.spacing(1),
  },
  section1: {
    margin: theme.spacing(2, 0, 3, 0),
  },
  section2: {
    margin: theme.spacing(2),
    textAlign: "center",
  },
  divWrapper: {
    margin: theme.spacing(3),
    padding: theme.spacing(2, 2, 2, 2),
    maxWidth: 800,
    minHeight: 800,
  },
  selectWrapper: {
    height: "3.25rem",
  },
  selectSource: {
    width: "100%",
  },
  selectLoading: {
    lineHeight: 3.25,
  },
  cameraViewWrapper: {
    minHeight: "480px",
    minWidth: "640px",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
  },
}));

const handleCameraRequest = (
  event,
  setCameraView,
  setIsCameraConnected,
  setCameraKey,
  indexSource
) => {
  console.log(event);

  axios
    .post(`${process.env.REACT_APP_API_URL}config-video`, {
      camera_index: indexSource,
      event_type: event,
    })
    .then((response) => {
      console.log(response.data);
      if (event === "camera-on") {
        setCameraView(true);
        setIsCameraConnected(true);
        setCameraKey(Math.random().toString(36).substring(7));
        console.log("caera event");
        console.log(event);
      }
      if (event === "camera-off") {
        setCameraView(false);
        setIsCameraConnected(false);
        console.log("caera event");
        console.log(event);
      }
    });
};

const WebCamera = (props) => {
  const classes = useStyles();
  const [cameraView, setCameraView] = React.useState(false);
  const [cameraKey, setCameraKey] = React.useState("");
  const [videoSourceList, setVideoSourceList] = React.useState([]);
  const [videoSource, setVideoSource] = React.useState(SOURCE_SCREEN_INDEX - 1);
  const [videoSourceLoading, setVideoSourceLoading] = React.useState(false);
  const [videoSourceLoadError, setVideoSourceLoadError] = React.useState("");

  const loadVideoSource = async () => {
    setVideoSourceLoadError("");
    setVideoSourceLoading(true);
    try {
      const response = await axios.get(
        `${process.env.REACT_APP_API_URL}scan-video`,
        {}
      );
      const { video_sources } = response.data;
      if (!_.isEmpty(video_sources) && _.isArray(video_sources)) {
        const mainSource = video_sources.find((el) => el.index === 0);
        setVideoSourceList(video_sources);
        setVideoSource(mainSource.index);
      }
    } catch (e) {
      setVideoSourceLoadError(
        "Failed to load video sources, please, try again"
      );
    }
    setVideoSourceLoading(false);
  };

  useEffect(() => {
    loadVideoSource();
  }, []);

  const getVideoSourceName = useCallback(() => {
    // useCallback
    const name = "Camera";
    if (!_.isEmpty(videoSourceList) && _.isArray(videoSourceList)) {
      return (
        videoSourceList.find((el) => el.index === videoSource)?.name || name
      );
    }
    return name;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [videoSource]);

  const handleUpdateVideoSourceList = () => {
    loadVideoSource();
  };

  const handleCameraSourceSelect = (e) => {
    setVideoSource(e.target.value);
  };

  return (
    <div>
      <div className={classes.section1}>
        <Typography component="h3" variant="h3" color="secondary">
          Video Source
        </Typography>
      </div>
      <div className={classes.section1}>
        <Divider variant="middle" />
      </div>

      <Camera
        classes={classes}
        cameraKey={cameraKey}
        isCameraConnected={props.isCameraConnected}
      ></Camera>
      <div className={classes.section2}>
        <Typography variant="subtitle1" color="textSecondary"></Typography>
      </div>

      <div className={classes.details}>
        <Grid container rows spacing={2}>
          <Grid item xs={12}>
            <Box
              className={classes.selectWrapper}
              display="flex"
              alignItems="center"
              justifyContent="center"
            >
              {videoSourceLoadError ? (
                <Typography color="error"> {videoSourceLoadError} </Typography>
              ) : videoSourceLoading ? (
                <Box className={classes.selectLoading}>{"Loading..."}</Box>
              ) : (
                <>
                  <FormControl
                    className={classes.selectSource}
                    variant="standard"
                    sx={{ m: 1, minWidth: 120 }}
                  >
                    <InputLabel id="video_sources_select_label">
                      Video Source
                    </InputLabel>
                    <Select
                      labelId="video_sources_select_label"
                      id="video_sources_select"
                      value={videoSource}
                      onChange={handleCameraSourceSelect}
                      label="Video source"
                      disabled={props.isCameraConnected !== false}
                    >
                      {videoSourceList.map((sourceCam) => (
                        <MenuItem
                          value={sourceCam.index}
                          key={`source_select_${sourceCam.index}`}
                        >
                          {sourceCam.name}
                        </MenuItem>
                      ))}
                    </Select>
                    {props.isCameraConnected !== false ? (
                      <FormHelperText id="my-helper-text">
                        To change souce, first disconnect {getVideoSourceName()}
                      </FormHelperText>
                    ) : null}
                  </FormControl>
                  <Tooltip title="Reload video sources">
                    <IconButton
                      aria-label="delete"
                      size="large"
                      color="primary"
                      disabled={props.isCameraConnected !== false}
                      onClick={handleUpdateVideoSourceList}
                    >
                      <CachedIcon fontSize="inherit" />
                    </IconButton>
                  </Tooltip>
                </>
              )}
            </Box>
          </Grid>
          <Grid item xs={12}>
            {props.isCameraConnected === false ? (
              <Button
                aria-label="Start Camera"
                variant="contained"
                color="primary"
                fullWidth={true}
                disabled={Boolean(videoSource < SOURCE_SCREEN_INDEX)}
                onClick={() => {
                  handleCameraRequest(
                    "camera-on",
                    setCameraView,
                    props.setIsCameraConnected,
                    setCameraKey,
                    videoSource
                  );
                }}
              >
                Connect to {getVideoSourceName()}
              </Button>
            ) : (
              <Button
                aria-label="Stop Camera"
                color="primary"
                variant="contained"
                fullWidth={true}
                onClick={() => {
                  handleCameraRequest(
                    "camera-off",
                    setCameraView,
                    props.setIsCameraConnected,
                    setCameraKey,
                    videoSource
                  );
                }}
              >
                Disconnect {getVideoSourceName()}
              </Button>
            )}
          </Grid>
        </Grid>
      </div>
    </div>
  );
};

export default WebCamera;
