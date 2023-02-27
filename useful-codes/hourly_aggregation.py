'''
Arlan Scortegagna - feb/2023

This program execute some procedures for a consistent hourly aggregation of data from Simepar's 15-min automated rainfall stations

Assumes datetime in UTC and final DataFrame will have the following configuration - closed = 'right' and label = 'right'
'''

#%%
import pandas as pd
import numpy as np
from datetime import datetime

def hourly_aggegation(df):
    print(f'\t{datetime.utcnow().isoformat()}: Hourly Aggregation - Arlan Scortegagna, feb/2023')
    
    print(f'\n\t{datetime.utcnow().isoformat()}: Checando registros duplicados...')
    df_dup = df.loc[df.duplicated(subset=['horestacao', 'hordatahora'], keep=False)]
    if df_dup.empty:
        print(f'\t{datetime.utcnow().isoformat()}: Sem registros duplicados.')
    else:
        df = df.loc[~df.duplicated(subset=['horestacao', 'hordatahora'], keep='last')]
        print(f'\t{datetime.utcnow().isoformat()}: Os dados contem registros duplicados! Ignorando duplicados...')

    print(f'\n\t{datetime.utcnow().isoformat()}: Checando frequencias inesperadas: minutos que nao fecham em 00, 15, 30 ou 45, ou segundos que nao fecham em 00...')
    df['hordatahora'] = pd.to_datetime(df['hordatahora'], utc=True)
    idx1 = df.loc[~df['hordatahora'].dt.minute.isin([0, 15, 30, 45])].index
    idx2 = df.loc[df['hordatahora'].dt.second != 0].index
    idx_freq = idx1.append(idx2)
    df_freq = df.loc[idx_freq]
    if df_freq.empty:
        print(f'\t{datetime.utcnow().isoformat()}: Sem estacoes com frequencias inesperadas.')
    else:
        nunique = df_freq.horestacao.nunique()
        df = df.drop(idx_freq)
        print(f'\t{datetime.utcnow().isoformat()}: Os dados contem {nunique} estaces com frequencias inesperadas! Esses registros serao ignorados! Para verificar os dados, utilize o segundo dataframe retornado.')
        
    print(f'\n\t{datetime.utcnow().isoformat()}: Pivotando...')
    df = df.pivot(index='hordatahora', columns='horestacao', values='horleitura')
    
    print(f'\n\t{datetime.utcnow().isoformat()}: Somando totais horarios...')
    df = df.asfreq('15T')
    df_hr = df.resample('1H', closed='right', label='right').apply(lambda x: x.sum(skipna=False))

    print(f'\n\t{datetime.utcnow().isoformat()}: Concluido.')
    return df_hr, df_freq

    # return 0

if __name__ == '__main__':
    
    # Exemplo
    df = pd.read_csv('../temp-data/chuva_estacoes_2016_2022.csv', usecols=['horestacao', 'hordatahora', 'horleitura', 'horqualidade'], dtype={'horestacao':int, 'hordatahora':str, 'horleitura':float, 'horqualidade':int})
    
    df_hr, df_freq = hourly_aggegation(df)
    