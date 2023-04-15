function addOption(id, optionsList) {
    sel = document.getElementById(id)
    for (let option of optionsList) {
        const opt = document.createElement('option')
        opt.value = option
        opt.innerHTML = option
        sel.appendChild(opt)
    }
}

fetch('/options').then(response => response.json()).then(
    data => { addOption('regiao-select', data.regioes); addOption('estado-select', data.estados); addOption('ano-inicial', data.anos); addOption('ano-final', data.anos)}
)

function atualizarAnos() {
    const anoInicial = document.getElementById("ano-inicial");
    const anoFinal = document.getElementById("ano-final");
  
    if (anoInicial.value > anoFinal.value) {
      anoFinal.value = anoInicial.value;
    }
  
    if (anoFinal.value < anoInicial.value) {
      anoInicial.value = anoFinal.value;
    }
  }

function selecionarRegiao() {
    const regiao = document.getElementById('regiao-select')
    const estado = document.getElementById('estado-select')

    if (regiao.value != "Todas") {
        estado.value = "Todos"
        estado.disabled = true
    }
    else {
        estado.disabled = false
    }
}