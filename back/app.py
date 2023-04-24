from data.datacenter import DataCenter

from flask import Flask, send_from_directory, redirect, request
import os


df = DataCenter().getDataFrame()
assert df is not None
df_criosfera = df[df['Estacao'] == 'CRIOSFERA']
df = df[df['Estacao'] != 'CRIOSFERA']

appoptions = {
    'regioes':  sorted(df.Regiao.unique().tolist()),
    'estados': sorted(df.Estado.unique().tolist()),
    'anos': sorted(df.Data.dt.year.unique().tolist())
}

app = Flask(__name__)


@app.route("/teste")
def teste():
    teste = {'carro': 'Creta', 'ano': 2020}
    return teste


@app.route('/')
def index():
    return redirect('/index.html')


@app.route('/<path:path>')
def root(path):
    return send_from_directory(os.path.join(os.getcwd(), 'front'), path)


@app.route('/data')
def datacriosfera():
    return {
        'datas': df_criosfera["Data"].dt.strftime('%Y-%m-%d').tolist(),
        'temperaturas': df_criosfera["Temperatura"].tolist(),
        'precipitacoes': df_criosfera["Precipitacao"].tolist()
    }


@app.route('/options')
def options():
    return appoptions


@app.route('/data', methods=['POST'])
def data():
    data = request.get_json()
    if (data['regiao'] != 'Todas'):
        _df = df[df['Regiao'] == data['regiao']]
    elif ((data['estado']) != 'Todos'):
        _df = df[df['Estado'] == data['estado']]
    else:
        _df = df

    _df = _df[(_df['Data'].dt.year >= int(data['anoinicial'])) & (
        _df['Data'].dt.year <= int(data['anofinal'])) & (_df['Temperatura'].notna())]
    _df = _df.groupby(_df['Data'], as_index=False,
                      sort=True).agg({'Temperatura': 'mean'})

    _df = _df.groupby(_df['Data'].dt.year, as_index=False)
    years = []
    for name, group in _df:
        year = {
            'type': data['tipo'],
            'name': name,
            'y': group['Temperatura'].tolist()
        }
        if data['tipo'] == "scatter":
            year['x'] = group['Data'].dt.strftime('1900-%m-%d').tolist()
        years.append(year)

    layout = {}

    if data['tipo'] == "scatter":
        layout = {
            'xaxis': {
                'tickformat': '%b'
            }
        }

    return {'data': years, 'layout': layout}


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)