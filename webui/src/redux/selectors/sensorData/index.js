
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
  const conversion = [0.005473429951690822, // LoadCel_LF
                        0.00551487290427258, //'LoadCel_LR':'
                        0.005473429951690822, //'LoadCel_RR':
                      0.0054911147011308566, //'LoadCel_RF':
                  ];

                      //  calculated_slope * kg

  let callibrations = [1,100,200,300,-1];
  let val = 0
  let index =0
  const weight_index=column.length-1
  let array_index=0

  sensorSimpleData.forEach((el, i) => {


    index = i % (column.length - 1);

    array_index=Math.floor(i / (column.length - 1));
    val=(el - callibrations[index])*conversion[index];
    sum += val;
    result[index].x.push(array_index);
    result[index].y.push(val);

    if (index === column.length - 2) {
      result[weight_index].x.push(array_index);
      result[weight_index].y.push(parseInt(sum));
      sum = 0;
      //debugger;
    }

  });


  return result;
};
