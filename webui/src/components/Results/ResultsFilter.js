import { Typography } from "@material-ui/core";
import React, { useEffect } from "react";

function getDifferenceInSeconds(date1, date2) {
  const diffInMs = Math.abs(date2 - date1);
  return diffInMs / 1000;
}

const ResultsFilter = (props) => {
  const now = new Date();
  const [updateTime, setUpdateTime] = React.useState(now);
  let [time, setTime] = React.useState(now);
  const [isIdle, setIsIdle] = React.useState(false);

  function filterData(data, filter_length) {
    const now = new Date();
    if (data.length === 0) {
      return "No Results";
    }

    console.log(getDifferenceInSeconds(updateTime, now));

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
      return "UNC";
    }
    return index;
  }

  useEffect(() => {
    const right_now = new Date();
    setUpdateTime(right_now);
    setIsIdle(false);
  }, [props.data]);

  function checkIdle() {
    const right_now = new Date();
    if (getDifferenceInSeconds(updateTime, right_now) > 10) {
      console.log(
        "setting idle",
        getDifferenceInSeconds(updateTime, right_now)
      );
      setIsIdle(true);
    }
  }

  React.useEffect(() => {
    console.log(`initializing interval`);
    const interval = setInterval(() => {
      checkIdle();
    }, 1000);

    return () => {
      console.log(`clearing interval`);
      clearInterval(interval);
    };
  }, []);

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
