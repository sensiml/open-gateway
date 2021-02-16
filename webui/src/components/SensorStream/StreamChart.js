import React from "react";
import Plot from "react-plotly.js";

const StreamChart = (data) => {
  return (
    <Plot
      data={data.data}
      layout={{
        autosize: true,
        width: 1080,
      }}
    />
  );
};

export default StreamChart;
