export const sensorDataForChart = column => (state) => {
  const { sensorSimpleData } = state.sensorData;
  console.log("HEREE");
  console.log(sensorSimpleData);
  // generate chart zero array
  const result = column.map(name => {
    return {
      x: [],
      y: [],
      type: 'scatter',
      mode: 'lines',
      name,
    };
  });
  // fill result array
  sensorSimpleData.forEach((el, i) => {
    result[i % column.length].x.push(Math.floor(i / column.length));
    result[i % column.length].y.push(el);
  });
  return result;
};
