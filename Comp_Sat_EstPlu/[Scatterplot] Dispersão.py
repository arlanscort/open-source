#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 10:22:28 2023

@author: ana.becker
"""


def disp_plot (df, x, y, freq):
    for i in range(0,len(sim)):
            df_est = df[df['codigo']== sim.codigo[i]]
            vmax = max(np.max(df_est[x]),np.max(df_est[y]))+20
            fig = px.scatter(df_est, 
                          x=x, 
                          y=y, 
                          title = f'Estação {str(sim.codigo[i])} - {str(sim.nome[i])}',
                          labels = {
                              "x": f"Chuva {freq} {x} (mm)",
                              "y": f"Chuva {freq} {y} (mm)"},
                         template = "plotly_white")
            fig.add_shape(type = 'line',
                          x0 = 0,
                          y0 = 0,
                          x1 = vmax,
                          y1 = vmax,
                          line = dict(color='black',),
                          xref = 'x',
                          yref = 'y'
                          )
            if not os.path.isdir(f'html/[Scatterplot] Dispersão {freq} ({x}-{y})'):
                os.makedirs(f'html/[Scatterplot] Dispersão {freq} ({x}-{y})')
            fig.write_html(f'html/[Scatterplot] Dispersão {freq} ({x}-{y})/{sim.codigo[i]}.html')


# nomes: 'CPC', 'Simepar', 'gsmap_now', 'gsmap_nrt'

# Dispersões horárias
freq = 'horária'
df = pd.read_csv('csv/[H] s j.csv').pivot(index=['time','codigo'],columns='variable',values='value').reset_index()
disp_plot(df, 'Simepar','gsmap_now', freq)
disp_plot(df, 'Simepar','gsmap_nrt', freq)
disp_plot(df, 'gsmap_now','gsmap_nrt', freq)

# Dispersões diárias
freq = 'diária'
df = pd.read_csv('csv/[D] s j c.csv').pivot(index=['time','codigo'],columns='variable',values='value').reset_index()
disp_plot(df, 'Simepar','gsmap_now', freq)
disp_plot(df, 'Simepar','gsmap_nrt', freq)
disp_plot(df, 'gsmap_now','gsmap_nrt', freq)   
disp_plot(df, 'Simepar','CPC', freq)
    
# Dispersões mensais
freq = 'mensal'
df = pd.read_csv('csv/[M] s j c.csv').pivot(index=['time','codigo'],columns='variable',values='value').reset_index()
disp_plot(df, 'Simepar','gsmap_now', freq)
disp_plot(df, 'Simepar','gsmap_nrt', freq)
disp_plot(df, 'gsmap_now','gsmap_nrt', freq)   
disp_plot(df, 'Simepar','CPC', freq)
