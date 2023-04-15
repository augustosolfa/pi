from data.datacenter import DataCenter

df = DataCenter().getDataFrame()
assert df is not None
df_criosfera = df[df['Estacao'] == 'CRIOSFERA']
df = df[df['Estacao'] != 'CRIOSFERA']

print('')