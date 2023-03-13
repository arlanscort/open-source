#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 13:44:32 2023

@author: ana.becker
"""


sim = pd.read_csv('data/estacoes.csv')[['codigo','latitude','longitude','nome']]
noaa = xr.open_dataset('data/noaa/dados_cpc.nc').precip


pnoaa = pd.DataFrame()

for i in range(0,len(sim)):
    df_noaa = noaa.sel(lon = sim.longitude[i], lat = sim.latitude[i], method ='nearest').to_dataframe()
    df_noaa['codigo'] = sim.codigo[i] 
    pnoaa = pd.concat([pnoaa,df_noaa])
    
    
pnoaa.rename(columns = {'precip': "value"}, inplace = True) 
pnoaa.reset_index(inplace=True)
pnoaa['time'] = pd.to_datetime(pnoaa['time'], format='%Y-%m-%d %H:%M:%S')+ timedelta(hours = 12)
pnoaa.drop(columns=['lat','lon'], inplace=True)

pnoaa['time'] = pnoaa['time'].apply(lambda x:str(x).split(" ")[0])
pnoaa['time'] = pd.to_datetime(pnoaa['time'], format='%Y-%m-%d %H:%M:%S')
pnoaa['variable'] = 'CPC'
pnoaa = pnoaa.sort_values(by='time')
pnoaa = pnoaa[pnoaa['time']>=pd.to_datetime('2019-06-27', format='%Y-%m-%d')] 
pnoaa = pnoaa[pnoaa['time']<=pd.to_datetime('2022-12-31', format='%Y-%m-%d')] 


