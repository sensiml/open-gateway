import { Typography } from "@material-ui/core";
import React from "react";

const ResultsFilter = (props) => {
  function filterData(data, filter_length) {
    if (data.length === 0) {
      return "No Results";
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
      return "UNC";
    }
    return index;
  }

  return (
    <Typography align="center" variant="h1" component="h2">
      {filterData(props.data, props.filter_length)}
    </Typography>
  );
};

export default ResultsFilter;
