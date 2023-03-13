#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 10:04:29 2023

@author: ana.becker
"""
    ###### Leitura dos dados ######
contagemp = pd.DataFrame()
for produto in ['gsmap_now', 'gsmap_nrt']:
    contagem = pd.read_csv(f"csv/indices_{produto}.csv")
    contagem['produto']= produto
    contagemp = pd.concat([contagemp, contagem])
    
    
    
sim = pd.read_csv('data/estacoes.csv')['codigo', 'nome', 'latitude', 'longitude']
results = pd.merge(sim, contagemp)
results_geo = gpd.GeoDataFrame(results, geometry=gpd.points_from_xy(results.longitude, results.latitude))
parana = gpd.read_file("gpkg/parana.gpkg")
    
###### Loop dos gráficos ######
colors = [(1.0, 0, 0), (1.0, 1.0, 0), (0, 1.0, 0)]
cmap = matplotlib.colors.LinearSegmentedColormap.from_list('mycmap', colors)
colors_far = [(0, 1.0, 0), (1.0, 1.0, 0), (1.0, 0, 0)]
cmap_far = matplotlib.colors.LinearSegmentedColormap.from_list('mycmap', colors_far)
    

for i, column in enumerate(['ACC', 'POD', 'BIAS', 'HSS','FAR']):
    vmin = results_geo[column].min()
    vmax = results_geo[column].max()
    fig, axs = plt.subplots(1, 2, figsize=(12,6)) # dois produtos por enquanto
    axs = axs.ravel()
    #axs[5].axis('off')
    for k, produto in enumerate(['gsmap_now', 'gsmap_nrt']):
        results_geo_figure =results_geo[results_geo['produto']==produto].reset_index(drop=True)
        
        ax = axs[k]
        ax = parana.plot(color='white', edgecolor='gray', linewidth = 0.5, ax=ax)
        
        if (i==4):
            results_geo_figure.plot(column=column, ax = ax, cmap=cmap_far, s= 16, vmin=vmin, vmax=vmax)
        else:
            results_geo_figure.plot(column=column, ax = ax, cmap=cmap, s= 16, vmin=vmin, vmax=vmax)
    
        for j in range(0,len(results_geo_figure)):
            ax.annotate(f'{results_geo_figure[column][j]*100:.0f}%', 
                         xy=(results_geo_figure.longitude[j], results_geo_figure.latitude[j]), 
                         xycoords='data',
                         xytext = (1,1), textcoords='offset points',
                         fontsize=7,
                         horizontalalignment='center')
        ax.set_aspect('equal')
        ax.set_title(produto, fontsize=8)
        ax.tick_params(axis='both', labelsize=8)
    
        cb = plt.colorbar(ax.get_children()[1], ax=ax, shrink=0.7)
        cb.ax.tick_params(labelsize=8)
        
    fig.suptitle(f'{column}')
        
    if not os.path.isdir(f'img/[Geo] Índices'):
        os.makedirs(f'img/[Geo] Índices')
    plt.savefig(f'img/[Geo] Índices/{column}.jpg', dpi = 400)
    plt.close()




