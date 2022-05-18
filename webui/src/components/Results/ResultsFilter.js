import { Typography } from "@material-ui/core";
import React, { useEffect } from "react";

function getDifferenceInSeconds(date1, date2) {
  const diffInMs = Math.abs(date2 - date1);
  return diffInMs / 1000;
}

const ResultsFilter = (props) => {
  const now = new Date();
  const [updateTime, setUpdateTime] = React.useState(now);
  const [isIdle, setIsIdle] = React.useState(false);

  function filterData(data, filter_length) {
    let result = "";
    if (data.length === 0) {
      result = "No Results";
      props.setLastValue(result);
      return result;
    }

    if (filter_length > data.length) {
      filter_length = data.length - 1;
    }

    let m = {};
    for (var i = data.length - filter_length; i < data.length; i++) {
      if (data[i].Classification in m) {
        m[data[i].Classification] += 1;
      } else {
        m[data[i].Classification] = 1;
      }
    }

    let index = 0;
    let max = 0;
    for (const [key, value] of Object.entries(m)) {
      if (value > max) {
        max = value;
        index = key;
      }
    }

    if (max < filter_length / 2) {
      result = "UNC";
      props.setLastValue(result);
      return result;
    }

    result = index;
    props.setLastValue(result);
    return result;

  }

  useEffect(() => {
    let right_now = new Date();
    setUpdateTime(right_now);
    setIsIdle(false);

  }, [props.data]);

  function checkIdle(time) {
    const right_now = new Date();
    if (getDifferenceInSeconds(time, right_now) > props.delay) {
      setIsIdle(true);
      props.setLastValue("Idle");
    }
  }

  React.useEffect(() => {
    if (!isIdle) {
        const interval = setInterval(() => {
        checkIdle(updateTime);
    }, 1000);

    return () => {
      clearInterval(interval);
    };
  }
  }, [updateTime, isIdle]);

  return (
    <>
      {isIdle ? (
        <Typography align="center" variant="h1" component="h2">
              IDLE
        </Typography>
      ) : (
        <Typography align="center" variant="h1" component="h2">
          {filterData(props.data, props.filter_length)}
        </Typography>
      )}
    </>
  );
};

export default ResultsFilter;
