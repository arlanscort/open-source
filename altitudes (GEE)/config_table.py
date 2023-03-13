#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  2 14:09:38 2023

@author: ana.becker
"""

import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import fiona

# Leitura das tabelas
#%%
elev = pd.read_csv("AltitudePontos.csv")[['elevation', 'estacao']]
est = pd.read_csv("din_df_estacoes.csv").rename(columns ={'id_estacao':'estacao'})

# Cria dataframe unificado
#%%
df = pd.merge(est, elev)#[['estacao','latitude','longitude','elevation']]
df = df.drop(columns=['altitude'])
df = df.rename(columns ={'elevation':'altitude'})

# Exporta tabela
#%%
df.to_csv('elevacoes.csv')

# Exporta kmz e gpkg
#%%
fiona.supported_drivers['KML'] = 'rw'
gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))
gdf.to_file('elevation.kml', driver='KML')
gdf.to_file("elevation.gpkg", driver="GPKG")

# Cria Figura
#%%
plt.style.use('_mpl-gallery')
plt.scatter(df['longitude'], df['latitude'], c=df['altitude'], marker='o', s=1)
plt.colorbar()
plt.title('Elevação')

plt.savefig('elevation.png', dpi=300)
