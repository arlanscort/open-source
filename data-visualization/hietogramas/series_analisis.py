'''
Created by Arlan Scortegagna, jul/2022
'''

#%% 
import pandas as pd 
import plotly.graph_objects as go


#%%
data_dir = '../../temp-data'

#%% Serie 1 - observado X
sr_cpc = pd.read_csv(f'{data_dir}/cpc_daily_ctba.csv', index_col='time', parse_dates=['time']).squeeze('columns')
sr_cpc.index = pd.to_datetime(sr_cpc.index + pd.Timedelta(12, 'H'))

## Serie 2 - estimativa Y
sr_estacao = pd.read_csv(f'{data_dir}/estacao_ctba_agregado_12utc.csv', parse_dates=['hordatahora'], index_col='hordatahora').squeeze('columns')


# #%% Hieotgramas a serem plotados
# hietos_series = [sr_cpc, sr_estacao]
# hietos_cores = ['black', 'red']
# hietos_nomes = ['CPC Daily - Curitiba', 'Simepar - Estacao Curitiba']


#%% Plot
fig = go.Figure()
fig.add_trace(go.Scatter(x=sr_cpc.values, y=sr_estacao.values, marker='.'))
# fig.update_layout(height=700, width=1300)
# fig.write_html('hyetographs.html')
