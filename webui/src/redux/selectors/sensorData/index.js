
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
  const conversion = [5.473, // LoadCel_LF
                      5.514, //'LoadCel_LR':'
                      5.473, //'LoadCel_RR':
                      5.491, //'LoadCel_RF':
                  ];

                      //  calculated_slope * kg

  let val = 0
  let index =0
  const weight_index=column.length-1
  let array_index=0

  sensorSimpleData.forEach((el, i) => {


    index = i % (column.length - 1);

    array_index=Math.floor(i / (column.length - 1));
    val=(el - calibration[index]);
    //debugger;

    val*=conversion[index];
    sum += val;
    result[index].x.push(array_index);
    result[index].y.push(parseInt(val));

    if (index === column.length - 2) {
      result[weight_index].x.push(array_index);
      result[weight_index].y.push(parseInt(sum));
      sum = 0;
      //debugger;
    }

  });
  console.log(result);

  return result;
};
