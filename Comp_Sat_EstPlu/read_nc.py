#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 13:44:32 2023

@author: ana.becker
"""

############ Estações do simepar ############
sim = pd.read_csv('data/estacoes.csv')[['codigo','latitude','longitude']]
sim.reset_index(drop=True, inplace=True)


# Realiza a leitura dos diversos arquivos .nc tendo como argumento o diretório e salva como csv
def read_nc (path):
    nc_files = glob.glob(os.path.join(path,"*.nc"))
    df_est = pd.DataFrame()
    psat = pd.DataFrame()
      
    for i in range(0,len(sim)):
        print('estacao '+ str(sim.codigo[i]) )
        for f in nc_files:
            xr_nc = xr.open_dataset(f).prate 
            df_mes = xr_nc.sel(lon = sim.longitude[i], lat = sim.latitude[i], method ='nearest').to_dataframe()
            df_mes['codigo'] = sim.codigo[i]   
            df_est = pd.concat([df_est,df_mes])
        psat = pd.concat([psat,df_est])
    psat.to_csv(f"csv/{path.split('/')[-1]}.csv")
    
    
read_nc('data/dados-processados/gsmap-now')
read_nc('data/dados-processados/gsmap-nrt')
