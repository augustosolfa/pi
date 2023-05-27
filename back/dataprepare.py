import math

def dataprepare(df, request):
    _df = local(df, request['regiao'], request['estado'])

    _df = anos(df, request['tipo'], int(request['anoinicial']), int(request['anofinal']))

    _df = _df.groupby(_df['Data'].dt.year, as_index=False)
    years = []
    for name, group in _df:
        year = {
            'type': request['tipo'],
            'name': name,
            'y': group['Temperatura'].tolist()
        }
        if request['tipo'] == "scatter":
            year['x'] = group['Data'].dt.strftime('1900-%m-%d').tolist()
        years.append(year)

    layout = {}

    if request['tipo'] == "scatter":
        layout = {
            'xaxis': {
                'tickformat': '%b'
            }
        }

    return {'data': years, 'layout': layout}


def local(df, regiao, estado):
    if (regiao != 'Todas'):
        _df = df[df['Regiao'] == regiao]
    elif ((estado) != 'Todos'):
        _df = df[df['Estado'] == estado]
    else:
        _df = df

    return _df


def anos(df, tipo, inicial, final):
    if tipo == "scatter":
        meio = math.floor((inicial + final) / 2)
        df = df[((df['Data'].dt.year == inicial) | (
            df['Data'].dt.year == final) | (
            df['Data'].dt.year == meio)) & (
            df['Temperatura'].notna())]
    else:
        df = df[(df['Data'].dt.year >= inicial) & (
            df['Data'].dt.year <= final) & (df['Temperatura'].notna())]
    df = df.groupby(df['Data'], as_index=False,
                      sort=True).agg({'Temperatura': 'mean'})
    
    return df