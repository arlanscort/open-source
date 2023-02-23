'''
Arlan Scortegagna - feb/2023

This program execute some procedures for a consistent hourly aggregation of data from Simepar's 15-min automated rainfall stations

Assumes datetime in UTC and final DataFrame will have the following configuration - closed = 'right' and label = 'right'
'''

#%%
import pandas as pd
import numpy as np

def hourly_aggegation(df):

    print('\n\tChecando registros duplicados...')
    df_dup = df.loc[df.duplicated(subset=['horestacao', 'hordatahora'], keep=False)]
    if df_dup.empty:
        print('\tSem registros duplicados.')
    else:
        df = df.loc[~df.duplicated(subset=['horestacao', 'hordatahora'], keep='last')]
        print('\tOs dados contem registros duplicados! Ignorando duplicados...')

    print('\n\tChecando frequencias inesperadas: minutos que nao fecham em 00, 15, 30 ou 45, ou segundos que nao fecham em 00...')
    df['hordatahora'] = pd.to_datetime(df['hordatahora'], utc=True)
    idx1 = df.loc[~df['hordatahora'].dt.minute.isin([0, 15, 30, 45])].index
    idx2 = df.loc[df['hordatahora'].dt.second != 0].index
    idx_freq = idx1.append(idx2)
    df_freq = df.loc[idx_freq]
    if df_freq.empty:
        print('\tSem estacoes com frequencias inesperadas.')
    else:
        nunique = df_freq.horestacao.nunique()
        df = df.drop(idx_freq)
        print(f'\tOs dados contem {nunique} estaces com frequencias inesperadas! Esses registros serao ignorados! Para verificar os dados, utilize o segundo dataframe retornado.')

    print('\n\tSomando totais horarios...')
    df = df.pivot(index='hordatahora', columns='horestacao', values='horleitura')
    df = df.asfreq('15T')
    df_hr = df.resample('1H', closed='right', label='right').apply(lambda x: x.sum() if x.count() == 4 else np.nan)

    print('\n\tConcluido.')
    return df_hr, df_freq


if __name__ == '__main__':
    print('\tHourly Aggregation - Arlan Scortegagna, feb/2023')
    
    print('\n\tCarregando DataFrame...')
    df = pd.read_csv('../temp-data/chuva_estacoes_2016.csv', usecols=['horestacao', 'hordatahora', 'horleitura', 'horqualidade'], dtype={'horestacao':int, 'hordatahora':str, 'horleitura':float, 'horqualidade':int})

    df_hr, df_freq = hourly_aggegation(df)
    
    print('\n\tSalvando DataFrame agregado')
    df_hr.to_csv('df_hr.csv')