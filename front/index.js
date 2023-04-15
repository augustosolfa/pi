
fetch('/data').then(response => response.json()).then(data => ({ y: data.temperaturas, type: 'box' })).then(trace => Plotly.newPlot('myDiv', [trace]))
