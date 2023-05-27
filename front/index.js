function drawData() {
    // fetch('/data').then(response => response.json()).then(data => ({ y: data.temperaturas, type: 'box' })).then(trace => Plotly.newPlot('myDiv', [trace]))
    options = {
        regiao: document.getElementById('regiao-select').value,
        estado: document.getElementById('estado-select').value,
        anoinicial: document.getElementById('ano-inicial').value,
        anofinal: document.getElementById('ano-final').value,
        tipo: document.getElementById('type-select').value,
        excluirparciais: document.getElementById('excluirparciais').checked
    }
    
    fetch('/data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(options)
    })
        .then(response => response.json())
        .then(response => Plotly.newPlot('myDiv', response.data, response.layout))

}

