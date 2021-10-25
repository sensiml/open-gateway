
export const sensorDataForChart = (column, calibration) => (state) => {
  const { sensorSimpleData } = state.sensorData;
  if (column.includes('Weight(Kg)') == false) {
    column.push('Weight(Kg)');
  }
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
  let sum = 0;
  let conversion = 0.05850 * .1; //  calculated_slope * kg conversion
  sensorSimpleData.forEach((el, i) => {

    let index = i % (column.length - 1);

    result[index].x.push(Math.floor(i / (column.length - 1)));
    result[index].y.push((el - calibration[index]) * conversion);

    if (index == column.length - 2) {
      sum += el - calibration[calibration.length - 1];
      sum *= conversion;
      result[column.length - 1].x.push(Math.floor(i / (column.length - 1)));
      result[column.length - 1].y.push(parseInt(sum));
      sum = 0;
      //debugger;
    }
    else {
      sum += el;
    }

  });


  return result;
};
