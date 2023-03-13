#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 15:04:40 2023

@author: ana.becker
"""
   

    
# Totais  Horários
#%%
df = pd.read_csv('csv/[H] s j.csv')

fontes = df.variable.unique()
for i in range(0,len(sim)):
        df_est = df[df['codigo']== sim.codigo[i]]
        fig = go.Figure()
        for j in range(0,len(fontes)):
            sr = df_est[df_est['variable']== fontes[j]]
            fig.add_trace(go.Scatter(x=sr.time, 
                                     y=sr.value, 
                                     name=fontes[j], 
                                     line=dict(color=cores_plotly[j], shape='vh')))
            fig.update_layout(legend_title_text = "Fonte",
                              title={'text': f'Estação {str(sim.codigo[i])} - {str(sim.nome[i])}'},
                              template = 'plotly_white')
            fig.update_yaxes(title_text="Chuva horária (mm)")
            fig.update_xaxes(title_text="Data")
        fig.write_html(f'html/[Hyetographs] Chuva horária/{sim.codigo[i]}.html')  
               

        
# Totais  Diarios
#%%
df = pd.read_csv('csv/[D] s j c.csv')

fontes = df.variable.unique()
for i in range(0,len(sim)):
        df_est = df[df['codigo']== sim.codigo[i]]
        fig = go.Figure()
        for j in range(0,len(fontes)):
            sr = df_est[df_est['variable']== fontes[j]]
            fig.add_trace(go.Scatter(x=sr.time, 
                                     y=sr.value, 
                                     name=fontes[j], 
                                     line=dict(color=cores_plotly[j], shape='vh')))
            fig.update_layout(legend_title_text = "Fonte",
                              title={'text': f'Estação {str(sim.codigo[i])} - {str(sim.nome[i])}'},
                              template = 'plotly_white')
            fig.update_yaxes(title_text="Chuva diária (mm)")
            fig.update_xaxes(title_text="Data")
        fig.write_html(f'html/[Hyetographs] Chuva diária/{sim.codigo[i]}.html')



# Totais Mensais
#%%
df = pd.read_csv('csv/[M] s j c.csv')

fontes = df.variable.unique()
for i in range(0,len(sim)):
        df_est = df[df['codigo']== sim.codigo[i]]
        fig = go.Figure()
        for j in range(0,len(fontes)):
            sr = df_est[df_est['variable']== fontes[j]]
            fig.add_trace(go.Scatter(x=sr.time, 
                                     y=sr.value, 
                                     name=fontes[j], 
                                     line=dict(color=cores_plotly[j], shape='vh')))
            fig.update_layout(legend_title_text = "Fonte",
                              title={'text': f'Estação {str(sim.codigo[i])} - {str(sim.nome[i])}'},
                              template = 'plotly_white')
            fig.update_yaxes(title_text="Chuva mensal (mm)")
            fig.update_xaxes(title_text="Data")
        fig.write_html(f'html/[Hyetographs] Chuva mensal/{sim.codigo[i]}.html')