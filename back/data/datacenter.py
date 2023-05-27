import pandas as pd
import numpy as np

import os
import os.path
import csv
import itertools


class DataCenter:
    file = os.path.join(os.path.dirname(__file__), 'dataframe.feather')
    dataframe = None

    def __init__(self):
        if (os.path.isfile(self.file)):
            self.dataframe = pd.read_feather(self.file)
            print(f"[info] Utilizando dados pré gravados em {self.file}")
        else:
            self.dataframe = self.extract_data()

    def getDataFrame(self):
        return self.dataframe

    def extract_data(self):
        rawdir = os.path.join(os.path.dirname(__file__), 'raw')

        separatedFiles = []
        totalfiles = count_files(rawdir)
        counter = 0
        print('[info] Iniciando extração de dados')
        for root, dirs, files in os.walk(rawdir):
            for file in files:
                separatedFiles.append(readFile(os.path.join(root, file)))
                counter += 1
                print(
                    f'\r{counter}/{totalfiles} {int(counter/totalfiles*100)}% dos arquivos lidos', end='')
        df = pd.concat(separatedFiles, ignore_index=True)
        df.to_feather(self.file)
        print('\n[info] Dados extraídos e gravados em ' + self.file)


def count_files(path):
    count = 0
    for root, dirs, files in os.walk(path):
        count += len(files)
    return count


def readFile(file):
    df = pd.read_csv(
        file,
        encoding='cp1252',
        skiprows=8,
        sep=';',
        usecols=[0, 2, 7],
        header=0,
        names=['_Data', 'Precipitacao', 'Temperatura'],
        parse_dates={'Data': [0]},
        decimal=','
    )
    df.loc[df.Precipitacao <0, 'Precipitacao'] = np.nan
    df.loc[df.Temperatura < -100, 'Temperatura'] = np.nan
    df = df.groupby(df['Data'].dt.date).agg(
        {'Data': 'min', 'Precipitacao': 'sum', 'Temperatura': 'median'})
    df.dropna(subset=['Precipitacao', 'Temperatura'], how='all', inplace=True)

    addHeader(df, file)
    df = df[df.Data > df.Inicio]

    return df


def addHeader(dataFrame, file):
    data = []
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for i in itertools.islice(reader, 8):
            data.append(i[1])
    dataFrame['Regiao'] = data[0]
    dataFrame['Estado'] = data[1]
    dataFrame['Estacao'] = data[2]
    dataFrame["Latitude"] = pd.to_numeric(data[4].replace(
        ",", "."), errors='coerce', downcast='float')
    dataFrame["Longitude"] = pd.to_numeric(
        data[5].replace(",", "."), errors='coerce', downcast='float')
    dataFrame["Altitude"] = pd.to_numeric(data[6].replace(
        ",", "."), errors='coerce', downcast='float')
    dataFrame["Inicio"] = toDate(data[7])


def toDate(strDate):
    try:
        return pd.to_datetime(strDate, format="%Y-%m-%d")
    except:
        return pd.to_datetime(strDate, format="%d/%m/%y")

if __name__ == '__main__':
    datacenter = DataCenter()
    print(datacenter.getDataFrame())
