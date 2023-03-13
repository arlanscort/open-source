#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  8 10:04:29 2023

@author: ana.becker
"""

for produto in ['gsmap_now', 'gsmap_nrt']:
    ###### Leitura dos dados ######
    contagem = pd.read_csv(f"csv/indices_{produto}.csv")
    sim = pd.read_csv('data/estacoes.csv')
    results = pd.merge(sim, contagem)
    results_geo = gpd.GeoDataFrame(results, geometry=gpd.points_from_xy(results.longitude, results.latitude))
    parana = gpd.read_file("gpkg/parana.gpkg")
    
    ###### Loop dos gráficos ######
    colors = [(1.0, 0, 0), (1.0, 1.0, 0), (0, 1.0, 0)]
    cmap = matplotlib.colors.LinearSegmentedColormap.from_list('mycmap', colors)
    colors_far = [(0, 1.0, 0), (1.0, 1.0, 0), (1.0, 0, 0)]
    cmap_far = matplotlib.colors.LinearSegmentedColormap.from_list('mycmap', colors_far)
    
    for column in ['ACC', 'POD', 'BIAS', 'HSS']:
        fig, ax = plt.subplots(1, 1)
        ax = parana.plot(color='white', edgecolor='gray', linewidth = 0.5)
    
        results_geo.plot(column=column, ax = ax, figsize=(100,66), cmap=cmap, s= 2)
    
        for i in range(0,len(results)):
            plt.annotate(f'{results.nome[i]} \n {results[column][i]*100:.2f}%', 
                         xy=(results.longitude[i], results.latitude[i]), 
                         xycoords='data',
                         xytext = (1,0), textcoords='offset points',
                         fontsize=2)
    
        plt.title(f'Simepar X {produto}\n{column}')
        ax.set_aspect('equal')
        ax.tick_params(axis='both', labelsize=6)
    
        cb = plt.colorbar(ax.get_children()[1], ax=ax, shrink=0.7)
        cb.ax.tick_params(labelsize=6)
        if not os.path.isdir(f'img/[Geo] Índices/{produto}'):
            os.makedirs(f'img/[Geo] Índices/{produto}')
        plt.savefig(f'img/[Geo] Índices/{produto}/{column}.jpg', dpi = 400)
        plt.close()

    
    
    
    ###### FAR ###### (escala inversa)
    colors_far = [(0, 1.0, 0), (1.0, 1.0, 0), (1.0, 0, 0)]
    cmap_far = matplotlib.colors.LinearSegmentedColormap.from_list('mycmap', colors_far)
    
    fig, ax = plt.subplots(1, 1)
    ax = parana.plot(color='white', edgecolor='gray', linewidth = 0.5)
    results_geo.plot(column='FAR', ax = ax, figsize=(100,66), cmap=cmap_far, s= 2)
    for i in range(0,len(results)):
        plt.annotate(f'{results.nome[i]} \n {results.FAR[i]*100:.2f}%', 
                     xy=(results.longitude[i], results.latitude[i]), 
                     xycoords='data',
                     xytext = (1,0), textcoords='offset points',
                     fontsize=2)
    plt.title(f'Simepar X {produto}\nFAR')
    ax.set_aspect('equal')
    ax.tick_params(axis='both', labelsize=6)
    cb = plt.colorbar(ax.get_children()[1], ax=ax, shrink=0.7)
    cb.ax.tick_params(labelsize=6)
    if not os.path.isdir(f'img/[Geo] Índices/{produto}'):
        os.makedirs(f'img/[Geo] Índices/{produto}')
    plt.savefig(f'img/[Geo] Índices/{produto}/FAR.jpg', dpi = 400)
    plt.close()

    
    
    ###### Mesma figura ###### 
    fig, axs = plt.subplots(3, 2, figsize=(12,10))
    axs = axs.ravel()
    axs[5].axis('off')
    for i, column in enumerate(['ACC', 'POD', 'BIAS', 'HSS','FAR']):
        ax = axs[i]
        ax = parana.plot(color='white', edgecolor='gray', linewidth = 0.5, ax=ax)
        
        if (i==4):
            results_geo.plot(column=column, ax = ax, cmap=cmap_far, s= 16)
        else:
            results_geo.plot(column=column, ax = ax, cmap=cmap, s= 16)
    
        for j in range(0,len(results)):
            ax.annotate(f'{results[column][j]*100:.0f}%', 
                         xy=(results.longitude[j], results.latitude[j]), 
                         xycoords='data',
                         xytext = (1,1), textcoords='offset points',
                         fontsize=7,
                         horizontalalignment='center')
        ax.set_aspect('equal')
        ax.set_title(column, fontsize=8)
        ax.tick_params(axis='both', labelsize=8)
    
        cb = plt.colorbar(ax.get_children()[1], ax=ax, shrink=0.7)
        cb.ax.tick_params(labelsize=8)
        
    fig.suptitle(f'Simepar X {produto}')
        
    if not os.path.isdir(f'img/[Geo] Índices/{produto}'):
        os.makedirs(f'img/[Geo] Índices/{produto}')
    plt.savefig(f'img/[Geo] Índices/{produto}/all.jpg', dpi = 400)
    plt.close()




