from data.datacenter import DataCenter
from dataprepare import dataprepare

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
    return dataprepare(df, data)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)