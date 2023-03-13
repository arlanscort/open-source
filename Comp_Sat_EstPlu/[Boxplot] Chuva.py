#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 15:04:16 2023

@author: ana.becker
"""



# Totais horários
#%%

# df = pd.read_csv('csv/[H] s j.csv')
# df = pd.merge(df,sim[['codigo','nome']])
# fig = px.box(df, 
#               x='nome', 
#               y="value", 
#               color='variable',
#               title = 'Chuva horária',
#               labels = {
#                   "value":"Chuva horária",
#                   "time": "Data",
#                   "variable":"Fonte",
#                   "nome":"Estação"},
#              template = "plotly_white",
#              category_orders = {'nome':sim.nome.values})
# fig.update_xaxes(type='category')
# fig.write_html('html/[Boxplot] Chuva/[Boxplot] Chuva Horária.html')
        
        
# Totais  Diarios
#%%

df = pd.read_csv('csv/[D] s j c.csv')
df = pd.merge(df,sim[['codigo','nome']])
fig = px.box(df, 
              x='nome', 
              y="value", 
              color='variable',
              title = 'Chuva diária',
              labels = {
                  "value":"Chuva diária",
                  "time": "Data",
                  "variable":"Fonte",
                  "nome":"Estação"},
             template = "plotly_white",
             category_orders = {'nome':sim.nome.values})
fig.update_xaxes(type='category')
fig.write_html('html/[Boxplot] Chuva/[Boxplot] Chuva Diária.html')



# Totais Mensais
#%%

df = pd.read_csv('csv/[M] s j c.csv')
df = pd.merge(df,sim[['codigo','nome']])
fig = px.box(df, 
              x='nome', 
              y="value", 
              color='variable',
              title = 'Chuva mensal',
              labels = {
                  "value":"Chuva mensal",
                  "time": "Data",
                  "variable":"Fonte",
                  "nome":"Estação"},
             template = "plotly_white",
             category_orders = {'nome':sim.nome.values})
fig.update_xaxes(type='category')
fig.write_html('html/[Boxplot] Chuva/[Boxplot] Chuva Mensal.html')