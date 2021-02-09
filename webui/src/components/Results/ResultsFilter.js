import React from "react";
import Plot from "react-plotly.js";



const ResultsFilter = (props) => {
    return (
        <Plot
            data={props.data}
            layout={{
                autosize: true,
            }}
        />
    );
};

export default ResultsFilter;
