'''
Created by Arlan Scortegagna, jul/2022
This program plots hyetographs from rainfall series that are aggregated with closed = "right" and label = "right" (end of interval of aggregation)
'''

#%% 
import pandas as pd 
import plotly.graph_objects as go


#%%
data_dir = '../../temp-data'

##%% Series 1 - GSMaP-NRT Ctba
sr_nrt = pd.read_csv(f'{data_dir}/sr.csv', index_col='time', parse_dates=['time']).squeeze('columns')


# #%% Serie 1 - observado
# sr_cpc = pd.read_csv(f'{data_dir}/cpc_daily_ctba.csv', index_col='time', parse_dates=['time']).squeeze('columns')
# sr_cpc.index = pd.to_datetime(sr_cpc.index + pd.Timedelta(12, 'H'))

# ## Serie 2 - estimativa 1
# sr_estacao = pd.read_csv(f'{data_dir}/estacao_ctba_agregado_12utc.csv', parse_dates=['hordatahora'], index_col='hordatahora').squeeze('columns')


#%% Hieotgramas a serem plotados
hietos_series = [sr_nrt]
hietos_cores = ['black']
hietos_nomes = ['GSMaP - NRT Curitiba']


#%% Plot
fig = go.Figure()
for i, sr in enumerate(hietos_series):
    fig.add_trace(go.Scatter(x=sr.index, y=sr, name=hietos_nomes[i], line=dict(color=hietos_cores[i], shape='vh')))
fig.update_layout(height=700, width=1300)
fig.write_html('hyetographs.html')

# %%
