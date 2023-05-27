import math

from mlprediction import predict

def dataprepare(df, request):
    tipo = request['tipo']
    anoinicial = int(request['anoinicial'])
    anofinal = int(request['anofinal'])
    excluirparciais = request['excluirparciais']

    _df = local(df, request['regiao'], request['estado'])

    predict_anos = predict(_df, tipo, anoinicial, anofinal, request['maxdepth'])

    _df = anos(df, tipo, anoinicial, anofinal, excluirparciais)

    return {"real": packageData(_df, tipo), "previsto": packageData(predict_anos, tipo)}


def local(df, regiao, estado):
    if (regiao != 'Todas'):
        _df = df[df['Regiao'] == regiao]
    elif ((estado) != 'Todos'):
        _df = df[df['Estado'] == estado]
    else:
        _df = df

    return _df


def anos(df, tipo, inicial, final, excluirparciais):
    if tipo == "scatter":
        meio = math.floor((inicial + final) / 2)
        df = df[((df['Data'].dt.year == inicial) | (
            df['Data'].dt.year == final) | (
            df['Data'].dt.year == meio)) & (
            df['Temperatura'].notna())]
    else:
        df = df[(df['Data'].dt.year >= inicial) & (
            df['Data'].dt.year <= final) & (df['Temperatura'].notna())]
    if excluirparciais:
        df = df[df['Inicio'].dt.year < inicial]
    df = df.groupby('Data', as_index=False,
                      sort=True).agg({'Temperatura': 'mean'})
    
    return df

def packageData(df, tipo):
    df = df.groupby(df['Data'].dt.year, as_index=False)
    years = []
    for name, group in df:
        year = {
            'type': tipo,
            'name': name,
            'y': group['Temperatura'].tolist()
        }
        if tipo == "scatter":
            year['x'] = group['Data'].dt.strftime('1900-%m-%d').tolist()
        years.append(year)

    layout = {}

    if tipo == "scatter":
        layout = {
            'xaxis': {
                'tickformat': '%b'
            }
        }

    return {'data': years, 'layout': layout}