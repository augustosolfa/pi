from sklearn.tree import DecisionTreeRegressor
import pandas as pd
import math

def predict(df, tipo, inicial, final, maxdepth):
    try:
        maxdepth = int(maxdepth)
        if maxdepth > 1000 or maxdepth < 1:
            maxdepth = 100
    except:
        maxdepth = 100

    _df = df[df["Temperatura"].notna()]
    _df = _df.groupby('Data', as_index=False, sort=True).agg({'Temperatura': 'mean'})
    splitDate(_df)

    X = _df[['year', 'month', 'day']]
    y = _df['Temperatura']
    reg = DecisionTreeRegressor(max_depth=maxdepth)
    reg.fit(X, y)
    if tipo=="scatter":
        days = pd.date_range(start=str(math.floor((inicial + final)/2)), end=str(str(math.floor((inicial + final)/2) + 1)), inclusive="left")
    else:
        days = pd.date_range(start=str(inicial), end=str(final + 1), inclusive="left")
    days = days.union(pd.date_range(start="2050", end="2051", inclusive="left"))
    days.name = "Data"
    days = pd.DataFrame(days)
    splitDate(days)
    days['Temperatura'] = reg.predict(days[['year', 'month', 'day']])
    return days

def splitDate(df):
    df['year'] = df['Data'].dt.year
    df['month'] = df['Data'].dt.month
    df['day'] = df['Data'].dt.day

if __name__ == "__main__":
    from app import df
    predict(df, "scatter", 2010, 2020, False)
    print("")
