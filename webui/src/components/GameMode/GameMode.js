import React, { useEffect, useRef, useState } from "react";

import _ from "lodash";
import useSound from 'use-sound';
import CloseOutlinedIcon from '@material-ui/icons/CloseOutlined';
import Confetti from 'react-confetti'

import { Backdrop, Box, IconButton, Button, Grid, Paper, Typography, Zoom } from "@material-ui/core";
import { useSelector } from "react-redux";

import AudioSuccess from "assets/AudioSuccess.mp3"
import AudioBoxingBell from "assets/AudioBoxingBell.mp3"
import AudioFail from "assets/AudioFail.wav"

import logoImg from "assets/logo.png";
import bellImg from "assets/bell.png";
import winnerImg from "assets/rocky-balboa.png";


import { APP_API_URL } from "configs";
import { selectClassImage } from "redux/selectors/classes";
import { useInterval } from "hooks";

import useGameModeStyle from "./GameModeStyle";

const UNKNOW_CLASSES = ["0", 0, "Unknow"];


const bin2String = (array) => {
  const results = String.fromCharCode.apply(null, array).split("\n");
  results.pop();

  return results.map((x) => {
    return JSON.parse(x);
  });
}

export const filterFormatDate = (dateString) => {
  if (!dateString) {
    return "";
  }
  const date = new Date(0);
  date.setSeconds(dateString);
  return date.toISOString().substr(14, 5).replace("0", "");
};

const GameMode = ({ onClose, classMapImages={}, countdownTimeDefault=60, winnerCountThreshold=25 }) => {
  const classes = useGameModeStyle();
  const [isStreaming, setIsStreaming] = useState(false);
  const [reader, setReader] = useState();
  const [playBell, {stop: stopBell}] = useSound(AudioBoxingBell, {
    onplay: () => setPlayingBell(true),
    onend: () => setPlayingBell(false),
  });
  const [playFail, {stop: stopPlainingFail}] = useSound(AudioFail);
  const [playSuccess, {stop: stopPlaingSuccess}] = useSound(AudioSuccess);

  const [playingBell, setPlayingBell] = useState(false);
  const [countdownTime, setCountdownTime] = useState(countdownTimeDefault);
  const [currentClass, setCurrentClass] = useState("");
  const [classScores, setClassScores] = useState({});
  const [totalClassScores, setTotalClassScores] = useState(0);
  const classImage = useSelector(selectClassImage(currentClass));

  const [isWon, setIsWon] = React.useState(false);
  const [isLost, setIsLost] = React.useState(false);

  const useCleanup = (val) => {
    const valRef = useRef(val);
    useEffect(() => {
      valRef.current = val;
    }, [val]);
  
    useEffect(() => {
      return () => {
        if (valRef?.current) {
          valRef.current.cancel();
        }
      };
    }, []);
  };

  const isNotUnknow = (className) => {
    return !UNKNOW_CLASSES.includes(className);
  };

  const handleClose = () => {
    onClose();
  };

  const handleCloseWinnerWindow = () => {
    setIsWon(false);
    handleReset();
  };

  const handleCloseLoserWindow = () => {
    setIsLost(false);
    handleReset();
  };

  const handleStopStreaming = () => {
    setIsStreaming(false);
    reader.cancel();
  };

  const handleLose = async () => {
    playBell();
    handleStopStreaming();
    setTimeout(() => stopBell(), 2000);
    setTimeout(() => playFail(), 2000);
    setTimeout(() => setIsLost(true), 2000);
  };

  const handleWin = () => {
    handleStopStreaming();
    setIsWon(true)
    playSuccess();
  };

  const handleSetCurrentClass = (value) => {
    setCurrentClass(value || "");
  };

  const handleSetResult = (result) => {
    handleSetCurrentClass(result.Classification);
    if (isNotUnknow(result.Classification)) {
      setClassScores(val => {
        const updatedVal = { ...val };
        if (!updatedVal[result.Classification]) {
          updatedVal[result.Classification] = 1;
        } else {
          updatedVal[result.Classification] += 1;
        }
        return updatedVal;
      });
      setTotalClassScores(val => (val + 1));
    }
  };

  const handleReset = () => {
    stopPlaingSuccess();
    stopPlainingFail();
    setCountdownTime(countdownTimeDefault);
    setClassScores({});
    setTotalClassScores(0);
  };

  const handleStartStreamRequest = (
    url=`${process.env.REACT_APP_API_URL}results`,
  ) => {
    handleReset();
    setIsStreaming(true);
    fetch(url, { method: "GET" }).then((response) => {
      const reader = response.body.getReader();
      setReader(reader);
      const stream = new ReadableStream({
        start(controller) {
          // The following function handles each data chunk
          function push() {
            // "done" is a Boolean and value a "Uint8Array"
            reader.read().then(({ done, value }) => {
              // Is there no more data to read?
              if (done) {
                // Tell the browser that we have finished sending data
                setIsStreaming(false);
                controller.close();
                return;
              }
              var results = bin2String(value);

              _.forEach(results, (result) => {
                handleSetResult(result);
              });
  
              push();
            });
          }
  
          push();
        },
      });
  
      return new Response(stream, { headers: { "Content-Type": "text/html" } });
    });
  };

  const handleCoundownTimer = () => {
    setCountdownTime(val => (val - 1));
    if (countdownTime - 1 <= 0) {
      handleLose();
    }
  };

  useInterval(
    handleCoundownTimer,
    countdownTime && isStreaming > 0 ? 1000 : null, 
  );

  useCleanup(reader);

  useEffect(() => {
    if (totalClassScores >= winnerCountThreshold) {
      handleWin();
    }
  }, [totalClassScores]);

  return (
    <Box className={classes.gameWrapper}>
      <IconButton color="primary" onClick={handleClose} className={classes.gameWrapperCloseIcon} size="medium">
        <CloseOutlinedIcon />
      </IconButton>
      <Grid
        container 
        direction="row"
        justifyContent="space-between"
        alignItems="flex-start"
        className={classes.topContainerWrapper}
      >
        <Grid item xs={12} md={6} className={classes.headerWrapper}>
          <Box className={classes.headerWrap}>
            <img className={classes.headerImg} src={logoImg} alt="" />
            <Typography className={classes.headetTitle} variant="h2" color="primary">Intelligent Edge Sensing</Typography>
          </Box>
          <Paper elevation={0} className={classes.timingWrapper}>
            <Typography className={classes.scoreHeader} variant="h4">Timer</Typography>
              <Box className={classes.resultBox}>
                {countdownTime > 0 ? filterFormatDate(countdownTime) : <img className={classes.bellImg} src={bellImg} alt=""/>}
              </Box>
            <Box className={classes.timingButtonsWrapper}>
              <Button variant="contained" color="primary" size="large" disabled={isStreaming} onClick={() => handleStartStreamRequest()}>
                Start
              </Button>
              {isStreaming ?
                <Button variant="outlined" color="primary" onClick={() => handleStopStreaming()}>
                  Stop
                </Button> :
                <Button variant="outlined" color="primary" onClick={() => handleReset()}>
                  Reset
                </Button>
              }
            </Box>
          </Paper>

        </Grid>
        <Grid item xs={12} md={6} className={classes.resultGridWrap}>
        <Zoom in={isStreaming}>
          <Paper elevation={0} className={classes.resultWrapper}>
            <Box className={classes.classImageWrapper} style={{ backgroundImage: `url(${classImage})` }}/>
            <Typography variant="h1">{currentClass}</Typography>
          </Paper>
        </Zoom>
        </Grid>
      </Grid>
      <Grid
        container 
        direction="row"
        className={classes.statsWrapper}
      >
        <Grid item xs={10} md={10} >
          <Typography className={classes.scoreHeader} variant="h4">Your Score</Typography>
          <Box className={classes.scoreWrapper} elevation={0}>
            {_.entries(classMapImages).filter(([name]) => (isNotUnknow(name))).map(([name, imgPath]) => (
              <Paper variant="outlined" className={classes.scoreItem} >
                <Box alt="" className={classes.scoreItemImgBox} style={{ backgroundImage: `url(${APP_API_URL}${imgPath})` }}/>
                <Typography variant="h5">{name}</Typography>
                <Typography variant="h1">{classScores[name] || 0}</Typography>
              </Paper>
            ))}
          </Box>
        </Grid>
        <Grid item xs={2} md={2}>
          <Box className={classes.resultWrapper}>
            <Typography className={classes.scoreHeader} variant="h4">Total</Typography>
            <Paper variant="outlined" className={`${classes.scoreItemImgBox} ${classes.resultBox}`}>{totalClassScores}/{winnerCountThreshold}</Paper>
          </Box>
        </Grid>
      </Grid>
      <Backdrop open={isWon} className={classes.backdrop}>
        <Confetti/>
        <Box className={classes.winnerBox}>
          <img src={winnerImg} alt=""/>
          <Typography className={classes.winnerTypography} variant="h2">Great job! Champ!</Typography>
          <Button variant="outlined" color="primary" size="large" onClick={handleCloseWinnerWindow}>
            Play Again
          </Button>
        </Box>
      </Backdrop>
      <Backdrop open={isLost} className={classes.backdrop}>
        <Box className={classes.winnerBox}>
          <img src={winnerImg} alt=""/>
          <Typography className={classes.loserTypography} variant="h2">Almost! Try Again!</Typography>
          <Button variant="outlined" color="primary" size="large" onClick={handleCloseLoserWindow}>
            Play Again
          </Button>
        </Box>
      </Backdrop>
    </Box>
  );
};

export default GameMode;