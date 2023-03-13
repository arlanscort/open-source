#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 14:59:24 2023

@author: ana.becker
"""
###### Dados horários ######
#%%
# leitura inventário das estações
sim = pd.read_csv('data/estacoes.csv')[['codigo', 'nome', 'latitude', 'longitude']]
sim.sort_values(by='longitude', inplace=True)
sim.reset_index(drop=True, inplace=True)


# leitura dos dados simepar
path = os.getcwd()+'/data/Chuvas-simepar'
csv_files = glob.glob(os.path.join(path, "*.csv"))
psim = pd.DataFrame()
for f in csv_files:
    df_est = pd.read_csv(f)
    df_est['codigo'] = f.split("/")[-1].split("_")[0]
    psim = pd.concat([psim,df_est])    
psim['codigo'] = psim['codigo'].astype(int)
psim = psim.set_index('codigo').join(sim.set_index('codigo'), on='codigo', how='left')
psim.rename(columns = {'datahora': "time",
                        'chuva_mm': 'psim'}, inplace = True) 
psim['time'] = psim['time'].apply(lambda x:x.split("+")[0])
psim['min'] = psim['time'].apply(lambda x:x.split(":")[1])
psim['time'] = pd.to_datetime(psim['time'], format='%Y-%m-%d %H:%M:%S')
psim = psim[psim['min']!='30']  # devido a agregacao cumulativa foram deletados os dados de fracao de hora
psim.drop(columns=['min'], inplace=True)
psim.reset_index(inplace=True)


# dados JAXA gsmap-now

gsmap_now = pd.read_csv('csv/gsmap-now.csv')
gsmap_now = gsmap_now.groupby(['codigo','time']).agg({'prate' : np.mean})
gsmap_now.reset_index(inplace=True)
gsmap_now['time'] = pd.to_datetime(gsmap_now['time'], format='%Y-%m-%d %H:%M:%S')
gsmap_now.drop(gsmap_now[gsmap_now['prate'] < 0].index, inplace = True)
gsmap_now = gsmap_now.sort_values(by='time')
gsmap_now_H = gsmap_now.set_index(['time']).groupby(['codigo']).resample("H", closed='right', label='right').agg({'prate' : np.sum}) 
gsmap_now_H.reset_index(inplace=True)

# dados JAXA gsmap-nrp
gsmap_nrt = pd.read_csv('csv/gsmap-nrt.csv')
gsmap_nrt = gsmap_nrt.groupby(['codigo','time']).agg({'prate' : np.mean})
gsmap_nrt.reset_index(inplace=True)
gsmap_nrt['time'] = pd.to_datetime(gsmap_nrt['time'], format='%Y-%m-%d %H:%M:%S')
gsmap_nrt.drop(gsmap_nrt[gsmap_nrt['prate'] < 0].index, inplace = True)
gsmap_nrt = gsmap_nrt.sort_values(by='time')
gsmap_nrt_H = gsmap_nrt.set_index(['time']).groupby(['codigo']).resample("H", closed='right', label='right').agg({'prate' : np.sum}) 
gsmap_nrt_H.reset_index(inplace=True)
#gsmap_nrp_H.to_csv('csv/gsmap_nrp_H.csv')


# uniao dos dados no mesmo dataframe
df_H = pd.merge(gsmap_now_H, psim, on = ['time','codigo']).rename(columns = {'prate': "gsmap_now",'psim': 'Simepar'}) 
df_H = pd.merge(df_H, gsmap_nrt_H, on = ['time','codigo']).rename(columns = {'prate': "gsmap_nrt"}) 
df_H = df_H.melt(value_vars = ['Simepar','gsmap_now','gsmap_nrt'], id_vars = ['time', 'codigo'])

df_H.to_csv('csv/[H] s j.csv', index=False)


###### Dados diários ######
#%%

df_D = df_H.set_index('time').groupby(['codigo','variable']).resample("D", closed='right', label='right').agg({'value' : np.sum}) 
df_D.reset_index(inplace=True)
df_D = pd.concat([df_D, pnoaa])

df_D.to_csv('csv/[D] s j c.csv', index=False)


###### Dados mensais ######
#%%
df_M = df_D.set_index(['time']).groupby(['codigo','variable']).resample("M", closed='right', label='right').agg({'value' : np.sum})
df_M.reset_index(inplace=True)
df_M.to_csv('csv/[M] s j c.csv', index=False)


