def dataprepare(df, request):
    if (request['regiao'] != 'Todas'):
        _df = df[df['Regiao'] == request['regiao']]
    elif ((request['estado']) != 'Todos'):
        _df = df[df['Estado'] == request['estado']]
    else:
        _df = df

    _df = _df[(_df['Data'].dt.year >= int(request['anoinicial'])) & (
        _df['Data'].dt.year <= int(request['anofinal'])) & (_df['Temperatura'].notna())]
    _df = _df.groupby(_df['Data'], as_index=False,
                      sort=True).agg({'Temperatura': 'mean'})

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