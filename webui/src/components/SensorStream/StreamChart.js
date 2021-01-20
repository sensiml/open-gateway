import React from "react";
import Plot from "react-plotly.js";

const StreamChart = (data) => {
  console.log(data.data);
  return <Plot data={data.data} />;
};

export default StreamChart;
