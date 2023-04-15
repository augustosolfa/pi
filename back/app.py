from data.datacenter import DataCenter

from flask import Flask, send_from_directory, redirect
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
    return send_from_directory(os.path.join(os.getcwd(), 'front') , path)

@app.route('/data')
def data():
    return {
        'datas': df_criosfera["Data"].dt.strftime('%Y-%m-%d').tolist(),
        'temperaturas': df_criosfera["Temperatura"].tolist(),
        'precipitacoes': df_criosfera["Precipitacao"].tolist()
    }

@app.route('/options')
def options():
    return appoptions
