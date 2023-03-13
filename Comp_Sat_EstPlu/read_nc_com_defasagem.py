#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 13:44:32 2023

@author: ana.becker
"""

import warnings
warnings.filterwarnings("ignore")


# Funções
#%%

# Cáluculo da distância entre dois pontos
def geoDist (x, y):
    rad = math.pi / 180
    a1 = x[0] * rad
    a2 = x[1] * rad
    b1 = y[0] * rad
    b2 = y[1] * rad
    dlon = b2 - a2
    dlat = b1 - a1
    a = (math.sin(dlat / 2))**2 + math.cos(a1) * math.cos(b1) * (math.sin(dlon / 2))**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    R = 6378.145
    d = R * c
    return(d)

# Leitura dos NetCDFs
# def read_nc (path):
#     nc_files = glob.glob(os.path.join(path,"*.nc"))
#     df_mes = pd.DataFrame()
#     psat = pd.DataFrame()
#     for f in nc_files:
#         df_mes = xr.open_dataset(f).prate.to_dataframe()
#         psat = pd.concat([psat,df_mes])
#     return(psat)
  
# Leitura dos dados
#%%

# Estações do simepar
sim = pd.read_csv('data/estacoes.csv')[['codigo','latitude','longitude']]
sim.reset_index(drop=True, inplace=True)


# Dados de satélite  
# now = read_nc('data/dados-processados/gsmap-now').reset_index()
# nrt = read_nc('data/dados-processados/gsmap-nrt').reset_index()


# Pesos da interpolação temporal
p1=0.5
p2=0.2
p3=0.05


# Loop para cálculo das chuvas para cada estação considerando o método idw para a defasagem espacial 
# e o sistema de pesos para a defasagem temporal
#%%
path = 'data/dados-processados/gsmap-nrt'
nc_files = glob.glob(os.path.join(path,"*.nc"))

for j in [0.05,0.5,1]:
    psat_todos = pd.DataFrame()
    for f in nc_files:
        print(f)
        xr_nc = xr.open_dataset(f).prate.to_dataframe().reset_index()
        psat = pd.DataFrame()   
        dist = xr_nc[['lat','lon']].drop_duplicates(subset=['lat','lon'])
        
        for k in range(len(sim)): # para cada estacao do simepar
            print('estacao '+ str(sim.codigo[k]) )
            dist['d']= dist.apply(lambda x: geoDist([x['lat'], x['lon']],[sim.latitude[k], sim.longitude[k]]), axis=1)
            selecao = dist[dist['d']<=30]
            selecao['idw'] = selecao.apply(lambda x: 1/(x['d']**2), axis=1)
            selecao['idw'] /= selecao['idw'].sum()
            chuvas = pd.merge(xr_nc,selecao)
            chuvas['chuva'] = chuvas.apply(lambda x: x['prate']*x['idw'], axis=1)
            chuvas = chuvas.groupby(['time']).agg({'chuva':np.sum}).reset_index()
            chuvas['chuva_time']=None
            latlongs = xr_nc[['lat','lon']].drop_duplicates(subset=['lat','lon']).reset_index(drop=True)
            chuvas_time = pd.DataFrame()
            
            for i in range(len(chuvas)):
                try: 
                    a = chuvas.chuva[i-2]
                except:
                    a = None
                try:
                    b = chuvas.chuva[i-1]
                except:
                    b = None
                try:
                    c = chuvas.chuva[i]
                except:
                    c = None
                try:
                    d = chuvas.chuva[i+1]
                except:
                    d = None
                try:
                    e = chuvas.chuva[i+2]
                except:
                    e = None
                try:
                    chuvas.chuva_time[i] = a*p3+b*p2+c*p1+d*p2+e*p3
                except:
                    chuvas.chuva_time[i] = None
            chuvas['codigo'] = sim.codigo[k]
            psat = pd.concat([psat,chuvas])
        
        psat.drop(columns = ['chuva'], inplace = True)
        psat.chuva_time[psat.chuva_time< j] = 0
        psat_todos = pd.concat([psat_todos,psat])
        
    
    psat_todos.to_csv(f'csv/[TimeSpace]gsmap-nrt-{j}mm.csv')
    


# Mapa
#%%
parana = gpd.read_file("gpkg/parana.gpkg")

plt.figure(figsize=(30,20))
parana.plot(color='white', edgecolor='gray', linewidth = 0.5)
plt.scatter(sim.longitude,sim.latitude, s =650, facecolors='none', edgecolors='r', marker = 'o')
plt.scatter(psat.lon,psat.lat, s =0.01, marker = "o")
plt.scatter(sim.longitude,sim.latitude, s =1, c = 'red', marker = "D")
plt.tick_params(axis='both', labelsize=7)
plt.savefig('img/Distribuição espacial.png', dpi = 400)





