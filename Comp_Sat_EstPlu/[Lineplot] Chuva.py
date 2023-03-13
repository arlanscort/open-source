#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 15:04:40 2023

@author: ana.becker
"""
   
        
# Totais  Horários
#%%
df = pd.read_csv('csv/[H] s j.csv')
for i in range(0,len(sim)):
        df_est = df[df['codigo']== sim.codigo[i]]
        fig = px.line(df_est, 
                      x='time', 
                      y="value", 
                      color='variable',
                      title = f'Estação {str(sim.codigo[i])} - {str(sim.nome[i])}',
                      labels = {
                          "value":"Chuva",
                          "time": "Data",
                          "variable":"Fonte"},
                     template = "plotly_white")
        fig.write_html(f'html/[Lineplot] Chuva horária/{sim.codigo[i]}.html')
        
        
        
# Totais  Diarios
#%%

df = pd.read_csv('csv/[D] s j c.csv')
for i in range(0,len(sim)):
        df_est = df[df['codigo']== sim.codigo[i]]
        fig = px.line(df_est, 
                      x='time', 
                      y="value", 
                      color='variable',
                      title = f'Estação {str(sim.codigo[i])} - {str(sim.nome[i])}',
                      labels = {
                          "value":"Chuva",
                          "time": "Data",
                          "variable":"Fonte"},
                     template = "plotly_white")
        fig.write_html(f'html/[Lineplot] Chuva diária/{sim.codigo[i]}.html')



# Totais Mensais
#%%
df = pd.read_csv('csv/[M] s j c.csv')
for i in range(0,len(sim)):
        df_est = df[df['codigo']== sim.codigo[i]]
        fig = px.line(df_est, 
                      x='time', 
                      y="value", 
                      color='variable',
                      title = f'Estação {str(sim.codigo[i])} - {str(sim.nome[i])}',
                      labels = {
                          "value":"Chuva",
                          "time": "Data",
                          "variable":"Fonte"},
                     template = "plotly_white")
        fig.write_html(f'html/[Lineplot] Chuva mensal/{sim.codigo[i]}.html')