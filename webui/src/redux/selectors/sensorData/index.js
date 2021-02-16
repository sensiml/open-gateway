export const sensorDataForChart = column => (state) => {
  const { sensorSimpleData } = state.sensorData;
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

export const sensorRecordedDataToCsv = column => (state) => {
  const { sensorRecordedData } = state.sensorData;
  // generate chart zero array
  let result = column.map(name => {
    return [name];
  });
  result.unshift(['column']);
  // fill result array
  sensorRecordedData.forEach((el, i) => {
    result[i % column.length + 1].push(el);
  });
  return [result, sensorRecordedData.length];
};